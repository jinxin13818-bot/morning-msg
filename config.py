"""早安文案项目 — 配置文件"""

import os

# --- 路径 ---
VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(OUTPUT_DIR, "history.db")

# --- DeepSeek API ---
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# --- Telegram ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# --- 节日列表（公历 + 农历）---
# 公历节日: (月, 日, 名称)
SOLAR_FESTIVALS = {
    (1, 1): "元旦",
    (2, 14): "情人节",
    (3, 8): "妇女节",
    (4, 1): "愚人节",
    (5, 1): "劳动节",
    (5, 4): "青年节",
    (6, 1): "儿童节",
    (7, 1): "建党节",
    (8, 1): "建军节",
    (9, 10): "教师节",
    (10, 1): "国庆节",
    (10, 31): "万圣节",
    (12, 25): "圣诞节",
}

# 农历节日: (月, 日, 名称) — 月日为农历
LUNAR_FESTIVALS = {
    (1, 1): "春节",
    (1, 15): "元宵节",
    (5, 5): "端午节",
    (7, 7): "七夕",
    (7, 15): "中元节",
    (8, 15): "中秋节",
    (9, 9): "重阳节",
    (12, 30): "除夕",
}

# 二十四节气（按顺序，用于查找最近的节气）
SOLAR_TERMS = [
    "小寒", "大寒", "立春", "雨水", "惊蛰", "春分",
    "清明", "谷雨", "立夏", "小满", "芒种", "夏至",
    "小暑", "大暑", "立秋", "处暑", "白露", "秋分",
    "寒露", "霜降", "立冬", "小雪", "大雪", "冬至",
]

# --- 七日主题 ---
WEEKDAY_THEMES = {
    0: {"name": "搞钱思维", "direction": "认知、机会、财富观"},
    1: {"name": "爱情", "direction": "浪漫、亲密关系、心动"},
    2: {"name": "亲情", "direction": "家人、陪伴、孝道"},
    3: {"name": "友情", "direction": "知己、信任、缘分"},
    4: {"name": "心态", "direction": "情绪、压力、自我和解"},
    5: {"name": "成功学", "direction": "自律、目标、行动力"},
    6: {"name": "人生哲学", "direction": "意义、选择、放下"},
}

# --- 文案生成 ---
MAX_GENERATION_RETRIES = 3  # 去重失败最大重试次数
TARGET_LENGTH = "130-180字"  # 目标长度（约30-35秒口播）
