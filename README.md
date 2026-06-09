# 早安文案

每日自动生成早安鸡汤文案，含农历日期、二十四节气、节日匹配，支持七日主题轮换，经 Humanizer-zh 去 AI 味后通过 Telegram Bot 推送。

## 功能

- 📅 **历法查询**：公历 → 农历（干支纪年 + 生肖）、二十四节气、公历/农历节日
- 🎯 **七日主题轮换**：爱情、亲情、友情、心态、成功学、人生哲学、搞钱思维
- 🤖 **DeepSeek 生成**：根据当天主题和节气节日自动生成文案
- ✨ **Humanizer-zh 去 AI 味**：24 条规则检测并消除 AI 痕迹
- 🔒 **SHA256 去重**：SQLite 存储历史文案哈希，避免重复
- 📱 **Telegram 推送**：每日定时推送到你的 Telegram
- 💾 **Markdown 存档**：文案以 YAML frontmatter 格式存入本地

## 快速开始

### 1. 环境要求

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

### 2. 安装

```bash
git clone https://github.com/你的用户名/morning-msg.git
cd morning-msg
uv sync
```

### 3. 配置

```bash
cp .env.example .env
# 编辑 .env 填入你的 DeepSeek API Key 和 Telegram Bot Token
```

或直接设置环境变量：

```bash
export DEEPSEEK_API_KEY="sk-xxx"
export TELEGRAM_BOT_TOKEN="123:abc"
export TELEGRAM_CHAT_ID="123456"
```

### 4. 运行

```bash
# 生成明日文案
uv run python main.py

# 重新生成（覆盖）
uv run python main.py --reroll

# 指定日期
uv run python main.py --date 2026-06-19
```

### 5. 定时任务（macOS launchd）

```bash
# 加载 plist（每天 23:00 自动运行）
cp com.jason.morning.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.jason.morning.plist
```

## 文件结构

```
morning-msg/
├── main.py              # 主入口，流程编排
├── config.py            # 配置（节日、节气、主题）
├── calendar_utils.py    # 农历/节气/节日查询
├── prompt.py            # DeepSeek 调用 + Humanizer-zh
├── dedup.py             # SHA256 去重
├── push.py              # Telegram 推送
├── com.jason.morning.plist  # launchd 配置
└── .env.example         # 环境变量模板
```

## License

MIT
