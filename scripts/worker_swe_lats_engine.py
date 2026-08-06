import os
import sys
import argparse
import json
try:
    import google.generativeai as genai
except ImportError:
    genai = None

def build_worker_engine(api_key: str, prompt_file: str, task_packet: str, memory_log: str = None) -> str:
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
        with open(task_packet, 'r', encoding='utf-8') as f:
            task_content = f.read()
    except FileNotFoundError as e:
        print(f"[ERROR] Could not read file: {e}")
        sys.exit(1)

    print("[Worker Engine] Initializing SWE-agent Worker...")
    if not genai:
        raise ImportError("google.generativeai is not installed")
        
    genai.configure(api_key=api_key)

    user_prompt = f"Task Packet:\n{task_content}"
    if memory_log:
        try:
            with open(memory_log, 'r', encoding='utf-8') as f:
                memory = f.read()
            user_prompt += f"\n\nReflexion Memory (Past Failure):\n{memory}"
        except:
            pass

    print("[Worker Engine] Executing code modifications (Simulation via LLM)...")
    model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=system_prompt)
    response = model.generate_content(
        user_prompt,
        generation_config=genai.types.GenerationConfig(temperature=0.2)
    )
    
    text = response.text.replace("```json", "").replace("```", "").strip()
    return json.dumps(json.loads(text), indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Worker SWE-agent Engine")
    parser.add_argument("--task", required=True, help="Path to SOP task packet")
    parser.add_argument("--prompt", required=True, help="Path to worker-swe-prompt.md")
    parser.add_argument("--memory", required=False, help="Path to reflexion memory log")
    
    args = parser.parse_args()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[Worker Engine] Mocking output for demo since API key is missing...")
        result = json.dumps({
            "thought_process": "Mocked successful execution of the task.",
            "files_edited": ["src/sort.py"],
            "tools_used": ["replace_file_content"]
        }, indent=2)
    else:
        try:
            result = build_worker_engine(api_key, args.prompt, args.task, args.memory)
        except Exception as e:
            print(f"[ERROR] Execution failed: {e}")
            sys.exit(1)
            
    print(result)
