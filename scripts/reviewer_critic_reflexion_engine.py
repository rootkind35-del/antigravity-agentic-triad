import os
import sys
import argparse
import json
try:
    import google.generativeai as genai
except ImportError:
    genai = None

def build_reviewer_engine(api_key: str, prompt_file: str, task_packet: str, diff_file: str) -> dict:
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
        with open(task_packet, 'r', encoding='utf-8') as f:
            task_content = f.read()
        with open(diff_file, 'r', encoding='utf-8') as f:
            diff_content = f.read()
    except FileNotFoundError as e:
        print(f"[ERROR] Could not read file: {e}")
        sys.exit(1)

    print("[Reviewer Engine] Initializing CRITIC/Reflexion Reviewer (Fresh Context)...")
    if not genai:
        raise ImportError("google.generativeai is not installed")
        
    genai.configure(api_key=api_key)

    user_prompt = f"""
    Original SOP Task Packet:
    ```markdown
    {task_content}
    ```
    
    Worker's Git Diff / Execution Output:
    ```diff
    {diff_content}
    ```
    
    Please evaluate this and output your verdict in JSON format.
    """

    print("[Reviewer Engine] Evaluating diff and generating episodic memory...")
    model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=system_prompt)
    response = model.generate_content(
        user_prompt,
        generation_config=genai.types.GenerationConfig(temperature=0.0)
    )
    
    text = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reviewer CRITIC/Reflexion Engine")
    parser.add_argument("--task", required=True, help="Path to SOP task packet")
    parser.add_argument("--diff", required=True, help="Path to git diff or output logs")
    parser.add_argument("--prompt", required=True, help="Path to reviewer-critic-prompt.md")
    
    args = parser.parse_args()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[Reviewer Engine] Mocking output for demo since API key is missing...")
        result = {
            "verdict": "fix-first",
            "feedback": "Worker failed to handle edge cases properly.",
            "memory_log": "DO NOT use modulo % 2 for negative sorting order."
        }
    else:
        try:
            result = build_reviewer_engine(api_key, args.prompt, args.task, args.diff)
        except Exception as e:
            print(f"[ERROR] Review failed: {e}")
            sys.exit(1)
            
    print(json.dumps(result, indent=2))
