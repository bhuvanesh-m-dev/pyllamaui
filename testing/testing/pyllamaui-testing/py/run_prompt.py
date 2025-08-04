import sys
import json
from api import OllamaAPI

def main():
    api = OllamaAPI()
    
    for line in sys.stdin:
        try:
            data = json.loads(line)
            command = data.get("command")
            
            if command == "sendPrompt":
                args = data.get("args", [])
                stream = "--stream" in args
                if stream:
                    args.remove("--stream")
                
                # The prompt is the first argument
                prompt = args[0] if args else ""
                
                if stream:
                    try:
                        for chunk in api.send_prompt(prompt, stream=True):
                            print(json.dumps({"response": chunk}), flush=True)
                    except Exception as e:
                        print(json.dumps({"error": str(e)}), flush=True)
                else:
                    response_text = api.send_prompt(prompt, stream=False)
                    print(json.dumps({"response": response_text}), flush=True)
            
            elif command == "getModelList":
                models = api.get_available_models()
                print(json.dumps({"models": models}), flush=True)

        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON received"}), flush=True)
        except Exception as e:
            print(json.dumps({"error": str(e)}), flush=True)

if __name__ == "__main__":
    main()