# 🌅 Morning Copy — Your Private Daily Greeting Broadcaster

> Wake up, phone buzzes — a morning message that knows the lunar calendar, solar terms, and today's theme is already waiting for you.
> Not generic copy-paste. AI-written, human-polished. **30 seconds, ready to record.**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Any_LLM-supported-orange" alt="Any Model">
</p>

---

## 📱 What You Get Every Day

```
🌅 Good morning! Today is June 11, 2026 · Thursday

Lunar: 丙午 (Horse) Year · April 26

Some say finding a kindred spirit is hard, but finding
someone you trust is even rarer. Friends don't need daily
chats — after six months apart, one sentence can still
catch you. That's real. Fate brought you together, but
trust is what walks the distance. A simple "I get you"
is worth more than anything.

Wishing you a smooth day! 💪
```

Every day is different. Monday = Love, Tuesday = Family, Wednesday = Friendship, Thursday = Mindset, Friday = Success, Saturday = Life Philosophy, Sunday = Wealth Mindset. When a solar term or festival arrives, the theme switches automatically.

---

## ✨ Why You Need This

| Pain | Fix |
|------|-----|
| 😫 Writing daily content burns you out | 🤖 Fully automated. You just sleep. |
| 📅 Can't track lunar dates & solar terms | 🗓️ Chinese lunisolar calendar baked in |
| 🤢 AI text reeks of ChatGPT | ✨ Humanizer-zh: 24 rules to kill AI flavor |
| 🔁 Accidentally repeat yesterday's copy | 🔒 SHA256 dedup. Near-zero collision. |
| 📱 Want it on your phone | 📲 Telegram Bot, one line to configure |

---

## 🚀 Get Running in 2 Minutes

### 1. Install

```bash
git clone https://github.com/jinxin13818-bot/morning-msg.git
cd morning-msg
uv sync
```

### 2. Configure

```bash
cp .env.example .env
```

Edit `.env`:

```bash
# LLM API (any OpenAI-compatible endpoint works)
LLM_API_KEY=sk-your-key
LLM_BASE_URL=https://api.deepseek.com     # Or https://api.openai.com
LLM_MODEL=deepseek-chat                    # Or your local model name

# Telegram Bot (optional — skip and just save locally)
TELEGRAM_BOT_TOKEN=123:abc
TELEGRAM_CHAT_ID=123456789
```

> 💡 **Any OpenAI-compatible API works**: DeepSeek, OpenAI, LM Studio, Ollama, vLLM… Just change `LLM_BASE_URL` and `LLM_MODEL`.

### 3. Run

```bash
uv run python main.py              # Generate tomorrow's copy
uv run python main.py --reroll     # Not happy? Regenerate.
uv run python main.py --date 2026-06-19  # Target a specific date
```

### 4. Schedule It (macOS)

```bash
# Edit the plist with your paths and API key, then:
cp com.jason.morning.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.jason.morning.plist
```

Runs at 23:00 daily. Wake up to a fresh message every morning.

---

## 🧠 Under the Hood

```
launchd (23:00) → main.py
  → calendar_utils.py: lookup tomorrow's lunisolar data
  → prompt.py: build themed prompt → call LLM
  → Humanizer-zh: 24 rules strip AI writing patterns
  → dedup.py: SHA256 check against SQLite → retry if dup (max 3x)
  → Save as Markdown with YAML frontmatter
  → Telegram Bot push to your phone
```

Simple stack, every piece battle-tested.

---

## 📁 File Map

```
morning-msg/
├── main.py              ← Entry point. Just run this.
├── config.py            ← Festivals, solar terms, themes, API config
├── calendar_utils.py    ← Gregorian↔Lunar, solar term detection
├── prompt.py            ← LLM calls + Humanizer-zh pipeline
├── dedup.py             ← SHA256-based deduplication
├── push.py              ← Telegram Bot integration
├── com.jason.morning.plist ← launchd schedule (macOS)
└── .env.example         ← Environment variable template
```

---

## ☕ Buy Me a Coffee

If this project saves you from the daily grind of writing morning copy—

<p align="center">
  <img src="coffee.jpg" width="200" alt="Buy me a coffee">
</p>

Late nights debugging lunar calendar edge cases, wrestling prompts until they sound human, stopping AI from saying "in this fast-paced world"… Code is free, coffee is not 😄

---

## 📄 License

MIT — use it, remix it, just don't forget to ⭐ Star.
