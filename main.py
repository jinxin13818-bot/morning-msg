#!/usr/bin/env python3
"""早安文案 — 主入口

用法:
    uv run python main.py                    # 生成明日文案
    uv run python main.py --reroll           # 重新生成今天文案（覆盖）
    uv run python main.py --date 2026-06-09  # 生成指定日期文案
"""

import sys
import os
from datetime import date, timedelta, datetime

from calendar_utils import get_day_info
from prompt import call_llm, build_generation_prompt, humanize
from dedup import is_duplicate, save_text
from push import send_telegram
from config import MAX_GENERATION_RETRIES, OUTPUT_DIR


def write_markdown(day_info: dict, text: str) -> str:
    """
    将文案写入 Obsidian Markdown 文件。

    Returns:
        文件的绝对路径
    """
    date_str = day_info["date"].strftime("%Y-%m-%d")
    filename = f"{date_str}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    lunar = day_info["lunar_display"]
    weekday = day_info["weekday"]
    theme = day_info["theme"]["name"]
    solar_term = day_info.get("solar_term") or ""
    festival = day_info.get("festival") or ""

    content = f"""---
date: {date_str}
lunar: {lunar}
weekday: {weekday}
theme: {theme}
solar_term: {solar_term}
festival: {festival}
---

早安！今天是 {day_info['date'].year}年{day_info['date'].month}月{day_info['date'].day}日 星期{weekday}

农历{lunar}

{text}

祝你今天一切顺利！💪
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[WRITE] 文案已写入: {filepath}")
    return filepath


def generate(target_date: date) -> dict:
    """
    生成一条完整的早安文案。

    Args:
        target_date: 目标日期（明天）

    Returns:
        {"day_info": {...}, "text": "...", "filepath": "..."}
    """
    day_info = get_day_info(target_date)
    print(f"[INFO] 目标日期: {day_info['solar_date']} ({day_info['lunar_display']})")
    print(f"[INFO] 主题: {day_info['theme']['name']} ({day_info['theme']['direction']})")
    if day_info["solar_term"]:
        print(f"[INFO] 节气: {day_info['solar_term']}")
    if day_info["festival"]:
        print(f"[INFO] 节日: {day_info['festival']}")

    system_prompt = "你是一位早安文案写手。你的每条文案都是30-35秒的口播稿。风格：简短有力，像朋友发的一条早安消息。不说教，不铺陈，点到为止。每句话都要有信息量。结尾总是「祝你今天一切顺利！💪」"
    user_prompt = build_generation_prompt(day_info)

    # 生成 + 去重循环（最多 3 次）
    for attempt in range(1, MAX_GENERATION_RETRIES + 1):
        print(f"[GEN] 第 {attempt} 次生成...")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        raw_text = call_llm(messages)
        print(f"[GEN] 生成完成 ({len(raw_text)}字)")

        # Humanizer-zh 去 AI 味
        print(f"[HUMANIZE] 去 AI 味处理...")
        humanized_text = humanize(raw_text)
        print(f"[HUMANIZE] 处理完成 ({len(humanized_text)}字)")

        # 去重检查
        if is_duplicate(humanized_text):
            print(f"[DEDUP] 文案重复！尝试 {attempt}/{MAX_GENERATION_RETRIES}")
            if attempt < MAX_GENERATION_RETRIES:
                # 加随机种子后重试
                user_prompt += f"\n\n（第{attempt}次尝试，请写出一个完全不同的版本）"
                continue
            else:
                print("[DEDUP] 重试次数用尽，跳过今日")
                raise RuntimeError("去重失败：3次生成均重复")

        # 通过去重，保存
        save_text(humanized_text, day_info["solar_date"])
        print(f"[DEDUP] 去重通过 ✓")

        # 写入 Markdown
        filepath = write_markdown(day_info, humanized_text)

        # 构建 Obsidian URI
        vault_name = "🤍日記"
        relative_path = f"项目/早安文案/{day_info['date'].strftime('%Y-%m-%d')}.md"
        obsidian_uri = f"obsidian://open?vault={vault_name}&file={relative_path}"

        # Telegram 推送
        print(f"[PUSH] Telegram 推送中...")
        date_str = f"{day_info['date'].year}年{day_info['date'].month}月{day_info['date'].day}日"
        weekday = day_info["weekday"]
        lunar = day_info["lunar_display"]
        tg_text = f"""🌅 早安！今天是 {date_str} 星期{weekday}

农历{lunar}

{humanized_text}

祝你今天一切顺利！💪"""
        send_telegram(tg_text)

        return {
            "day_info": day_info,
            "text": humanized_text,
            "filepath": filepath,
        }

    raise RuntimeError("Unreachable")


def main():
    # 解析参数
    target_date = date.today() + timedelta(days=1)  # 默认：明天

    args = sys.argv[1:]
    if "--reroll" in args:
        target_date = date.today() + timedelta(days=1)
        print(f"[REROLL] 重新生成 {target_date.strftime('%Y-%m-%d')} 的文案")
    elif "--date" in args:
        idx = args.index("--date")
        if idx + 1 < len(args):
            target_date = datetime.strptime(args[idx + 1], "%Y-%m-%d").date()
            print(f"[DATE] 指定日期: {target_date}")

    try:
        result = generate(target_date)
        print(f"\n✅ 早安文案生成成功！")
        print(f"📄 {result['filepath']}")
        print(f"📝 {result['text']}")
    except Exception as e:
        print(f"\n❌ 早安文案生成失败: {e}")
        # 失败通知
        send_telegram(f"❌ 早安文案生成失败\n{str(e)[:200]}")
        sys.exit(1)


if __name__ == "__main__":
    main()
