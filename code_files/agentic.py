# agentic.py
# Manages agentic workflows for PyLlamaUI, handling task chaining and code execution

from collections import deque
import subprocess
import tempfile
import os
from api import OllamaAPI

class AgenticWorkflow:
    def __init__(self, api: OllamaAPI):
        """Initialize the agentic workflow with a task queue and Ollama API."""
        self.api = api
        self.task_queue = deque()  # FIFO queue for tasks
        self.results = []  # Store task results

    def add_task(self, task_type: str, prompt: str, depends_on: int = None):
        """Add a task to the queue.
        
        Args:
            task_type: 'generate_code', 'execute_code', or 'analyze'
            prompt: The prompt or input for the task
            depends_on: Index of previous task to use as input (None for independent)
        """
        self.task_queue.append({
            'type': task_type,
            'prompt': prompt,
            'depends_on': depends_on,
            'result': None
        })

    def run_tasks(self):
        """Process tasks in the queue, chaining outputs where needed."""
        while self.task_queue:
            task = self.task_queue.popleft()
            result = self._execute_task(task)
            self.results.append(result)
            task['result'] = result
            yield result  # Stream results for UI integration

    def _execute_task(self, task):
        """Execute a single task based on its type."""
        try:
            if task['type'] == 'generate_code':
                return self._generate_code(task['prompt'], task['depends_on'])
            elif task['type'] == 'execute_code':
                return self._execute_code(task['prompt'], task['depends_on'])
            elif task['type'] == 'analyze':
                return self._analyze(task['prompt'], task['depends_on'])
            else:
                return f"**Error**: Unknown task type '{task['type']}'"
        except Exception as e:
            return f"**Error**: Task failed - {str(e)}"

    def _generate_code(self, prompt, depends_on):
        """Generate code using Ollama API, optionally using previous result."""
        if depends_on is not None and depends_on < len(self.results):
            prompt = f"Based on: {self.results[depends_on]}\n{prompt}"
        # Enforce valid Python syntax in prompt
        response = self.api.send_prompt(
            f"Generate valid Python code for: {prompt}\nEnsure proper syntax (e.g., colons, indentation) and wrap the code in ```python\n```",
            stream=False
        )
        if isinstance(response, str) and "Error" in response:
            return f"**Error**: {response}"
        return f"**Generated Code**:\n{response}"

    def _execute_code(self, code, depends_on):
        """Execute Python code safely using subprocess with syntax check."""
        if depends_on is not None and depends_on < len(self.results):
            code = self.results[depends_on] + "\n" + code
        # Extract code from Markdown block if present
        import re
        code_match = re.search(r'```python\n(.*?)\n```', code, re.DOTALL)
        if code_match:
            code = code_match.group(1)
        # Simple syntax check
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        try:
            # Compile to check syntax (won't execute yet)
            compile(code, temp_file_path, 'exec')
            result = subprocess.run(
                ['python', temp_file_path],
                capture_output=True, text=True, timeout=10
            )
            os.unlink(temp_file_path)
            if result.returncode == 0:
                return f"**Execution Output**:\n```\n{result.stdout}\n```"
            else:
                return f"**Execution Error**:\n```\n{result.stderr}\n```"
        except SyntaxError as e:
            os.unlink(temp_file_path)
            return f"**Syntax Error**: {str(e)}"
        except subprocess.TimeoutExpired:
            os.unlink(temp_file_path)
            return "**Error**: Code execution timed out"
        except Exception as e:
            os.unlink(temp_file_path)
            return f"**Error**: {str(e)}"

    def _analyze(self, prompt, depends_on):
        """Analyze text or code using Ollama API."""
        if depends_on is not None and depends_on < len(self.results):
            prompt = f"Analyze this: {self.results[depends_on]}\n{prompt}"
        response = self.api.send_prompt(
            f"Analyze and provide insights: {prompt}", stream=False
        )
        if isinstance(response, str) and "Error" in response:
            return f"**Error**: {response}"
        return f"**Analysis**:\n{response}"