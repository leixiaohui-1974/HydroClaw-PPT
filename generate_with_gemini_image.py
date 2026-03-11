#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Google Gemini 3 Pro Image生成HydroClaw PPT图表
通过aicode.cat代理调用
"""

import sys
import io
import requests
import json
import base64
from pathlib import Path

# 设置UTF-8输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# API配置
GEMINI_API_KEY = "sk-253cb0523fb0818434ed0bd4f45e7379161abd56914c7f0f85c57fcbbec7a2f0"
BASE_URL = "https://aicode.cat/v1beta"
MODEL = "gemini-3-pro-image"

def generate_image(prompt, output_path):
    """
    使用Gemini 3 Pro Image生成图片

    Args:
        prompt: 图片描述提示词
        output_path: 输出文件路径
    """
    print(f"\n生成图片: {output_path}")
    print(f"提示词: {prompt[:100]}...")

    url = f"{BASE_URL}/models/{MODEL}:generateContent"

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }

    payload = {
        "contents": [{
            "parts": [{
                "text": f"Generate an image: {prompt}"
            }]
        }],
        "generationConfig": {
            "temperature": 0.4,
            "topK": 32,
            "topP": 1,
            "maxOutputTokens": 4096,
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()
        print(f"API响应: {json.dumps(result, indent=2)[:500]}...")

        # 尝试提取图片数据
        if 'candidates' in result:
            for candidate in result['candidates']:
                if 'content' in candidate:
                    parts = candidate['content'].get('parts', [])
                    for part in parts:
                        # 检查是否有inline_data
                        if 'inline_data' in part:
                            mime_type = part['inline_data'].get('mime_type', '')
                            if 'image' in mime_type:
                                img_data = part['inline_data']['data']
                                # 解码base64
                                img_bytes = base64.b64decode(img_data)
                                with open(output_path, 'wb') as f:
                                    f.write(img_bytes)
                                print(f"✓ 已保存: {output_path}")
                                return True

        print(f"警告: 未找到图片数据")
        return False

    except Exception as e:
        print(f"错误: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应: {e.response.text[:500]}")
        return False

# 图表提示词（简化版，先测试）
PROMPTS = {
    "architecture_pyramid.png": """Professional 4-layer architecture pyramid for HydroClaw water network system. Isometric view, 4 stacked layers. Bottom layer (cyan): Object Layer with component icons. Layer 2 (green): Computing Engine with 7 icons. Layer 3 (orange): Skill Orchestration with workflow. Top layer (purple): Cognitive Decision with AI brain icon. Modern flat design, white background, 16:9, high quality.""",

    "comparison_chart.png": """Professional bar chart comparing Traditional Method vs HydroClaw. 4 metrics: Design Efficiency (30% vs 90%), Accuracy (60% vs 95%), Explainability (40% vs 85%), Learning Cost (80% vs 30%). Gray bars for traditional, blue bars for HydroClaw. Clean modern style, white background, grid, labels, 16:9.""",

    "decision_flow.png": """Professional workflow diagram with 6 circular nodes connected by arrows. Nodes alternate blue and orange: User Input, Intent Understanding, Solution Generation, Rule Verification, Optimization, Result Output. Modern flat design, white background, clean typography, 16:9.""",

    "kpi_metrics.png": """Professional 2x2 dashboard with 4 KPI cards. Top-left: '15%' in blue (Energy Reduction). Top-right: '3-5x' in green (Efficiency). Bottom-left: '30%' in orange (Leakage Reduction). Bottom-right: '70%' in yellow (Training Time). Clean modern dashboard, white background, large numbers, 16:9."""
}

if __name__ == "__main__":
    output_dir = Path("D:/cowork/ppt/nano_diagrams")
    output_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("HydroClaw PPT 图表生成器 (Gemini 3 Pro Image)")
    print("=" * 60)

    success_count = 0
    for filename, prompt in PROMPTS.items():
        output_path = output_dir / filename
        if generate_image(prompt, str(output_path)):
            success_count += 1

    print("\n" + "=" * 60)
    print(f"✓ 成功生成 {success_count}/{len(PROMPTS)} 张图片")
    print("=" * 60)
