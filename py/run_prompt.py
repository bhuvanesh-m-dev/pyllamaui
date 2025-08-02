# run_prompt.py
import sys
import json
from api import OllamaAPI

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No prompt provided"}))
        return

    prompt = " ".join(sys.argv[1:])
    api = OllamaAPI()
    response_text = api.send_prompt(prompt, stream=False)
    print(json.dumps({"response": response_text}))

if __name__ == "__main__":
    main()
