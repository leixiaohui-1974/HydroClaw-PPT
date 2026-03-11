"""
使用Google Imagen 3 (Nano Banana 3) 生成PPT配图
API配置从 d:\cowork\个人\aicode.env 读取
"""
import os
import sys
import json
import base64
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
GEMINI_BASE_URL = os.getenv("OPENCLAW_GEMINI_BASE_URL", "https://aicode.cat/v1beta")

print(f"API Key: {GEMINI_API_KEY[:20]}...")
print(f"Base URL: {GEMINI_BASE_URL}")

# 创建输出目录
output_dir = Path("generated_images")
output_dir.mkdir(exist_ok=True)

# 图片生成提示词（针对Imagen 3优化）
image_prompts = {
    "1_cover_bg": {
        "prompt": """A professional technology background for presentation cover.
Modern intelligent water network system concept.
Deep blue gradient background (#1F497D to #44546A).
Abstract flowing water patterns with neural network connection lines.
Smart infrastructure silhouettes (dams, pipes, sensors).
Clean, professional, suitable for text overlay.
High contrast, corporate style.
16:9 aspect ratio, 1920x1080.""",
        "filename": "cover_background.png"
    },

    "2_architecture_pyramid": {
        "prompt": """A 4-layer architecture pyramid diagram in isometric 3D style.
From bottom to top:
- Layer 4 (Yellow #FFC000): Object Layer with component icons
- Layer 3 (Green #70AD47): Engine Layer with 7 engine symbols
- Layer 2 (Orange #ED7D31): Skill Layer with orchestration symbols
- Layer 1 (Blue #5B9BD5): Cognitive Layer with AI brain icon
Each layer clearly separated with depth and shadows.
Clean professional infographic style.
White background, clear labels.
16:9 aspect ratio.""",
        "filename": "architecture_pyramid.png"
    },

    "3_cognitive_flow": {
        "prompt": """A professional flowchart showing AI cognitive decision process.
Flow: User Input → Intent Recognition → Rule Matching → (split into two paths)
Path 1 (Blue): Large Language Model for uncertainty
Path 2 (Orange): Rule Engine for certainty
Both paths merge → Skill Selection → Engine Invocation → Result Packaging → Output
Modern flowchart with rounded rectangles and directional arrows.
Blue (#5B9BD5) and Orange (#ED7D31) color scheme.
White background, clean design.
16:9 aspect ratio.""",
        "filename": "cognitive_flow.png"
    },

    "4_seven_engines": {
        "prompt": """Seven minimalist circular icons for computation engines arranged in a grid.
Icons:
1. Prediction Engine: crystal ball (Blue #5B9BD5)
2. Optimization Engine: target with arrow (Orange #ED7D31)
3. Simulation Engine: rotating gears (Green #70AD47)
4. Learning Engine: brain with neural connections (Yellow #FFC000)
5. Validation Engine: shield with checkmark (Blue #5B9BD5)
6. Visualization Engine: eye symbol (Orange #ED7D31)
7. Collaboration Engine: connected network nodes (Green #70AD47)
Flat design, consistent style, circular backgrounds.
White background, professional look.
16:9 aspect ratio.""",
        "filename": "seven_engines.png"
    },

    "5_component_library": {
        "prompt": """A component library diagram showing 3 categories in tree structure.
Category 1 (Blue #5B9BD5): Physical Components
- Reservoir, River, Gate, Pump Station, Pipeline, Valve
Category 2 (Orange #ED7D31): Hydrological Components
- Rainfall, Evaporation, Runoff, Flow Routing, Groundwater
Category 3 (Green #70AD47): Model Components
- Hydrodynamics, Water Quality, Ecology, Economics
Each component with a simple icon.
Clean organized layout, professional infographic style.
White background.
16:9 aspect ratio.""",
        "filename": "component_library.png"
    },

    "6_runtime_sequence": {
        "prompt": """A UML-style sequence diagram showing system execution flow.
Vertical swimlanes for: User, Cognitive Layer, Skill Layer, Engine Layer, Object Layer
Horizontal arrows showing message flow for "Optimize river cross-section" example.
Color-coded layers: Blue, Orange, Green, Yellow.
Clean professional design with clear labels.
White background.
16:9 aspect ratio.""",
        "filename": "runtime_sequence.png"
    },

    "7_design_roadmap": {
        "prompt": """A 3-phase roadmap timeline diagram.
Phase 1 (Blue #5B9BD5): Single-Point Tools
- Pump selection, Pipeline calculation, Cross-section optimization
- Value: Replace Excel
Phase 2 (Orange #ED7D31): MBD Validation
- Digital twin system, Full system validation
- Value: Reduce rework by 50%
Phase 3 (Green #70AD47): Full Automation
- Automated design generation
- Value: 10x efficiency improvement
Horizontal timeline with milestones and arrows.
Professional roadmap style, white background.
16:9 aspect ratio.""",
        "filename": "design_roadmap.png"
    },

    "8_digital_twin": {
        "prompt": """An isometric 3D view of intelligent water network system.
Elements: Large reservoir with dam, winding river, 2-3 pump stations, pipeline network, control center.
Sensors and monitoring points with glowing effects.
Data flow visualization with light streams.
Semi-realistic with tech elements.
Blue water (#5B9BD5), green landscape (#70AD47), gray infrastructure.
Glowing cyan/blue tech elements.
Smart city / IoT aesthetic, professional futuristic look.
Light blue to white gradient background.
16:9 aspect ratio, 1920x1080.""",
        "filename": "digital_twin_scene.png"
    }
}

