"""
使用Gemini生成详细的图片描述，然后可以用于其他AI绘图工具
"""
import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
import requests

# 设置UTF-8编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 加载API配置
env_path = Path(r"d:\cowork\个人\aicode.env")
load_dotenv(env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-pro-preview")  # 使用配置文件中的模型

print(f"API Key: {GEMINI_API_KEY[:20]}...")
print(f"Model: {GEMINI_MODEL}")

# 创建输出目录
output_dir = Path("generated_images")
output_dir.mkdir(exist_ok=True)

# 图片需求
image_requirements = {
    "1_cover_bg": "水网智能化概念图：蓝色渐变背景，水流纹理，神经网络连接线，智能基础设施剪影",
    "2_architecture": "四层金字塔架构图：从下到上分别是对象层(黄色)、引擎层(绿色)、技能层(橙色)、认知层(蓝色)",
    "3_cognitive_flow": "认知决策流程图：用户输入→意图识别→规则匹配→(大模型/规则引擎)→Skill选择→引擎调用→结果输出",
    "4_seven_engines": "七个圆形图标：预测(水晶球)、优化(靶心)、仿真(齿轮)、学习(大脑)、验证(盾牌)、可视(眼睛)、协同(网络)",
    "5_components": "三族元件库树状图：物理元件(蓝色)、水文元件(橙色)、模型元件(绿色)，每个分支下有具体元件",
    "6_runtime": "运行时序列图：用户→认知层→技能层→引擎层→对象层，箭头显示数据流向",
    "7_roadmap": "三阶段路线图：阶段1单点工具(蓝色)→阶段2 MBD验证(橙色)→阶段3全流程(绿色)，带时间轴",
    "8_digital_twin": "水网数字孪生场景：等距3D视图，水库、河道、泵站、管道，蓝绿色调，科技感"
}

def generate_detailed_description(key, requirement):
    """使用Gemini生成详细的图片描述"""
    print(f"\n{'='*60}")
    print(f"[{key}] {requirement}")
    print(f"{'='*60}")

    try:
        # 使用aicode.cat代理端点
        url = f"https://aicode.cat/v1beta/models/{GEMINI_MODEL}:generateContent"

        prompt = f"""请为以下PPT配图需求生成详细的AI绘图提示词：

需求：{requirement}

请生成：
1. 英文Midjourney提示词（详细、专业）
2. 英文DALL-E提示词（清晰、具体）
3. 中文详细描述（用于人工绘制参考）

要求：
- 风格：现代、专业、科技感、商务演示风格
- 配色：蓝色(#5B9BD5)、橙色(#ED7D31)、绿色(#70AD47)、黄色(#FFC000)
- 背景：白色或浅灰色
- 尺寸：16:9比例，适合PPT使用
- 元素：清晰、简洁、易于理解

请按以下格式输出：

## Midjourney提示词
[英文提示词]

## DALL-E提示词
[英文提示词]

## 中文详细描述
[中文描述]

## 设计要点
[关键设计要素]
"""

        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 2048,
            }
        }

        print("正在调用Gemini API...")

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": GEMINI_API_KEY
            },
            json=payload,
            timeout=60,
            verify=False
        )

        if response.status_code == 200:
            result = response.json()

            # 提取生成的文本
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    text = candidate['content']['parts'][0]['text']

                    # 保存详细描述
                    desc_file = output_dir / f"{key}_detailed.md"
                    with open(desc_file, 'w', encoding='utf-8') as f:
                        f.write(f"# {key}\n\n")
                        f.write(f"## 原始需求\n{requirement}\n\n")
                        f.write("---\n\n")
                        f.write(text)

                    print(f"[OK] 详细描述已保存: {desc_file}")
                    print(f"\n预览:\n{text[:300]}...\n")

                    return text

            print("[WARN] 未找到有效内容")
            return None

        else:
            print(f"[ERROR] API请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None

    except Exception as e:
        print(f"[ERROR] 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("\n" + "="*60)
    print("PPT配图详细描述生成工具 - Gemini 2.0 Flash")
    print("="*60)
    print(f"输出目录: {output_dir.absolute()}\n")

    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    results = {}
    success_count = 0

    for i, (key, requirement) in enumerate(image_requirements.items(), 1):
        print(f"\n[{i}/{len(image_requirements)}] 处理: {key}")
        result = generate_detailed_description(key, requirement)
        results[key] = result
        if result:
            success_count += 1

    print("\n" + "="*60)
    print(f"完成！成功生成 {success_count}/{len(image_requirements)} 个详细描述")
    print(f"输出目录: {output_dir.absolute()}")
    print("="*60)

    # 生成汇总报告
    report_file = output_dir / "detailed_descriptions_summary.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# PPT配图详细描述汇总\n\n")
        f.write(f"生成时间: 2026-03-11\n")
        f.write(f"使用模型: {GEMINI_MODEL}\n\n")
        f.write(f"成功: {success_count}/{len(image_requirements)}\n\n")
        f.write("---\n\n")

        for key, requirement in image_requirements.items():
            f.write(f"## {key}\n\n")
            f.write(f"**原始需求:** {requirement}\n\n")
            f.write(f"**状态:** {'[OK] 成功' if results[key] else '[FAIL] 失败'}\n\n")
            f.write(f"**详细描述文件:** `{key}_detailed.md`\n\n")
            f.write("---\n\n")

    print(f"\n汇总报告: {report_file}")

    # 提取所有Midjourney提示词
    mj_prompts_file = output_dir / "all_midjourney_prompts.txt"
    with open(mj_prompts_file, 'w', encoding='utf-8') as f:
        f.write("# 所有Midjourney提示词\n\n")
        for key in image_requirements.keys():
            desc_file = output_dir / f"{key}_detailed.md"
            if desc_file.exists():
                content = desc_file.read_text(encoding='utf-8')
                # 提取Midjourney部分
                if "## Midjourney提示词" in content:
                    start = content.find("## Midjourney提示词")
                    end = content.find("##", start + 1)
                    if end == -1:
                        end = len(content)
                    mj_section = content[start:end].strip()
                    f.write(f"\n## {key}\n")
                    f.write(mj_section + "\n\n")
                    f.write("---\n")

    print(f"Midjourney提示词汇总: {mj_prompts_file}")

if __name__ == "__main__":
    main()
