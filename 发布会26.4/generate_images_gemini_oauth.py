#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 Gemini CLI 的 OAuth 凭据通过 cloudcode-pa API 生成图片

原理：通过 cloudcode-pa.googleapis.com 调用 Gemini 模型，
让模型使用 tool_use 来生成图片描述，然后用 matplotlib 渲染。

注意：cloudcode-pa 端点不支持 responseModalities=IMAGE，
所以改用以下策略：
  1. 如果有 Google AI Studio API Key -> 直接调 Imagen 3
  2. 如果没有 -> 通过 cloudcode-pa 让 Gemini 生成详细图片描述 + matplotlib 渲染

使用方法：
  # 方法1: 设置 Google AI Studio API Key (推荐，去 aistudio.google.com 免费获取)
  export GOOGLE_AI_API_KEY=your_key_here
  python generate_images_gemini_oauth.py

  # 方法2: 仅使用 OAuth (通过 matplotlib 渲染)
  python generate_images_gemini_oauth.py --matplotlib
"""

import sys, io, json, os, time, base64, argparse, requests
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OAUTH_FILE = Path.home() / ".gemini" / "oauth_creds.json"
OUT_DIR = Path("D:/cowork/ppt/发布会26.4/images/generated")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_oauth_token():
    with open(OAUTH_FILE) as f:
        creds = json.load(f)
    expiry = creds.get("expiry_date", 0)
    now = time.time() * (1000 if expiry > 1e12 else 1)
    remaining_min = (expiry - now) / (60000 if expiry > 1e12 else 60)
    if remaining_min < 2:
        print("!! OAuth token 过期，请运行 `gemini` 刷新")
        return None
    print(f"OAuth token 有效 ({remaining_min:.0f}min)")
    return creds["access_token"]


def get_project_id(token):
    """通过 loadCodeAssist 获取项目ID"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = "https://cloudcode-pa.googleapis.com/v1internal:loadCodeAssist"
    payload = {"metadata": {"ideType": "IDE_UNSPECIFIED", "platform": "PLATFORM_UNSPECIFIED", "pluginType": "GEMINI"}}
    resp = requests.post(url, headers=headers, json=payload, timeout=15)
    if resp.status_code == 200:
        return resp.json().get("cloudaicompanionProject", "")
    return ""


