"""
Markdown → Presenton JSON 解析器

将 Markdown 文本转换为 presenton_cli.py 中 build_slides_from_json() 所需的 JSON 格式。

输入格式示例
============

```markdown
---
title: 演示文稿标题
author: 作者名
---

# 封面标题
副标题文字

## 第一章 章节标题
章节副标题

### 内容页标题
- 要点1
- 要点2
- 要点3

> 高亮大字标题
> — 底部辅助说明

### 对比页标题
| 左栏标题 | 右栏标题 |
| 左项1 | 右项1 |
| 左项2 | 右项2 |

### 数据页标题
* 100+ :: 功能模块
* 15% :: 效率提升

![图片标题](asset:cover_dam)
图片说明文字

### 图文页标题 ![](asset:ai_brain)
- 要点1
- 要点2

### 编号列表页标题
1. 第一项
2. 第二项
3. 第三项

#### 卡片1标题
- 卡片1内容行1
- 卡片1内容行2

#### 卡片2标题
- 卡片2内容行1

#### 卡片3标题
- 卡片3内容行1
```

输出格式
========

返回 dict，结构为::

    {
        "title": "演示文稿标题",
        "slides": [
            {"type": "cover", "title": "...", "subtitle": "...", "author": "..."},
            {"type": "chapter", "chapter_num": "一", "title": "...", "subtitle": "..."},
            {"type": "content", "title": "...", "bullets": ["...", "..."]},
            {"type": "highlight", "label": "", "main_text": "...", "sub_text": "..."},
            {"type": "two_column", "title": "...", "left_title": "...",
             "left_items": [...], "right_title": "...", "right_items": [...]},
            {"type": "stats", "title": "...", "stats": [["100+", "功能模块"], ...]},
            {"type": "image", "title": "...", "image": "asset:cover_dam", "caption": "..."},
            {"type": "image_content", "title": "...", "bullets": [...], "image": "asset:..."},
            {"type": "numbered_list", "title": "...", "items": ["...", "..."]},
            {"type": "three_card", "title": "...", "cards": [["标题", ["行1", "行2"]], ...]},
        ]
    }

slide type 对应的参数签名请参考 presenton_cli.py 中的 SLIDE_TYPE_MAP 和各 *_slide() 函数。
"""

import re
import json
from typing import Dict, List, Optional, Tuple, Any


# ============================================================
# Front-matter 解析
# ============================================================

