#!/bin/bash
# 使用Imagen 3生成HydroClaw架构图

PROMPT="Create a professional 4-layer architecture pyramid diagram for HydroClaw intelligent water network system. Isometric pyramid view with 4 horizontal layers stacked from bottom to top. Layer 4 (bottom, cyan gradient #44A5DC): Object Layer with component icons. Layer 3 (green gradient #4CAF50): Computing Engine Layer with 7 engine icons. Layer 2 (orange gradient #FF7043): Skill Orchestration Layer with workflow icons. Layer 1 (top, purple gradient #7B1FA2): Cognitive Decision Layer with AI brain and rule engine icons. Modern flat design, white background, professional business presentation style, clear visual hierarchy, minimalist, 16:9 aspect ratio, high quality."

# 尝试不同的调用方式
if command -v imagen &> /dev/null; then
    imagen generate "$PROMPT" --output architecture_pyramid.png --size 1920x1080
elif command -v gemini &> /dev/null; then
    echo "$PROMPT" | gemini imagen -o architecture_pyramid.png
else
    echo "Imagen 3 not available, using Python matplotlib instead"
    python ../generate_architecture_diagram.py
fi
