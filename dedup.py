"""文案去重 — SHA256 + SQLite"""

import hashlib
import sqlite3
import os
from config import DB_PATH


def _get_conn() -> sqlite3.Connection:
    """获取数据库连接，自动初始化表"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sha256 TEXT UNIQUE NOT NULL,
            date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn


def sha256_hash(text: str) -> str:
    """计算文本的 SHA256 哈希"""
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def is_duplicate(text: str) -> bool:
    """检查文案是否已存在"""
    h = sha256_hash(text)
    conn = _get_conn()
    cur = conn.execute("SELECT 1 FROM history WHERE sha256 = ?", (h,))
    result = cur.fetchone() is not None
    conn.close()
    return result


def save_text(text: str, target_date: str):
    """保存文案哈希到历史库"""
    h = sha256_hash(text)
    conn = _get_conn()
    conn.execute(
        "INSERT OR IGNORE INTO history (sha256, date) VALUES (?, ?)",
        (h, target_date),
    )
    conn.commit()
    conn.close()


def clear_db():
    """清空历史库（调试用）"""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


if __name__ == "__main__":
    # 测试
    test_text = "这是一条测试早安文案"
    print(f"SHA256: {sha256_hash(test_text)[:16]}...")
    print(f"重复? {is_duplicate(test_text)}")
    save_text(test_text, "2026-06-09")
    print(f"保存后重复? {is_duplicate(test_text)}")
    # 清理测试数据
    clear_db()
    print("测试完成，已清理")