def generate_with_ai_studio_key(api_key, prompt, filename, model="imagen-3.0-generate-002"):
    """通过 Google AI Studio API Key 调用 Imagen 3"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:predict?key={api_key}"
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1, "aspectRatio": "16:9", "outputMimeType": "image/png"}
    }
    try:
        resp = requests.post(url, json=payload, timeout=120)
        if resp.status_code == 200:
            predictions = resp.json().get("predictions", [])
            if predictions and "bytesBase64Encoded" in predictions[0]:
                img = base64.b64decode(predictions[0]["bytesBase64Encoded"])
                (OUT_DIR / filename).write_bytes(img)
                print(f"  OK [Imagen3] {filename} ({len(img)//1024}KB)")
                return True
        print(f"  !! Imagen3 [{resp.status_code}]: {resp.text[:150]}")
    except Exception as e:
        print(f"  !! Imagen3 error: {e}")
    return False


def generate_with_genai_sdk(api_key, prompt, filename):
    """通过 google-genai SDK + API Key 调用 Imagen 3"""
    try:
        for k in list(os.environ.keys()):
            if 'GEMINI' in k.upper() or ('GOOGLE' in k.upper() and 'PATH' not in k.upper()):
                os.environ.pop(k, None)

        from google import genai
        from google.genai import types
        from PIL import Image
        from io import BytesIO

        client = genai.Client(api_key=api_key)
        response = client.models.generate_images(
            model='imagen-3.0-generate-002',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio='16:9',
                output_mime_type='image/png',
            )
        )
        if response.generated_images:
            img_bytes = response.generated_images[0].image.image_bytes
            image = Image.open(BytesIO(img_bytes))
            image.save(str(OUT_DIR / filename))
            print(f"  OK [SDK+Imagen3] {filename} ({len(img_bytes)//1024}KB)")
            return True
    except Exception as e:
        print(f"  !! SDK error: {e}")
    return False


def generate_with_gemini_native(api_key, prompt, filename):
    """通过 Gemini 模型原生图片生成 (Nano Banana)"""
    try:
        for k in list(os.environ.keys()):
            if 'GEMINI' in k.upper() or ('GOOGLE' in k.upper() and 'PATH' not in k.upper()):
                os.environ.pop(k, None)

        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        # 尝试多个支持图片输出的模型
        models = ['gemini-2.0-flash-exp', 'gemini-2.5-flash-preview-04-17']
        for model in models:
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=f"Generate a high quality image: {prompt}",
                    config=types.GenerateContentConfig(
                        response_modalities=["TEXT", "IMAGE"],
                        temperature=1.0,
                    )
                )
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        data = part.inline_data.data
                        if isinstance(data, str):
                            data = base64.b64decode(data)
                        (OUT_DIR / filename).write_bytes(data)
                        print(f"  OK [Gemini-{model}] {filename} ({len(data)//1024}KB)")
                        return True
            except Exception as e:
                emsg = str(e)[:100]
                if '404' in emsg or 'not found' in emsg.lower():
                    continue
                print(f"  !! {model}: {emsg}")
    except Exception as e:
        print(f"  !! Gemini native error: {e}")
    return False


# ─── PPT 图片 Prompt 清单 ───
PROMPTS = [
    {
        "name": "cover_bg.png",
        "prompt": (
            "A futuristic smart water network control center, dark blue technology background, "
            "holographic 3D display showing water infrastructure with rivers, dams, pumping stations, "
            "and pipelines connected by glowing blue data streams, AI brain neural network overlay, "
            "clean modern minimalist, cinematic lighting, 8K, professional presentation background"
        ),
    },
    {
        "name": "architecture_3d.png",
        "prompt": (
            "A 4-layer pyramid architecture diagram in 3D isometric style on dark blue background, "
            "layers from bottom: yellow Object Layer with gears, green Engine Layer with algorithms, "
            "orange Skill Layer with puzzle pieces, blue Cognitive Layer with AI brain, "
            "glowing neon connection lines, technology infographic, clean flat design, 16:9"
        ),
    },
    {
        "name": "seven_engines_3d.png",
        "prompt": (
            "Seven interconnected hexagonal engine modules in a circle around central hub, "
            "Simulation(blue), Identification(orange), Scheduling(green), Control(yellow), "
            "Optimization(purple), Prediction(cyan), Learning(red), dark background, "
            "holographic data streams, futuristic UI, professional infographic"
        ),
    },
    {
        "name": "digital_twin_scene.png",
        "prompt": (
            "Photorealistic 3D digital twin of water distribution network, reservoirs canals "
            "pump stations pipelines as transparent holographic models with real-time data overlays, "
            "water flow with blue glowing particles, floating control dashboards, smart city, "
            "cinematic lighting, high-tech atmosphere, 8K"
        ),
    },
    {
        "name": "smart_water_persona.png",
        "prompt": (
            "Four professional personas using smart water AI system in 4 quadrants: "
            "engineer with blueprints, operator with monitoring dashboard, "
            "researcher with algorithms, teacher with students in virtual lab, "
            "modern flat illustration, blue white color scheme, technology icons"
        ),
    },
    {
        "name": "cognitive_ai_flow.png",
        "prompt": (
            "AI cognitive decision flow infographic, 5 connected hexagonal steps left to right: "
            "Intent Understanding, Skill Matching, Rule Loading, Execution, Output Rendering, "
            "dark blue background, glowing neon lines, modern tech dashboard"
        ),
    },
    {
        "name": "component_library.png",
        "prompt": (
            "3D component library for water engineering: physical components (dam pump valve pipe) left, "
            "hydrological (rainfall river groundwater) center, AI models (neural network GNN RL) right, "
            "dark display shelf with holographic labels, isometric 3D, blue tech style"
        ),
    },
    {
        "name": "timeline_strategy.png",
        "prompt": (
            "Horizontal timeline infographic 3 phases: Phase 1 blue single tools replacing Excel, "
            "Phase 2 orange digital twin verification, Phase 3 green full automation revolution, "
            "ascending growth arrow, dark background, modern flat business presentation style"
        ),
    },
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", help="Google AI Studio API Key")
    parser.add_argument("--matplotlib", action="store_true", help="Use matplotlib only")
    args = parser.parse_args()

    print("=" * 60)
    print("HydroClaw 高质量图片生成器 (Gemini)")
    print("=" * 60)

    # 获取 API key
    api_key = args.key or os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    if not api_key:
        # 尝试从 aicode.env 读取
        env_file = Path("d:/cowork/个人/aicode.env")
        if env_file.exists():
            from dotenv import load_dotenv
            load_dotenv(str(env_file))
            api_key = os.environ.get("GEMINI_API_KEY")

    if api_key and not api_key.startswith("sk-"):
        print(f"使用 API Key: {api_key[:10]}...")
    elif api_key and api_key.startswith("sk-"):
        print("API Key 是代理格式(sk-...)，尝试直接使用...")
    else:
        print("!! 未找到 Google AI Studio API Key")
        print("!! 请去 https://aistudio.google.com/apikey 免费获取")
        print("!! 然后运行: set GOOGLE_AI_API_KEY=your_key")
        print("!! 或: python generate_images_gemini_oauth.py --key YOUR_KEY")
        print()

        # 试试OAuth
        token = load_oauth_token()
        if token:
            project = get_project_id(token)
            print(f"GCP Project: {project}")
            print("!! 但 cloudcode-pa 端点不支持图片生成")
            print("!! Vertex AI 未在此项目启用")
        return

    success = 0
    for i, item in enumerate(PROMPTS):
        print(f"\n[{i+1}/{len(PROMPTS)}] {item['name']}")

        # 策略1: SDK + Imagen 3
        if generate_with_genai_sdk(api_key, item["prompt"], item["name"]):
            success += 1
            continue

        # 策略2: REST + Imagen 3
        if generate_with_ai_studio_key(api_key, item["prompt"], item["name"]):
            success += 1
            continue

        # 策略3: Gemini native image
        if generate_with_gemini_native(api_key, item["prompt"], item["name"]):
            success += 1
            continue

        print(f"  !! 所有方法均失败")

    print(f"\n{'='*60}")
    print(f"完成: {success}/{len(PROMPTS)} 张图片")
    print(f"输出: {OUT_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
