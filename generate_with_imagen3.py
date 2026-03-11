#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Google Imagen 3 (Nano Banana Pro) 生成HydroClaw PPT图表
通过Gemini API调用
"""

import os
import sys
import requests
import json
from pathlib import Path

# 读取API Key
env_file = Path("D:/个人/aicode.env")
if not env_file.exists():
    print(f"错误: 找不到API配置文件 {env_file}")
    print("请确保文件存在并包含 GOOGLE_API_KEY")
    sys.exit(1)

# 解析.env文件
api_key = None
with open(env_file, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('GOOGLE_API_KEY='):
            api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
            break

if not api_key:
    print("错误: 在aicode.env中找不到GOOGLE_API_KEY")
    sys.exit(1)

print(f"✓ 已加载API Key (前8位): {api_key[:8]}...")

# Imagen 3 API配置
# 根据搜索结果，模型名称可能是以下之一：
# - gemini-3-pro-image
# - imagen-3
# - imagegeneration@006
IMAGEN_MODEL = "imagen-3"  # 或 "gemini-3-pro-image"
API_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{IMAGEN_MODEL}:generateImages"

def generate_image(prompt, output_path, size="1920x1080"):
    """
    使用Imagen 3生成图片

    Args:
        prompt: 图片描述提示词
        output_path: 输出文件路径
        size: 图片尺寸 (默认1920x1080)
    """
    print(f"\n生成图片: {output_path}")
    print(f"提示词: {prompt[:100]}...")

    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "prompt": prompt,
        "number_of_images": 1,
        "aspect_ratio": "16:9",  # 或使用 size 参数
        "safety_filter_level": "block_few",
        "person_generation": "allow_adult"
    }

    url = f"{API_ENDPOINT}?key={api_key}"

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        result = response.json()

        # 提取图片数据
        if 'generatedImages' in result and len(result['generatedImages']) > 0:
            image_data = result['generatedImages'][0]

            # 如果返回的是base64编码
            if 'bytesBase64Encoded' in image_data:
                import base64
                img_bytes = base64.b64decode(image_data['bytesBase64Encoded'])
                with open(output_path, 'wb') as f:
                    f.write(img_bytes)
                print(f"✓ 已保存: {output_path}")
                return True

            # 如果返回的是URL
            elif 'imageUrl' in image_data:
                img_response = requests.get(image_data['imageUrl'])
                with open(output_path, 'wb') as f:
                    f.write(img_response.content)
                print(f"✓ 已保存: {output_path}")
                return True

        print(f"错误: 未找到生成的图片数据")
        print(f"响应: {json.dumps(result, indent=2)}")
        return False

    except requests.exceptions.RequestException as e:
        print(f"错误: API请求失败 - {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应内容: {e.response.text}")
        return False

# 图表提示词
PROMPTS = {
    "architecture_pyramid.png": """Create a professional 4-layer architecture pyramid diagram for HydroClaw intelligent water network system. Isometric pyramid view with 4 horizontal layers stacked from bottom to top. Layer 4 (bottom, cyan gradient #44A5DC): Object Layer with component icons. Layer 3 (green gradient #4CAF50): Computing Engine Layer with 7 engine icons. Layer 2 (orange gradient #FF7043): Skill Orchestration Layer with workflow icons. Layer 1 (top, purple gradient #7B1FA2): Cognitive Decision Layer with AI brain and rule engine icons. Modern flat design, white background, professional business presentation style, clear visual hierarchy, minimalist, 16:9 aspect ratio, high quality.""",

    "comparison_chart.png": """Create a professional comparison bar chart showing 'Traditional Method vs HydroClaw'. Horizontal grouped bar chart with 4 metrics: Design Efficiency, Accuracy, Explainability, Learning Cost. Traditional Method (gray bars): 30%, 60%, 40%, 80%. HydroClaw (blue bars): 90%, 95%, 85%, 30%. Clean modern business chart, white background, grid lines, bilingual labels (Chinese and English), professional color scheme, data labels on bars, legend. 16:9 aspect ratio.""",

    "decision_flow.png": """Create a professional horizontal workflow diagram showing HydroClaw decision process. 6 circular nodes connected by arrows from left to right: 'User Input' (blue), 'Intent Understanding' (orange), 'Solution Generation' (blue), 'Rule Verification' (orange), 'Optimization' (blue), 'Result Output' (orange). Gray curved arrows connecting nodes. Modern flat design, white background, clean typography, professional business presentation quality, minimalist. 16:9 aspect ratio.""",

    "kpi_metrics.png": """Create a professional 2x2 grid dashboard showing 4 KPIs. Card 1: '15%' in blue, label 'Energy Reduction'. Card 2: '3-5x' in green, label 'Efficiency Improvement'. Card 3: '30%' in orange, label 'Leakage Reduction'. Card 4: '70%' in yellow, label 'Training Time Reduction'. Clean modern dashboard, white background, subtle card shadows, large bold numbers, bilingual labels, professional business presentation quality. 16:9 aspect ratio."""
}

if __name__ == "__main__":
    output_dir = Path("D:/cowork/ppt/nano_diagrams")
    output_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("HydroClaw PPT 图表生成器 (Imagen 3)")
    print("=" * 60)

    success_count = 0
    for filename, prompt in PROMPTS.items():
        output_path = output_dir / filename
        if generate_image(prompt, str(output_path)):
            success_count += 1

    print("\n" + "=" * 60)
    print(f"✓ 成功生成 {success_count}/{len(PROMPTS)} 张图片")
    print("=" * 60)
