import os
import sys
import argparse
try:
    import google.generativeai as genai
except ImportError:
    genai = None

def build_architect_engine(api_key: str, prompt_file: str, user_request: str) -> str:
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
    except FileNotFoundError as e:
        print(f"[ERROR] Could not read prompt file: {e}")
        sys.exit(1)

    print("[Architect Engine] Initializing Gemini Architect (MetaGPT/ToT)...")
    if not genai:
        raise ImportError("google.generativeai is not installed")
        
    genai.configure(api_key=api_key)

    print("[Architect Engine] Structuring SOP Task Packet...")
    model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=system_prompt)
    response = model.generate_content(
        f"User Request: {user_request}",
        generation_config=genai.types.GenerationConfig(temperature=0.2)
    )
    
    return response.text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Architect MetaGPT Engine")
    parser.add_argument("--request", required=True, help="Vague user request string")
    parser.add_argument("--prompt", required=True, help="Path to architect-metagpt-prompt.md")
    parser.add_argument("--output", required=True, help="Path to save the generated task packet")
    
    args = parser.parse_args()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[Architect Engine] Mocking output for demo since API key is missing...")
        sop_content = f"# Task Packet: Auto-Generated\n\n## 1. Goal\nImplement: {args.request}\n\n## 2. Files\n- `src/main.py`\n\n## 3. Interfaces\n- `def execute():`\n\n## 4. Constraints\n- Standard rules.\n\n## 5. Verification\n- `pytest`\n"
    else:
        sop_content = build_architect_engine(api_key, args.prompt, args.request)
        
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(sop_content.strip())
        
    print(f"\n[SUCCESS] SOP Task Packet successfully written to: {args.output}")
