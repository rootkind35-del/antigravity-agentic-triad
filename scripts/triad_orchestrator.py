import os
import sys
import subprocess
import json
import argparse
from pathlib import Path

def run_engine(script_name: str, args: list) -> str:
    print(f"\n[{script_name.upper()}] Starting engine...")
    cmd = [sys.executable, f"scripts/{script_name}"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] Engine {script_name} failed: {result.stderr}")
        sys.exit(1)
    
    # Return the stdout, stripping the log lines from the engines
    lines = result.stdout.strip().split('\n')
    output_lines = [l for l in lines if not l.startswith('[')]
    return '\n'.join(output_lines).strip()

def main():
    parser = argparse.ArgumentParser(description="Antigravity Agentic Triad Orchestrator")
    parser.add_argument("--request", required=True, help="Vague user request")
    args = parser.parse_args()
    
    base_dir = Path("examples/orchestrator-demo")
    base_dir.mkdir(parents=True, exist_ok=True)
    
    task_file = base_dir / "task_packet.md"
    diff_file = base_dir / "worker_diff.md"
    memory_file = base_dir / "episodic_memory.md"
    
    # 1. ARCHITECT (MetaGPT)
    print("\n--- PHASE 1: SPECIFICATION ---")
    run_engine("architect_metagpt_engine.py", [
        "--request", args.request,
        "--prompt", "assets/architect-metagpt-prompt.md",
        "--output", str(task_file)
    ])
    
    # 2. ROUTER (FrugalGPT)
    print("\n--- PHASE 2: ROUTING ---")
    router_out = run_engine("router_frugalgpt_engine.py", [
        "--task", str(task_file),
        "--prompt", "assets/router-frugalgpt-prompt.md"
    ])
    
    try:
        routing_data = json.loads(router_out)
        print(f"Selected Model: {routing_data.get('model_choice')} (Complexity: {routing_data.get('complexity')})")
    except:
        print(f"Failed to parse router output: {router_out}")
    
    # REPEAT LOOP
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        print(f"\n--- PHASE 3: EXECUTION (Attempt {attempt}) ---")
        
        worker_args = [
            "--task", str(task_file),
            "--prompt", "assets/worker-swe-prompt.md"
        ]
        if memory_file.exists():
            worker_args.extend(["--memory", str(memory_file)])
            
        worker_out = run_engine("worker_swe_lats_engine.py", worker_args)
        
        # Save diff/output
        with open(diff_file, 'w', encoding='utf-8') as f:
            f.write(worker_out)
            
        print("\n--- PHASE 4: REVIEW ---")
        reviewer_out = run_engine("reviewer_critic_reflexion_engine.py", [
            "--task", str(task_file),
            "--diff", str(diff_file),
            "--prompt", "assets/reviewer-critic-prompt.md"
        ])
        
        try:
            review_data = json.loads(reviewer_out)
            verdict = review_data.get('verdict')
            feedback = review_data.get('feedback')
            memory = review_data.get('memory_log')
            
            print(f"Verdict: {verdict}")
            print(f"Feedback: {feedback}")
            
            if verdict == "ship":
                print("\n[SUCCESS] Triad execution complete!")
                break
            else:
                print("\n[REJECTED] Worker failed the independent audit.")
                with open(memory_file, 'w', encoding='utf-8') as f:
                    f.write(memory)
                
                if attempt == max_retries:
                    print("\n--- PHASE 5: HARNESS OPTIMIZATION (Harness-R1) ---")
                    run_engine("harness_r1_engine.py", [
                        "--task", str(task_file),
                        "--failure", str(memory_file),
                        "--prompt", "assets/harness-engineer-prompt.md",
                        "--output", str(task_file)
                    ])
                    print("[RETHINK] Harness patched. Rebooting system for next cycle...")
                    
        except Exception as e:
            print(f"Reviewer output parsing failed: {e}\n{reviewer_out}")
            break

if __name__ == "__main__":
    main()
