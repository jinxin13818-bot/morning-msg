# 🌅 早安文案 — 你的私人早安播报员

> 每天醒来，手机一震，一条懂节气、知农历、有温度的早安文案已经躺好了。
> 不是群发的鸡汤，是 AI 帮你写的、去了机器味的口播稿。
> **30 秒一条，直接能录。**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/模型-随意换-orange" alt="Any Model">
</p>

---

## 📱 每天你会收到什么

```
🌅 早安！今天是 2026年6月11日 星期四

农历丙午马年 四月二十六日

都说知己难找，其实能信任的更金贵。朋友不用天天见，
隔了半年，一句话还能接住你，那才是真的。缘分让你我认识，
信任才让关系走远。一句"我懂"，比什么都管用。

祝你今天一切顺利！💪
```

每天不重样。周一聊爱情，周二写亲情，周三说友情，周四讲心态，周五搞成功学，周六谈人生哲学，周日悟搞钱思维。遇到节气节日，自动切换主题。

---

## ✨ 为什么你需要它

| 痛点 | 解决 |
|------|------|
| 😫 每天想文案想到头秃 | 🤖 全自动，你只管睡 |
| 📅 搞不清农历和节气 | 🗓️ 干支纪年 + 二十四节气全自动 |
| 🤢 AI 写的味太重 | ✨ Humanizer-zh 24条规则去 AI 味 |
| 🔁 怕重复发一样的 | 🔒 SHA256 去重，撞车率接近零 |
| 📱 想推送到手机 | 📲 Telegram Bot 一键推送 |

---

## 🚀 2 分钟跑起来

### 1. 装依赖

```bash
git clone https://github.com/jinxin13818-bot/morning-msg.git
cd morning-msg
uv sync
```

### 2. 配环境变量

```bash
cp .env.example .env
```

编辑 `.env`：

```bash
# 模型 API（用哪个都行——DeepSeek / OpenAI / 本地 LM Studio 全兼容）
LLM_API_KEY=sk-your-key
LLM_BASE_URL=https://api.deepseek.com     # 用 OpenAI 就填 https://api.openai.com
LLM_MODEL=deepseek-chat                    # 用本地模型就填你的模型名

# Telegram Bot（不配也行，只存档不推送）
TELEGRAM_BOT_TOKEN=123:abc
TELEGRAM_CHAT_ID=123456789
```

> 💡 **支持任何 OpenAI 兼容接口**：DeepSeek、OpenAI、LM Studio、Ollama、vLLM……换模型只需改 `LLM_BASE_URL` 和 `LLM_MODEL`。

### 3. 跑

```bash
uv run python main.py           # 生成明天的
uv run python main.py --reroll  # 不满意？重写
uv run python main.py --date 2026-06-19  # 指定日期（比如端午节）
```

### 4. 设个定时（macOS）

```bash
# 编辑 plist 里的路径和 API Key，然后：
cp com.jason.morning.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.jason.morning.plist
```

每天 23:00 自动生成第二天的文案，你醒来就能收到。

---

## 🧠 技术内幕

```
launchd（23:00）→ main.py
  → calendar_utils.py 查明天历法（农历+节气+节日+星期主题）
  → prompt.py 构建 prompt → 调 LLM 生成文案
  → Humanizer-zh 24条规则去AI味（删"在这个快节奏的时代"那种）
  → dedup.py SHA256 查 SQLite → 重复就重写（最多3次）
  → 写入 Obsidian Markdown（YAML frontmatter）
  → Telegram Bot 推送到你手机
```

就这些，不复杂。但每个环节都抠过了。

---

## 📁 文件地图

```
morning-msg/
├── main.py              ← 入口，跑他就行
├── config.py            ← 节日/节气/主题/API 全在这
├── calendar_utils.py    ← 公历→农历，节气判断
├── prompt.py            ← LLM 调用 + Humanizer-zh
├── dedup.py             ← SHA256 去重
├── push.py              ← Telegram 推送
├── com.jason.morning.plist ← launchd 定时配置
└── .env.example         ← 环境变量模板
```

---

## ☕ 请我喝杯咖啡

如果这个项目帮你省了每天挠头想文案的时间——

<p align="center">
  <b>👉 把收款码图片放到 <code>coffee.png</code> 就能显示在此 👈</b>
</p>

<!-- 替换为你的收款二维码 -->
<!-- <p align="center"><img src="coffee.png" width="200"></p> -->

半夜调 prompt、修农历 bug、跟 AI 斗智斗勇……代码免费，咖啡不免费 😄

---

## 📄 License

MIT — 随便改，随便用，记得 Star ⭐