def generate_image_with_imagen(prompt, filename):
    """使用Google Imagen 3生成图片"""
    print(f"\n{'='*60}")
    print(f"生成图片: {filename}")
    print(f"{'='*60}")

    try:
        # 使用Gemini API的图片生成端点
        # 注意：实际的Imagen API端点可能需要调整
        url = f"{GEMINI_BASE_URL}/models/imagen-3.0-generate-001:predict"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GEMINI_API_KEY}"
        }

        payload = {
            "instances": [{
                "prompt": prompt
            }],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": "16:9",
                "safetyFilterLevel": "block_few",
                "personGeneration": "allow_adult"
            }
        }

        print(f"请求URL: {url}")
        print(f"提示词: {prompt[:100]}...")

        # 禁用SSL验证（如果需要）
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=120,
            verify=False  # 禁用SSL验证
        )

        if response.status_code == 200:
            result = response.json()

            # 保存响应
            json_file = output_dir / f"{filename}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"[OK] 响应已保存: {json_file}")

            # 提取图片数据
            if 'predictions' in result and len(result['predictions']) > 0:
                prediction = result['predictions'][0]

                # 如果返回base64编码的图片
                if 'bytesBase64Encoded' in prediction:
                    image_data = base64.b64decode(prediction['bytesBase64Encoded'])

                    # 保存图片
                    image_file = output_dir / filename
                    with open(image_file, 'wb') as f:
                        f.write(image_data)

                    print(f"[OK] 图片已保存: {image_file}")
                    return True

                # 如果返回URL
                elif 'imageUrl' in prediction:
                    image_url = prediction['imageUrl']
                    print(f"[OK] 图片URL: {image_url}")

                    # 下载图片
                    img_response = requests.get(image_url, verify=False)
                    if img_response.status_code == 200:
                        image_file = output_dir / filename
                        with open(image_file, 'wb') as f:
                            f.write(img_response.content)
                        print(f"[OK] 图片已下载: {image_file}")
                        return True

            print("[WARN] 未找到图片数据")
            return False

        else:
            print(f"[ERROR] API请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")

            # 保存提示词到文件
            prompt_file = output_dir / f"{filename}.prompt.txt"
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(f"Filename: {filename}\n\n")
                f.write(f"Prompt:\n{prompt}\n\n")
                f.write(f"Error: {response.status_code}\n")
                f.write(f"Response: {response.text}\n")

            print(f"[OK] 提示词已保存: {prompt_file}")
            return False

    except Exception as e:
        print(f"[ERROR] 生成失败: {e}")
        import traceback
        traceback.print_exc()

        # 保存提示词
        prompt_file = output_dir / f"{filename}.prompt.txt"
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(f"Filename: {filename}\n\n")
            f.write(f"Prompt:\n{prompt}\n\n")
            f.write(f"Error: {str(e)}\n")

        return False

def main():
    print("\n" + "="*60)
    print("PPT配图生成工具 - Google Imagen 3 (Nano Banana 3)")
    print("="*60)

    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    user_prompt = "A futuristic water network digital twin with holographic displays, blue tech style."
    user_filename = "test_img.png"
    
    # 确保 output_dir 是相对于工作目录的绝对路径，或者直接使用绝对路径
    global output_dir 
    output_dir = Path("D:/cowork/ppt/发布会26.4/images/generated")
    output_dir.mkdir(exist_ok=True) # 确保目录存在

    print(f"输出目录: {output_dir.absolute()}\n")

    result = generate_image_with_imagen(user_prompt, user_filename)

    print("\n" + "="*60)
    if result:
        print(f"完成！成功生成 1/1 张图片")
    else:
        print(f"失败！生成 0/1 张图片")
    print(f"输出目录: {output_dir.absolute()}")
    print("="*60)


if __name__ == "__main__":
    main()
