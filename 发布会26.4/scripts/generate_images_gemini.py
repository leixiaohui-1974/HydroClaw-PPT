"""
使用Gemini 3 Pro生成PPT配图
API配置从 d:/cowork/个人/aicode.env 读取
"""
import os
import sys

# 设置UTF-8编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# 加载API配置
env_path = Path(r"d:\cowork\个人\aicode.env")
load_dotenv(env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_BASE_URL = os.getenv("OPENCLAW_GEMINI_BASE_URL", "https://aicode.cat/v1beta")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-pro-preview")

print(f"API Key: {GEMINI_API_KEY[:20]}...")
print(f"Base URL: {GEMINI_BASE_URL}")
print(f"Model: {GEMINI_MODEL}")

# 创建输出目录
output_dir = Path("generated_images")
output_dir.mkdir(exist_ok=True)

# 图片生成提示词（针对Gemini优化）
image_prompts = {
    "cover_bg": {
        "prompt": """Generate a professional presentation cover background image.

Theme: Intelligent Water Network System with AI Integration
Style: Modern, technology-inspired, professional
Color Scheme: Deep blue (#1F497D) gradient to medium blue (#44546A)
Elements:
- Abstract flowing water patterns
- Neural network connection lines
- Smart infrastructure silhouettes (dams, pipes, sensors)
- Subtle grid or circuit board patterns
- Glowing nodes representing AI decision points

Composition:
- Clean, uncluttered design
- Suitable for text overlay
- Professional corporate style
- High contrast for readability

Technical Requirements:
- Resolution: 1920x1080
- Format: PNG with transparency where appropriate
- No text or labels
- Landscape orientation""",
        "filename": "cover_background.png"
    },

    "architecture_diagram": {
        "prompt": """Generate a 4-layer architecture diagram in 3D pyramid style.

Layers (bottom to top):
1. OBJECT LAYER (Yellow #FFC000): Component library icons
2. ENGINE LAYER (Green #70AD47): 7 engine icons in a row
3. SKILL LAYER (Orange #ED7D31): Skill orchestration symbols
4. COGNITIVE LAYER (Blue #5B9BD5): AI brain and rule engine icons

Style:
- Isometric 3D pyramid view
- Each layer clearly separated with depth
- Clean, professional design
- Icons representing each layer's function
- Arrows showing data flow between layers

Technical:
- Resolution: 1600x1200
- White or light gray background
- Clear layer labels
- Professional infographic style""",
        "filename": "architecture_pyramid.png"
    },

    "cognitive_decision": {
        "prompt": """Generate a flowchart diagram showing AI cognitive decision process.

Flow:
User Input → Intent Recognition → Rule Matching → [Split into two paths]
Path 1 (Blue): Large Language Model (for uncertainty)
Path 2 (Orange): Rule Engine (for certainty)
Both paths → Skill Selection → Engine Invocation → Result Packaging → Output

Style:
- Professional flowchart with rounded rectangles
- Clear directional arrows
- Two-color scheme: Blue (#5B9BD5) for LLM, Orange (#ED7D31) for Rules
- Clean, modern design
- Icons for each step

Technical:
- Resolution: 1400x800
- White background
- Clear labels in English and Chinese
- Suitable for presentation""",
        "filename": "cognitive_flow_diagram.png"
    },

    "seven_engines": {
        "prompt": """Generate 7 minimalist circular icons for computation engines.

Icons needed:
1. Prediction Engine: Crystal ball or forecast chart (Blue #5B9BD5)
2. Optimization Engine: Target with arrow hitting bullseye (Orange #ED7D31)
3. Simulation Engine: Play button or rotating gears (Green #70AD47)
4. Learning Engine: Brain with neural connections (Yellow #FFC000)
5. Validation Engine: Shield with checkmark (Blue #5B9BD5)
6. Visualization Engine: Eye or bar chart (Orange #ED7D31)
7. Collaboration Engine: Connected network nodes (Green #70AD47)

Style:
- Flat design, minimalist
- Each icon in a circle with colored background
- Consistent line weight and style
- Professional, modern look
- Arranged in a grid (3 top, 4 bottom)

Technical:
- Resolution: 1400x800
- White background
- Each icon 200x200 pixels
- Clear spacing between icons""",
        "filename": "seven_engines_icons.png"
    },

    "component_library": {
        "prompt": """Generate a component library diagram showing 3 categories.

Categories:
1. Physical Components (Blue #5B9BD5):
   - Reservoir, River, Gate, Pump Station, Pipeline, Valve

2. Hydrological Components (Orange #ED7D31):
   - Rainfall, Evaporation, Runoff Generation, Flow Routing, Groundwater

3. Model Components (Green #70AD47):
   - Hydrodynamics, Water Quality, Ecology, Economics

Style:
- Tree structure or grouped boxes
- Simple icon for each component
- Color-coded by category
- Clean, organized layout
- Professional infographic style

Technical:
- Resolution: 1400x1000
- White or light gray background
- Clear category labels
- Suitable for presentation""",
        "filename": "component_library_diagram.png"
    },

    "runtime_sequence": {
        "prompt": """Generate a sequence diagram showing system execution flow.

Sequence:
User → Cognitive Layer → Skill Layer → Engine Layer → Object Layer → Result

Example flow: "Optimize river cross-section"
1. User inputs request
2. Cognitive layer: Intent recognition + Rule matching
3. Skill layer: Select "Cross-section Optimization" skill
4. Engine layer: Call optimization + simulation engines
5. Object layer: Read/update river component parameters
6. Return: Optimized parameters + 3D visualization + Report

Style:
- UML-style sequence diagram
- Vertical swimlanes for each layer
- Horizontal arrows for messages
- Color-coded layers (Blue, Orange, Green, Yellow)
- Clean, professional design

Technical:
- Resolution: 1400x1000
- White background
- Clear labels and annotations
- Suitable for presentation""",
        "filename": "runtime_sequence_diagram.png"
    },

    "design_roadmap": {
        "prompt": """Generate a 3-phase roadmap timeline diagram.

Phases:
Phase 1 (Blue #5B9BD5): Single-Point Tools
- Pump station selection
- Pipeline calculation
- Cross-section optimization
- Value: Replace Excel and empirical formulas

Phase 2 (Orange #ED7D31): MBD Validation
- Digital twin system
- Full system validation
- Detect design flaws
- Value: Reduce rework by 50%

Phase 3 (Green #70AD47): Full Automation
- Automated design generation
- From concept to construction drawings
- Value: 10x efficiency improvement

Style:
- Horizontal timeline with milestones
- Each phase in a rounded rectangle
- Icons representing key features
- Arrows showing progression
- Professional roadmap style

Technical:
- Resolution: 1600x800
- White or light gradient background
- Clear phase labels
- Suitable for presentation""",
        "filename": "design_roadmap_timeline.png"
    },

    "digital_twin": {
        "prompt": """Generate a 3D isometric view of an intelligent water network system.

Elements:
- Large reservoir with dam
- Winding river with multiple sections
- 2-3 pump stations with buildings
- Pipeline network (above and underground)
- Control center building with screens
- Sensors and monitoring points (glowing)
- Data flow visualization (light streams)

Style:
- Isometric 3D view (30-degree angle)
- Semi-realistic with tech elements
- Blue water, green landscape, gray infrastructure
- Glowing tech elements (sensors, data flows)
- Smart city / IoT aesthetic
- Professional, futuristic look

Colors:
- Water: Blue (#5B9BD5)
- Landscape: Green (#70AD47)
- Infrastructure: Gray with blue accents
- Tech elements: Glowing cyan/blue
- Background: Light blue to white gradient

Technical:
- Resolution: 1920x1080
- Landscape orientation
- High detail, professional quality
- Suitable for presentation cover or key visual""",
        "filename": "digital_twin_scene.png"
    }
}

def generate_image_with_gemini(prompt, filename):
    """使用Gemini API生成图片"""
    print(f"\n{'='*60}")
    print(f"生成图片: {filename}")
    print(f"{'='*60}")

    try:
        # 构建API请求
        url = f"{GEMINI_BASE_URL}/models/{GEMINI_MODEL}:generateContent"

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }

        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Generate an image based on this description:\n\n{prompt}\n\nPlease create a high-quality, professional image suitable for a business presentation."
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 2048,
            }
        }

        print(f"请求URL: {url}")
        print(f"提示词长度: {len(prompt)} 字符")

        response = requests.post(url, headers=headers, json=payload, timeout=60)

        if response.status_code == 200:
            result = response.json()

            # 保存响应到文件
            json_file = output_dir / f"{filename}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"[OK] 响应已保存: {json_file}")

            # 提取文本描述
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0].get('content', {})
                parts = content.get('parts', [])
                if parts:
                    text = parts[0].get('text', '')

                    # 保存描述
                    desc_file = output_dir / f"{filename}.txt"
                    with open(desc_file, 'w', encoding='utf-8') as f:
                        f.write(f"原始提示词:\n{prompt}\n\n")
                        f.write(f"{'='*60}\n\n")
                        f.write(f"Gemini响应:\n{text}\n")

                    print(f"[OK] 描述已保存: {desc_file}")
                    print(f"\n响应预览:\n{text[:300]}...")

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
    print("PPT配图生成工具 - Gemini 3 Pro")
    print("="*60)
    print(f"输出目录: {output_dir.absolute()}\n")

    results = {}
    success_count = 0

    for i, (key, config) in enumerate(image_prompts.items(), 1):
        print(f"\n[{i}/{len(image_prompts)}] 处理: {key}")
        result = generate_image_with_gemini(
            config["prompt"],
            config["filename"]
        )
        results[key] = result
        if result:
            success_count += 1

    print("\n" + "="*60)
    print(f"完成！成功生成 {success_count}/{len(image_prompts)} 个图片描述")
    print(f"输出目录: {output_dir.absolute()}")
    print("="*60)

    # 生成汇总报告
    report_file = output_dir / "generation_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# PPT配图生成报告\n\n")
        f.write(f"生成时间: {Path(__file__).stat().st_mtime}\n\n")
        f.write(f"成功: {success_count}/{len(image_prompts)}\n\n")
        f.write("---\n\n")

        for key, config in image_prompts.items():
            f.write(f"## {config['filename']}\n\n")
            f.write(f"**状态:** {'[OK] 成功' if results[key] else '[FAIL] 失败'}\n\n")
            f.write(f"**原始提示词:**\n```\n{config['prompt']}\n```\n\n")
            if results[key]:
                f.write(f"**生成描述:**\n{results[key]}\n\n")
            f.write("---\n\n")

    print(f"\n汇总报告: {report_file}")

if __name__ == "__main__":
    main()
