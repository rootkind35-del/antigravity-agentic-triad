#!/usr/bin/env python3
"""
High-Resolution Visual Diagram Generator for Antigravity Agentic Triad
Programmatically renders a clean, dark-mode architecture flowchart image (assets/architecture_flowchart.png).
"""

import os
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("[WARNING] Pillow library not found. Installing via pip...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    from PIL import Image, ImageDraw, ImageFont

def render_diagram(output_path="assets/architecture_flowchart.png"):
    width, height = 1200, 600
    # Dark mode background
    bg_color = (15, 23, 42)  # Slate 900
    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    # Colors
    cyan = (6, 182, 212)
    purple = (168, 85, 247)
    green = (34, 197, 94)
    blue = (59, 130, 246)
    white = (248, 250, 252)
    gray = (148, 163, 184)
    box_bg = (30, 41, 59)
    border_color = (51, 65, 85)

    # Load default font
    try:
        font_large = ImageFont.truetype("arial.ttf", 22)
        font_main = ImageFont.truetype("arial.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 13)
    except IOError:
        font_large = ImageFont.load_default()
        font_main = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw Title Header
    draw.text((width // 2 - 200, 30), "ANTIGRAVITY AGENTIC TRIAD ARCHITECTURE", fill=white, font=font_large)
    draw.text((width // 2 - 160, 60), "Dynamic Model Switching & Independent Audit Flow", fill=cyan, font=font_small)

    # Box 1: Architect
    draw.rectangle([60, 150, 320, 280], fill=box_bg, outline=purple, width=2)
    draw.text((80, 165), "1. ARCHITECT", fill=purple, font=font_main)
    draw.text((80, 195), "• 5-Part Task Packet (SOP)", fill=gray, font=font_small)
    draw.text((80, 215), "• MetaGPT Handoff Rules", fill=gray, font=font_small)
    draw.text((80, 235), "• Model: Primary Session", fill=gray, font=font_small)

    # Box 2a: Routine Worker (Flash)
    draw.rectangle([440, 120, 720, 240], fill=box_bg, outline=cyan, width=2)
    draw.text((460, 135), "2a. ROUTINE WORKER", fill=cyan, font=font_main)
    draw.text((460, 165), "• Routine / Well-scoped edits", fill=gray, font=font_small)
    draw.text((460, 185), "• Model: Gemini 3.6 Flash", fill=white, font=font_small)
    draw.text((460, 205), "• High Throughput (10% Cost)", fill=gray, font=font_small)

    # Box 2b: Escalated Worker (Pro)
    draw.rectangle([440, 280, 720, 400], fill=box_bg, outline=blue, width=2)
    draw.text((460, 295), "2b. ESCALATED WORKER", fill=blue, font=font_main)
    draw.text((460, 325), "• Retries on 'fix-first' failure", fill=gray, font=font_small)
    draw.text((460, 345), "• Model: Gemini Pro (Auto)", fill=white, font=font_small)
    draw.text((460, 365), "• Deep Logic Reasoning", fill=gray, font=font_small)

    # Box 3: Independent Reviewer
    draw.rectangle([840, 200, 1140, 340], fill=box_bg, outline=green, width=2)
    draw.text((860, 215), "3. INDEPENDENT REVIEWER", fill=green, font=font_main)
    draw.text((860, 245), "• Fresh Conversation Context", fill=gray, font=font_small)
    draw.text((860, 265), "• Checks git diff Ownership", fill=gray, font=font_small)
    draw.text((860, 285), "• Verifies Test Adequacy", fill=gray, font=font_small)
    draw.text((860, 305), "• Model: Gemini Pro", fill=white, font=font_small)

    # Connecting Arrows
    # Architect -> Routine Worker
    draw.line([(320, 180), (440, 180)], fill=cyan, width=2)
    draw.polygon([(435, 175), (445, 180), (435, 185)], fill=cyan)

    # Architect -> Escalated Worker
    draw.line([(320, 250), (380, 250), (380, 340), (440, 340)], fill=blue, width=2)
    draw.polygon([(435, 335), (445, 340), (435, 345)], fill=blue)

    # Routine Worker -> Reviewer
    draw.line([(720, 180), (780, 180), (780, 270), (840, 270)], fill=green, width=2)
    draw.polygon([(835, 265), (845, 270), (835, 275)], fill=green)

    # Escalated Worker -> Reviewer
    draw.line([(720, 340), (780, 340), (780, 270), (840, 270)], fill=green, width=2)

    # Feedback Loop (Reviewer -> Escalated Worker)
    draw.line([(990, 340), (990, 460), (580, 460), (580, 400)], fill=(239, 68, 68), width=2)
    draw.polygon([(575, 405), (580, 395), (585, 405)], fill=(239, 68, 68))
    draw.text((700, 470), "fix-first: Dynamic Model Escalation (Flash -> Pro)", fill=(239, 68, 68), font=font_small)

    # Save image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path, "PNG")
    print(f"[SUCCESS] Visual architecture diagram generated at: {output_path}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "assets/architecture_flowchart.png"
    render_diagram(out)
