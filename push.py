"""双通道推送 — macOS 通知 + Telegram Bot"""

import subprocess
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def _escape_applescript(s: str) -> str:
    """转义 AppleScript 字符串中的特殊字符"""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def send_macos_notification(title: str, message: str, open_url: str | None = None):
    """
    发送 macOS 系统通知。

    Args:
        title: 通知标题
        message: 通知内容
        open_url: 点击通知后打开的 URL（可选，如 obsidian://）
    """
    title = _escape_applescript(title)
    message = _escape_applescript(message.replace("\n", " "))

    script_parts = [
        f'display notification "{message}" with title "{title}"',
    ]
    if open_url:
        open_url_escaped = _escape_applescript(open_url)
        script_parts.append(f'open location "{open_url_escaped}"')

    script = "\n".join(script_parts)

    full_script = f"on run\n{script}\nend run"

    try:
        subprocess.run(
            ["osascript", "-e", full_script],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )
        print("[PUSH] macOS 通知发送成功")
    except subprocess.CalledProcessError as e:
        print(f"[PUSH] macOS 通知失败: {e.stderr}")


def send_telegram(text: str, parse_mode: str = "HTML") -> bool:
    """
    发送 Telegram 消息。

    Args:
        text: 消息内容
        parse_mode: 解析模式（HTML/Markdown/None）

    Returns:
        是否发送成功
    """
    if "YOUR_BOT_TOKEN" in TELEGRAM_BOT_TOKEN or "YOUR_CHAT_ID" in TELEGRAM_CHAT_ID:
        print("[PUSH] Telegram 未配置，跳过")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": parse_mode,
    }

    try:
        resp = requests.post(url, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("ok"):
            print("[PUSH] Telegram 发送成功")
            return True
        else:
            print(f"[PUSH] Telegram 发送失败: {data}")
            return False
    except Exception as e:
        print(f"[PUSH] Telegram 异常: {e}")
        return False


def push_morning(day_info: dict, text: str, obsidian_uri: str):
    """
    双通道推送早安文案。

    Args:
        day_info: get_day_info() 返回的日期信息
        text: 文案正文
        obsidian_uri: Obsidian 笔记的 URI（如 obsidian://open?vault=...&file=...）
    """
    theme = day_info["theme"]["name"]
    lunar = day_info["lunar_display"]
    date_str = day_info["date"].strftime("%m月%d日")

    # 简短预览（前 60 字）
    preview = text[:60] + ("..." if len(text) > 60 else "")

    # macOS 通知
    notify_title = f"🌅 {date_str} 早安"
    notify_msg = f'{lunar} · {theme}\n\n"{preview}"'
    send_macos_notification(notify_title, notify_msg, open_url=obsidian_uri)

    # Telegram 消息
    telegram_text = f"""🌅 <b>{date_str} 早安</b>
{lunar} · {theme}

"{preview}"

📖 <a href="{obsidian_uri}">打开 Obsidian 看全文</a>"""
    send_telegram(telegram_text)


if __name__ == "__main__":
    # 测试 macOS 通知
    send_macos_notification("测试", "这是一条测试通知")
    print("如果看到通知弹窗，说明 macOS 推送正常")