_FRONTMATTER_RE = re.compile(r"\A\s*---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _parse_frontmatter(text: str) -> Tuple[dict, str]:
    """提取 YAML-like front-matter（简易 key: value 解析，不依赖 PyYAML）。

    Returns:
        (metadata_dict, remaining_text)
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip()
    return meta, text[m.end():]


# ============================================================
# 行级工具
# ============================================================

# 匹配 ### 标题 ![alt](src) 形式（标题中嵌入图片引用）
_H3_IMAGE_RE = re.compile(
    r"^###\s+(.+?)\s*!\[([^\]]*)\]\(([^)]+)\)\s*$"
)

# 匹配独立图片行 ![title](src)
_IMAGE_LINE_RE = re.compile(
    r"^!\[([^\]]*)\]\(([^)]+)\)\s*$"
)

# 匹配 stats 行: * 100+ :: 标签
_STATS_RE = re.compile(
    r"^\*\s+(.+?)\s*::\s*(.+)$"
)

# 匹配 table 行: | col1 | col2 |  (允许没有尾部 |)
_TABLE_ROW_RE = re.compile(
    r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|?\s*$"
)

# 章节编号 "第X章" 或 "第X部分"
_CHAPTER_NUM_RE = re.compile(r"第([一二三四五六七八九十百千\d]+)[章部]")

# blockquote 归因行 — 识别 "— xxx" 或 "—— xxx"
_ATTRIBUTION_RE = re.compile(r"^[—–-]{1,2}\s*(.+)$")


def _strip_bullet(line: str) -> str:
    """去除行首的 '- ' 或 '* ' 前缀。"""
    s = line.strip()
    if s.startswith("- ") or s.startswith("* "):
        return s[2:]
    return s


def _is_separator_row(text: str) -> bool:
    """判断 table 行是否为分隔符行 (| --- | --- |)。"""
    cleaned = text.replace("|", "").replace("-", "").replace(":", "").strip()
    return cleaned == ""


# ============================================================
# 分块（按顶级标记拆分 Markdown 为 slide 块）
# ============================================================

def _split_into_blocks(text: str) -> List[dict]:
    """将 Markdown 文本按顶层标记拆分为 slide 块。

    每个块是一个 dict，至少包含 ``kind`` 和 ``lines``。

    块的切割规则：
    - ``# H1``  → 新块 (cover)
    - ``## H2`` → 新块 (chapter)
    - ``### H3`` → 新块 (content / image_content / stats / two_column / numbered_list)
    - ``#### H4`` → 积累三个后合并为 three_card 块
    - ``> blockquote`` → 新块 (highlight)
    - ``![title](image)`` 独立行 → 新块 (image)
    """
    lines = text.splitlines()
    blocks: List[dict] = []
    current: Optional[dict] = None
    h4_accumulator: List[dict] = []  # 收集连续 #### 块

    def _flush_h4():
        """将积累的 h4 块合并为 three_card 块或退化为 content 块。"""
        nonlocal h4_accumulator
        if not h4_accumulator:
            return
        if len(h4_accumulator) >= 3:
            # 每三个一组
            for start in range(0, len(h4_accumulator) - 2, 3):
                group = h4_accumulator[start:start + 3]
                blocks.append({
                    "kind": "three_card",
                    "cards": group,
                })
            remainder = len(h4_accumulator) % 3
            if remainder:
                # 剩余不足三个的退化为 content
                for h4 in h4_accumulator[-remainder:]:
                    blocks.append({
                        "kind": "content_from_h4",
                        "title": h4["title"],
                        "lines": h4["lines"],
                    })
        else:
            # 不足3个，退化
            for h4 in h4_accumulator:
                blocks.append({
                    "kind": "content_from_h4",
                    "title": h4["title"],
                    "lines": h4["lines"],
                })
        h4_accumulator = []

    def _flush_current():
        nonlocal current
        if current is not None:
            blocks.append(current)
            current = None

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # ---- H1: cover ----
        if stripped.startswith("# ") and not stripped.startswith("## "):
            _flush_h4()
            _flush_current()
            current = {"kind": "cover", "title": stripped[2:].strip(), "lines": []}
            i += 1
            continue

        # ---- H2: chapter ----
        if stripped.startswith("## ") and not stripped.startswith("### "):
            _flush_h4()
            _flush_current()
            current = {"kind": "chapter", "title": stripped[3:].strip(), "lines": []}
            i += 1
            continue

        # ---- H3 with inline image: image_content ----
        m_h3img = _H3_IMAGE_RE.match(stripped)
        if m_h3img:
            _flush_h4()
            _flush_current()
            current = {
                "kind": "image_content",
                "title": m_h3img.group(1).strip(),
                "image": m_h3img.group(3).strip(),
                "lines": [],
            }
            i += 1
            continue

        # ---- H3: content (type determined later by body content) ----
        if stripped.startswith("### ") and not stripped.startswith("#### "):
            _flush_h4()
            _flush_current()
            current = {"kind": "h3", "title": stripped[4:].strip(), "lines": []}
            i += 1
            continue

        # ---- H4: potential three_card ----
        if stripped.startswith("#### "):
            # If we were accumulating a non-h4 block, flush it
            _flush_current()
            # Start a new h4 entry
            h4_entry = {"title": stripped[5:].strip(), "lines": []}
            h4_accumulator.append(h4_entry)
            i += 1
            # Collect lines until next heading or block marker
            while i < len(lines):
                nxt = lines[i].strip()
                if nxt.startswith("#") or _IMAGE_LINE_RE.match(nxt) or nxt.startswith(">"):
                    break
                h4_entry["lines"].append(lines[i])
                i += 1
            continue

        # ---- blockquote: highlight ----
        if stripped.startswith("> "):
            _flush_h4()
            _flush_current()
            bq_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                bq_lines.append(lines[i].strip()[1:].strip())  # remove '> '
                i += 1
            blocks.append({"kind": "highlight", "lines": bq_lines})
            continue

        # ---- standalone image ----
        m_img = _IMAGE_LINE_RE.match(stripped)
        if m_img:
            _flush_h4()
            _flush_current()
            img_block = {
                "kind": "image",
                "title": m_img.group(1).strip(),
                "image": m_img.group(2).strip(),
                "lines": [],
            }
            # Next non-empty line could be a caption
            i += 1
            while i < len(lines):
                nxt = lines[i].strip()
                if not nxt:
                    i += 1
                    continue
                # If it's another block-level marker, stop
                if nxt.startswith("#") or nxt.startswith(">") or _IMAGE_LINE_RE.match(nxt):
                    break
                img_block["lines"].append(nxt)
                i += 1
                break  # only one caption line
            blocks.append(img_block)
            continue

        # ---- body line (belongs to current block) ----
        if current is not None:
            current["lines"].append(line)
        # else: stray line before any heading — ignore

        i += 1

    # Final flush
    _flush_h4()
    _flush_current()

    return blocks


# ============================================================
# 块 → slide dict 转换
# ============================================================

def _block_to_slide(block: dict, meta: dict) -> Optional[dict]:
    """将一个解析块转换为 slide dict。"""

    kind = block["kind"]

    # ------ cover ------
    if kind == "cover":
        body_lines = [l.strip() for l in block.get("lines", []) if l.strip()]
        subtitle = "\n".join(body_lines) if body_lines else ""
        slide = {"type": "cover", "title": block["title"], "subtitle": subtitle}
        if meta.get("author"):
            slide["author"] = meta["author"]
        return slide

    # ------ chapter ------
    if kind == "chapter":
        raw_title = block["title"]
        body_lines = [l.strip() for l in block.get("lines", []) if l.strip()]
        subtitle = "\n".join(body_lines) if body_lines else ""

        # 尝试提取章节编号
        m_num = _CHAPTER_NUM_RE.search(raw_title)
        if m_num:
            chapter_num = m_num.group(1)
            # 从标题中移除 "第X章 " 前缀
            cleaned = _CHAPTER_NUM_RE.sub("", raw_title).strip()
            # 也去掉可能残留的 "第X部分" 后面的空格
            cleaned = cleaned.lstrip(" ·:：—-")
            title = cleaned if cleaned else raw_title
        else:
            # 没有 "第X章" 模式：用递增数字作为 chapter_num
            chapter_num = ""
            title = raw_title

        slide: dict = {"type": "chapter", "chapter_num": chapter_num, "title": title}
        if subtitle:
            slide["subtitle"] = subtitle
        return slide

    # ------ highlight (blockquote) ------
    if kind == "highlight":
        bq_lines = block["lines"]
        main_lines: List[str] = []
        sub_text = ""
        for l in bq_lines:
            m_attr = _ATTRIBUTION_RE.match(l)
            if m_attr:
                sub_text = m_attr.group(1)
            else:
                main_lines.append(l)
        main_text = "\n".join(main_lines)
        slide = {"type": "highlight", "label": "", "main_text": main_text}
        if sub_text:
            slide["sub_text"] = sub_text
        return slide

    # ------ image (standalone) ------
    if kind == "image":
        slide = {"type": "image", "image": block["image"]}
        if block.get("title"):
            slide["title"] = block["title"]
        caption_lines = block.get("lines", [])
        if caption_lines:
            slide["caption"] = caption_lines[0].strip()
        return slide

    # ------ image_content (### title ![](image)) ------
    if kind == "image_content":
        body_lines = [l.strip() for l in block.get("lines", []) if l.strip()]
        bullets = [_strip_bullet(l) for l in body_lines if l.startswith("-") or l.startswith("*")]
        if not bullets:
            bullets = [l for l in body_lines if l]
        slide = {
            "type": "image_content",
            "title": block["title"],
            "bullets": bullets,
            "image": block["image"],
        }
        return slide

    # ------ three_card ------
    if kind == "three_card":
        cards_data = block["cards"]
        # Derive a parent title — use the text before the first card if available,
        # otherwise synthesize from card titles
        title = block.get("title", "")
        if not title:
            # No explicit title; use a generic one
            title = ""

        cards = []
        for c in cards_data[:3]:
            body = [_strip_bullet(l) for l in c["lines"] if l.strip()]
            cards.append([c["title"], body])

        slide = {"type": "three_card", "title": title, "cards": cards}
        return slide

    # ------ content_from_h4 (degraded single h4) ------
    if kind == "content_from_h4":
        bullets = [_strip_bullet(l) for l in block.get("lines", []) if l.strip()]
        return {"type": "content", "title": block["title"], "bullets": bullets}

    # ------ h3: determine sub-type from body content ------
    if kind == "h3":
        title = block["title"]
        body_lines = block.get("lines", [])
        stripped_body = [l.strip() for l in body_lines]
        non_empty = [l for l in stripped_body if l]

        if not non_empty:
            # Empty body — bare content slide
            return {"type": "content", "title": title, "bullets": []}

        # --- check for stats pattern: * num :: label ---
        stats_matches = [_STATS_RE.match(l) for l in non_empty]
        if all(m is not None for m in stats_matches) and len(non_empty) >= 1:
            stats = [[m.group(1).strip(), m.group(2).strip()] for m in stats_matches]
            return {"type": "stats", "title": title, "stats": stats}

        # --- check for table pattern ---
        table_rows = []
        is_table = False
        for l in non_empty:
            m_tr = _TABLE_ROW_RE.match(l)
            if m_tr:
                if not _is_separator_row(l):
                    table_rows.append((m_tr.group(1).strip(), m_tr.group(2).strip()))
                is_table = True
            elif is_table:
                break  # table ended

        if is_table and len(table_rows) >= 2:
            # First row = column titles
            left_title = table_rows[0][0]
            right_title = table_rows[0][1]
            left_items = [r[0] for r in table_rows[1:]]
            right_items = [r[1] for r in table_rows[1:]]
            return {
                "type": "two_column",
                "title": title,
                "left_title": left_title,
                "right_title": right_title,
                "left_items": left_items,
                "right_items": right_items,
            }

        # --- check for numbered list: 1. xxx ---
        numbered = []
        for l in non_empty:
            m_num = re.match(r"^\d+[\.\)]\s+(.+)$", l)
            if m_num:
                numbered.append(m_num.group(1))
        if len(numbered) == len(non_empty) and len(numbered) >= 2:
            return {"type": "numbered_list", "title": title, "items": numbered}

        # --- default: bullet content slide ---
        bullets = []
        for l in non_empty:
            bullets.append(_strip_bullet(l))
        return {"type": "content", "title": title, "bullets": bullets}

    return None


# ============================================================
# three_card 标题回填
# ============================================================

def _backfill_three_card_titles(slides: List[dict]) -> List[dict]:
    """如果 three_card 没有标题，尝试从前一个 h3 block 回溯获取。

    实际上，我们在块分割时已经无法获得上层标题。这里做一个简单的
    检查：如果 three_card.title 为空，就保持为空（presenton 的
    three_card_slide 会接受空标题）。
    """
    return slides


# ============================================================
# 公开 API
# ============================================================

def parse_markdown(text: str) -> dict:
    """将 Markdown 文本解析为 presenton JSON 格式的 dict。

    Args:
        text: Markdown 格式的演示文稿内容

    Returns:
        dict，包含 ``title`` (str) 和 ``slides`` (list[dict]) 两个键。
        可直接传给 ``build_slides_from_json()``。

    Example::

        >>> md = '''
        ... ---
        ... title: 我的演示
        ... author: 张三
        ... ---
        ...
        ... # 我的演示
        ... 副标题
        ...
        ... ### 内容页
        ... - 要点A
        ... - 要点B
        ... '''
        >>> result = parse_markdown(md)
        >>> result["title"]
        '我的演示'
        >>> result["slides"][0]["type"]
        'cover'
    """
    meta, body = _parse_frontmatter(text)
    blocks = _split_into_blocks(body)

    slides: List[dict] = []
    for block in blocks:
        s = _block_to_slide(block, meta)
        if s is not None:
            slides.append(s)

    slides = _backfill_three_card_titles(slides)

    # Determine presentation title
    title = meta.get("title", "")
    if not title and slides:
        # Fall back to cover slide title
        for s in slides:
            if s.get("type") == "cover":
                title = s.get("title", "")
                break
    if not title:
        title = "Presentation"

    return {"title": title, "slides": slides}


def parse_markdown_file(path: str) -> dict:
    """从文件读取 Markdown 并解析为 presenton JSON 格式。

    Args:
        path: Markdown 文件的路径（支持 UTF-8 编码）

    Returns:
        dict，同 :func:`parse_markdown` 的返回值。

    Raises:
        FileNotFoundError: 文件不存在
        UnicodeDecodeError: 文件编码不是 UTF-8
    """
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return parse_markdown(text)


# ============================================================
# CLI — 可独立运行进行测试
# ============================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python markdown_parser.py <input.md> [output.json]")
        print("      python markdown_parser.py --test   # 运行内置测试")
        sys.exit(1)

    if sys.argv[1] == "--test":
        sample = r"""---
title: 测试演示
author: 测试者
---

# 测试演示
这是副标题

## 第一章 引言
章节说明

### 内容页
- 要点1
- 要点2
- 要点3

> 这是高亮强调页的大字文本
> — 底部辅助说明

### 对比页
| 左栏标题 | 右栏标题 |
| --- | --- |
| 左项1 | 右项1 |
| 左项2 | 右项2 |

### 数据页
* 100+ :: 功能模块
* 15% :: 效率提升
* 99.9% :: 可用性

![科技水坝](asset:cover_dam)
图片说明文字

### 图文页 ![](asset:ai_brain)
- 要点带图片
- 另一个要点

### 编号列表
1. 第一项
2. 第二项
3. 第三项

#### 卡片1
- 内容A1
- 内容A2

#### 卡片2
- 内容B1
- 内容B2

#### 卡片3
- 内容C1
- 内容C2
"""
        result = parse_markdown(sample)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"\n--- 共 {len(result['slides'])} 张幻灯片 ---")
        for i, s in enumerate(result["slides"]):
            print(f"  [{i}] {s['type']:16s} | {s.get('title', s.get('main_text', ''))[:40]}")
    else:
        result = parse_markdown_file(sys.argv[1])
        output = sys.argv[2] if len(sys.argv) > 2 else None
        if output:
            with open(output, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"Saved to {output}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
