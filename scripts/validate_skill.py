#!/usr/bin/env python3
"""
Antigravity Agentic Triad Skill Validator for Google Antigravity
Validates YAML frontmatter, file paths, references, and loop boundary rules.
"""

import sys
import os
import re
from pathlib import Path

# Ensure UTF-8 output encoding for Windows terminal compatibility
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def validate_skill(skill_dir: Path) -> bool:
    print(f"[SEARCH] Validating Agentic Triad Skill at: {skill_dir}")
    errors = []
    
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        errors.append("[ERROR] Missing SKILL.md in root directory.")
        return False
        
    content = skill_file.read_text(encoding="utf-8")
    
    # 1. Validate YAML Frontmatter
    frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not frontmatter_match:
        errors.append("[ERROR] Invalid or missing YAML frontmatter in SKILL.md.")
    else:
        fm = frontmatter_match.group(1)
        if "name: antigravity-agentic-triad" not in fm:
            errors.append("[ERROR] Frontmatter name must be 'antigravity-agentic-triad'.")
        if "description:" not in fm:
            errors.append("[ERROR] Frontmatter missing 'description:' property.")
            
    # 2. Check for Guardrail Rules
    if "3 consecutive" not in content or "fix-first" not in content:
        errors.append("[WARNING] Missing explicit 3-cycle fix-first limit check.")
    if "2 consecutive" not in content or "rethink" not in content:
        errors.append("[WARNING] Missing explicit 2-cycle rethink limit check.")
    if "Files/Ownership" not in content:
        errors.append("[WARNING] Missing Files/Ownership scope check reference.")
    if "verification insufficient" not in content:
        errors.append("[WARNING] Missing verification adequacy check rule.")

    # 3. Check Directory Structure
    required_dirs = ["scripts", "references", "examples", "assets"]
    for d in required_dirs:
        dir_path = skill_dir / d
        if not dir_path.exists() or not dir_path.is_dir():
            errors.append(f"[ERROR] Missing recommended directory: {d}/")

    # 4. Check Key Reference Files
    expected_files = [
        "references/dynamic-model-switching.md",
        "references/research-foundation.md",
        "references/architect-guide.md",
        "references/role-contracts.md",
        "references/antigravity-specs.md",
        "assets/task-packet-template.md",
        "assets/review-report-template.md",
        "examples/task-packet-sample.md",
        "examples/review-outcomes-sample.md"
    ]
    for rel_path in expected_files:
        fpath = skill_dir / rel_path
        if not fpath.exists():
            errors.append(f"[ERROR] Missing expected subfile: {rel_path}")

    # Report results
    if errors:
        print("\n[FAIL] Validation Failed with Errors:")
        for err in errors:
            print(f"  {err}")
        return False
        
    print("\n[SUCCESS] Antigravity Agentic Triad Validation Passed Successfully!")
    return True

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent
    success = validate_skill(target)
    sys.exit(0 if success else 1)
