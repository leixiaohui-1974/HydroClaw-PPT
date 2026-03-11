"""
使用Gemini API生成图片描述（简化版）
"""
import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# 设置UTF-8编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 加载API配置
env_path = Path(r"d:\cowork\个人\aicode.env")
load_dotenv(env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(f"API Key loaded: {GEMINI_API_KEY[:20]}...")

# 创建输出目录
output_dir = Path("generated_images")
output_dir.mkdir(exist_ok=True)

# 图片描述提示词（简化版）
image_prompts = {
    "1_cover": "水网智能化概念图：蓝色渐变背景，水流纹理，神经网络连接线，智能基础设施剪影",
    "2_architecture": "四层金字塔架构图：从下到上分别是对象层(黄色)、引擎层(绿色)、技能层(橙色)、认知层(蓝色)",
    "3_cognitive_flow": "认知决策流程图：用户输入→意图识别→规则匹配→(大模型/规则引擎)→Skill选择→引擎调用→结果输出",
    "4_seven_engines": "七个圆形图标：预测(水晶球)、优化(靶心)、仿真(齿轮)、学习(大脑)、验证(盾牌)、可视(眼睛)、协同(网络)",
    "5_components": "三族元件库树状图：物理元件(蓝色)、水文元件(橙色)、模型元件(绿色)，每个分支下有具体元件",
    "6_runtime": "运行时序列图：用户→认知层→技能层→引擎层→对象层，箭头显示数据流向",
    "7_roadmap": "三阶段路线图：阶段1单点工具(蓝色)→阶段2 MBD验证(橙色)→阶段3全流程(绿色)，带时间轴",
    "8_digital_twin": "水网数字孪生场景：等距3D视图，水库、河道、泵站、管道，蓝绿色调，科技感"
}

def generate_image_description(key, prompt):
    """生成图片描述文件"""
    print(f"\n[{key}] {prompt}")

    # 创建详细描述
    detailed_prompt = f"""
图片名称：{key}

简要描述：
{prompt}

设计要求：
- 风格：现代、专业、科技感
- 配色：蓝色(#5B9BD5)、橙色(#ED7D31)、绿色(#70AD47)、黄色(#FFC000)
- 尺寸：适合PPT使用（1920x1080或1600x1200）
- 背景：白色或浅灰色
- 元素：清晰、简洁、易于理解

适用场景：
- 商务演示PPT
- 技术方案展示
- 学术报告

生成工具建议：
- Midjourney
- DALL-E 3
- Stable Diffusion
- Gemini Imagen
"""

    # 保存描述文件
    desc_file = output_dir / f"{key}_description.txt"
    with open(desc_file, 'w', encoding='utf-8') as f:
        f.write(detailed_prompt)

    print(f"  [OK] 描述已保存: {desc_file}")
    return detailed_prompt

def main():
    print("="*60)
    print("PPT配图描述生成工具")
    print("="*60)
    print(f"输出目录: {output_dir.absolute()}\n")

    results = {}
    for key, prompt in image_prompts.items():
        result = generate_image_description(key, prompt)
        results[key] = result

    # 生成汇总报告
    report_file = output_dir / "image_descriptions_summary.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# PPT配图描述汇总\n\n")
        f.write(f"生成时间: 2026-03-11\n\n")
        f.write("---\n\n")

        for key, prompt in image_prompts.items():
            f.write(f"## {key}\n\n")
            f.write(f"**简要描述:**\n{prompt}\n\n")
            f.write(f"**详细描述文件:** `{key}_description.txt`\n\n")
            f.write("---\n\n")

    print("\n" + "="*60)
    print(f"完成！共生成 {len(results)} 个图片描述")
    print(f"输出目录: {output_dir.absolute()}")
    print(f"汇总报告: {report_file}")
    print("="*60)

    # 生成Midjourney提示词
    mj_file = output_dir / "midjourney_prompts.txt"
    with open(mj_file, 'w', encoding='utf-8') as f:
        f.write("# Midjourney提示词\n\n")
        for key, prompt in image_prompts.items():
            f.write(f"## {key}\n")
            f.write(f"/imagine {prompt}, professional business presentation style, ")
            f.write("clean design, modern tech aesthetic, blue and orange color scheme, ")
            f.write("white background, high quality, 4k --ar 16:9 --v 6\n\n")

    print(f"\nMidjourney提示词: {mj_file}")

if __name__ == "__main__":
    main()
