import os
import sys
import json
import argparse
try:
    import google.generativeai as genai
except ImportError:
    genai = None

def build_router_engine(api_key: str, prompt_file: str, task_packet: str) -> dict:
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
        with open(task_packet, 'r', encoding='utf-8') as f:
            task_content = f.read()
    except FileNotFoundError as e:
        print(f"[ERROR] Could not read file: {e}")
        sys.exit(1)

    print("[Router Engine] Initializing FrugalGPT Router...")
    if not genai:
        raise ImportError("google.generativeai is not installed")
        
    genai.configure(api_key=api_key)

    print("[Router Engine] Evaluating task complexity...")
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
    response = model.generate_content(
        f"Task Packet:\n{task_content}",
        generation_config=genai.types.GenerationConfig(temperature=0.0)
    )
    
    # Strip json markdown block if present
    text = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Router FrugalGPT Engine")
    parser.add_argument("--task", required=True, help="Path to SOP task packet")
    parser.add_argument("--prompt", required=True, help="Path to router-frugalgpt-prompt.md")
    
    args = parser.parse_args()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[Router Engine] Mocking output for demo since API key is missing...")
        result = {"complexity": 2, "model_choice": "flash"}
    else:
        try:
            result = build_router_engine(api_key, args.prompt, args.task)
        except Exception as e:
            print(f"[ERROR] Parsing failed: {e}")
            sys.exit(1)
            
    print(json.dumps(result, indent=2))
