"""Prompt 构建 + DeepSeek API 调用 + Humanizer-zh 去 AI 味"""

import json
import requests
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL


def call_deepseek(messages: list[dict], temperature: float = 0.85, max_tokens: int = 400) -> str:
    """调用 DeepSeek API，返回生成的文本"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    resp = requests.post(
        f"{DEEPSEEK_BASE_URL}/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()


def build_generation_prompt(day_info: dict) -> str:
    """构建早安文案生成的 user prompt"""
    theme = day_info["theme"]
    lunar = day_info["lunar_display"]
    weekday = day_info["weekday"]
    solar_term = day_info.get("solar_term")
    festival = day_info.get("festival")

    # 日期描述
    solar_month = day_info["date"].month
    date_desc = f"{day_info['solar_date']}（公历{solar_month}月），星期{weekday}，农历{lunar}"
    if solar_term:
        date_desc += f"，节气：{solar_term}"
    if festival:
        date_desc += f"，节日：{festival}"

    return f"""日期背景：{date_desc}。今日主题：{theme["name"]}（{theme["direction"]}）。

请写一条早安口播文案，要求：

1. 围绕「{theme["name"]}」主题，像朋友发早安消息一样自然
2. 如果有节气或节日，自然融入
3. 每句话简短有力，不要超过25字
4. 正文严格控制在90-110字，这是硬性要求
5. 说一个道理就够，点到为止
6. 正文不要出现「早安」二字——标题已经说过早安了
7. 不要用「今天是X月X日」「星期X」「农历X」等开头——日期信息会另外展示
8. 【重要】农历月份名（如"四月"）不等于公历月份，现在是公历{solar_month}月，不要用农历月份名来判断季节或写风景
9. 【重要】不要写任何形式的祝福语结尾，不要用emoji——这些会由模板统一添加
10. 只输出正文，不加署名、前缀、后缀"""


# Humanizer-zh 系统提示词（提取自 op7418/Humanizer-zh 的 24 条 AI 痕迹检测规则）
HUMANIZER_SYSTEM_PROMPT = """你是一位中文文案润色专家。你的任务是把 AI 生成的文案改写得更像真人写的。

请严格遵循以下规则重写文案：

## 内容层面
1. 删除所有"在这个快节奏的时代"、"现代社会"、"当今社会"等泛泛的宏大叙事
2. 把抽象概念替换为具体的、可感知的场景或细节
3. 删除任何"让我们"、"让我们一起"、"愿我们"等集体呼吁句式
4. 不要总结、不要升华、不要上价值——点到为止

## 语言层面
5. 删除"不仅...而且..."、"既...又..."等关联词堆砌
6. 删除"总之"、"总而言之"、"综上所述"等总结词
7. 把"犹如"、"宛若"、"仿佛"等书面比喻词改成更口语的表达
8. 删除"人生的真谛"、"生命的意义"、"灵魂"等大词
9. 避免连续使用三个以上的"的"字短语
10. 把"日益"、"愈发"、"越来越"等渐变词改成更直接的表达
11. 删除"毋庸置疑"、"毫无疑问"、"众所周知"等绝对化副词

## 风格层面
12. 句子长度要错落：长句不超过25字，穿插5-10字的短句
13. 用口语化表达替换书面语：比如"做自己"不用"成为更好的自己"
14. 允许适当的不完美：可以有一两句不太工整但很真实的表达
15. 避免排比句——真人很少用排比
16. 删除鸡汤味浓的词：如"拥抱"、"遇见更好的自己"、"温柔以待"
17. 不要用分号连接句子——真人写作很少用分号

## 沟通层面
18. 像朋友聊天一样写，不要像老师讲课
19. 可以适当加入个人感受或小故事片段
20. 避免命令式的祈使句（"你要..."、"你必须..."）
21. 可以用"我"开头，用第一人称拉近距离
22. 允许有点小情绪：可以有点无奈、有点自嘲、有点小确幸

## 输出要求
23. 重写后字数严格控制在80-110字
24. 原文已经足够简洁的就保留，不要为了改写而改写
25. 不要输出任何祝福语结尾（「祝你…」「愿你…」「希望你…」等），不要用emoji
26. 只输出最终文案，不要加任何解释、标注或前缀"""


def humanize(original_text: str) -> str:
    """调用 DeepSeek 对文案进行去 AI 味处理"""
    messages = [
        {"role": "system", "content": HUMANIZER_SYSTEM_PROMPT},
        {"role": "user", "content": f"请重写以下文案：\n\n{original_text}"},
    ]
    return call_deepseek(messages, temperature=0.9, max_tokens=400)


if __name__ == "__main__":
    # 测试：生成一条
    from calendar_utils import get_day_info
    from datetime import date, timedelta

    tomorrow = date.today() + timedelta(days=1)
    info = get_day_info(tomorrow)

    system_prompt = "你是一位温暖的早安文案写手，用中文写作。"
    user_prompt = build_generation_prompt(info)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    print("=" * 50)
    print("原始生成:")
    print("=" * 50)
    raw = call_deepseek(messages)
    print(raw)
    print()

    print("=" * 50)
    print("Humanizer-zh 处理后:")
    print("=" * 50)
    humanized = humanize(raw)
    print(humanized)
