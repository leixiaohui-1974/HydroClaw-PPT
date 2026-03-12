#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 Nano Banana Pro (gemini-3-pro-image-preview) 通过 aicode.cat 代理生成图片

使用方法:
  python generate_images_nanobanana.py                    # 生成所有图片
  python generate_images_nanobanana.py --only G01,G02     # 只生成指定ID
  python generate_images_nanobanana.py --skip-existing    # 跳过已有图片
  python generate_images_nanobanana.py --model gemini-2.5-flash-image  # 指定模型
"""

import sys, io, json, os, time, base64, argparse, requests
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from image_prompts import PROMPTS

OUT_DIR = Path("D:/cowork/ppt/发布会26.4/images/generated")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# aicode.cat 代理配置
DEFAULT_BASE_URL = "https://aicode.cat/v1beta"
DEFAULT_API_KEY = None  # 从环境变量或 aicode.env 读取

# Nano Banana 模型优先级列表
MODELS = [
    "gemini-3-pro-image-preview",      # Nano Banana Pro (最佳质量)
    "gemini-3.1-flash-image-preview",   # Nano Banana 2 (最快)
    "gemini-2.5-flash-image",           # Nano Banana (经典)
]


def load_api_key():
    """从环境变量或 aicode.env 加载 API Key"""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key

    env_file = Path("d:/cowork/个人/aicode.env")
    if env_file.exists():
        for line in env_file.read_text(encoding='utf-8').splitlines():
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip()
    return None


def generate_image(api_key, base_url, model, prompt, filename, retry=2):
    """调用 Nano Banana 生成单张图片"""
    url = f"{base_url}/models/{model}:generateContent"
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "temperature": 1.0,
        },
    }

    for attempt in range(retry + 1):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=180)

            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if not candidates:
                    print(f"    !! 无候选结果")
                    continue

                parts = candidates[0].get("content", {}).get("parts", [])
                for part in parts:
                    if "inlineData" in part:
                        img_data = base64.b64decode(part["inlineData"]["data"])
                        (OUT_DIR / filename).write_bytes(img_data)
                        print(f"    OK [{model}] {filename} ({len(img_data)//1024}KB)")
                        return True
                    elif "text" in part:
                        print(f"    文本: {part['text'][:100]}")

                print(f"    !! 响应中无图片数据")
            else:
                error_msg = resp.text[:200]
                print(f"    !! [{resp.status_code}] {error_msg}")

                # 如果是 "No available accounts"，等待后重试
                if "No available" in error_msg and attempt < retry:
                    wait = 10 * (attempt + 1)
                    print(f"    >> 等待 {wait}s 后重试...")
                    time.sleep(wait)
                    continue
                # 其他错误不重试
                break

        except requests.exceptions.Timeout:
            print(f"    !! 超时 (180s)")
            if attempt < retry:
                print(f"    >> 重试 {attempt+2}/{retry+1}...")
        except Exception as e:
            print(f"    !! 异常: {e}")
            break

    return False


def main():
    parser = argparse.ArgumentParser(description="Nano Banana 图片批量生成")
    parser.add_argument("--key", help="Gemini API Key (或设置 GEMINI_API_KEY 环境变量)")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="API 基础 URL")
    parser.add_argument("--model", help="指定模型 (默认自动尝试多个)")
    parser.add_argument("--only", help="只生成指定ID，逗号分隔 (如 G01,G02)")
    parser.add_argument("--skip-existing", action="store_true", help="跳过已存在的图片")
    parser.add_argument("--retry", type=int, default=2, help="失败重试次数")
    args = parser.parse_args()

    api_key = args.key or load_api_key()
    if not api_key:
        print("错误: 未找到 GEMINI_API_KEY")
        print("请设置环境变量或使用 --key 参数")
        return

    models = [args.model] if args.model else MODELS
    only_ids = set(args.only.split(",")) if args.only else None

    print("=" * 60)
    print("HydroClaw PPT — Nano Banana 图片生成器")
    print(f"  模型: {models}")
    print(f"  输出: {OUT_DIR}")
    print(f"  图片: {len(PROMPTS)} 张")
    print("=" * 60)

    success, skip, fail = 0, 0, 0

    for i, item in enumerate(PROMPTS):
        pid = item["id"]
        name = item["name"]
        section = item["section"]

        # 过滤
        if only_ids and pid not in only_ids:
            continue

        # 跳过已有
        if args.skip_existing and (OUT_DIR / name).exists():
            print(f"  [{i+1:02d}/{len(PROMPTS)}] {pid} {name} — 已存在，跳过")
            skip += 1
            continue

        print(f"\n  [{i+1:02d}/{len(PROMPTS)}] {pid} [{section}] {name}")

        # 尝试多个模型
        ok = False
        for model in models:
            ok = generate_image(api_key, args.base_url, model, item["prompt"], name, retry=args.retry)
            if ok:
                break
            print(f"    >> 尝试下一个模型...")

        if ok:
            success += 1
        else:
            fail += 1

    print(f"\n{'='*60}")
    print(f"完成: 成功 {success} / 跳过 {skip} / 失败 {fail} / 共 {len(PROMPTS)}")
    print(f"输出目录: {OUT_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
