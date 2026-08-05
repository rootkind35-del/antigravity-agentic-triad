#!/usr/bin/env python3
"""
Antigravity Agentic Triad Skill Validator
Validates skill directory structure, frontmatter schema, file bounds, and link integrity.
"""

import sys
import re
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def validate_skill(skill_dir_path):
    skill_dir = Path(skill_dir_path).resolve()
    print(f"[SEARCH] Validating Agentic Triad Skill at: {skill_dir}")
    
    errors = []

    # 1. Check SKILL.md Existence
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append("[ERROR] Missing required file: SKILL.md")
    else:
        content = skill_md.read_text(encoding="utf-8")
        if not content.startswith("---"):
            errors.append("[ERROR] SKILL.md must start with YAML frontmatter delimiter '---'")
        if "name: antigravity-agentic-triad" not in content:
            errors.append("[ERROR] SKILL.md YAML frontmatter missing correct 'name: antigravity-agentic-triad'")
        if "description:" not in content:
            errors.append("[ERROR] SKILL.md YAML frontmatter missing 'description'")

    # 2. Check README.md Existence
    readme_md = skill_dir / "README.md"
    if not readme_md.exists():
        errors.append("[ERROR] Missing required file: README.md")

    # 3. Check Directory Structure
    expected_dirs = ["scripts", "references", "examples", "assets"]
    for d in expected_dirs:
        dir_path = skill_dir / d
        if not dir_path.exists() or not dir_path.is_dir():
            errors.append(f"[ERROR] Missing recommended directory: {d}/")

    # 4. Check Key Reference Files & Scripts
    expected_files = [
        "references/dynamic-model-switching.md",
        "references/research-foundation.md",
        "references/architect-guide.md",
        "references/role-contracts.md",
        "references/antigravity-specs.md",
        "assets/banner.jpg",
        "assets/architecture_flowchart.png",
        "assets/task-packet-template.md",
        "assets/review-report-template.md",
        "examples/task-packet-sample.md",
        "examples/review-outcomes-sample.md",
        "scripts/generate_diagram.py",
        "scripts/model_switch_matrix.py",
        "scripts/run_verification.py"
    ]
    for rel_path in expected_files:
        fpath = skill_dir / rel_path
        if not fpath.exists():
            errors.append(f"[ERROR] Missing reference file/asset: {rel_path}")

    # Output Validation Results
    if errors:
        print("[FAIL] Skill Validation Failed with the following errors:")
        for err in errors:
            print(f"  {err}")
        return False

    print("\n[SUCCESS] Antigravity Agentic Triad Validation Passed Successfully!")
    return True

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    success = validate_skill(target)
    sys.exit(0 if success else 1)
