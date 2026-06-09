"""日历工具 — 公历/农历转换、节气、节日、星期主题"""

from datetime import date, datetime, timedelta
import zhdate
from config import (
    SOLAR_FESTIVALS, LUNAR_FESTIVALS, SOLAR_TERMS, WEEKDAY_THEMES
)


# 天干地支
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
SHENG_XIAO = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

# 农历月份名
LUNAR_MONTH_NAMES = [
    "", "正月", "二月", "三月", "四月", "五月", "六月",
    "七月", "八月", "九月", "十月", "冬月", "腊月"
]

# 农历日期名
LUNAR_DAY_NAMES = [
    "", "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
    "二十一", "二十二", "二十三", "二十四", "二十五", "二十六", "二十七", "二十八", "二十九", "三十"
]

# 星期名
WEEKDAY_NAMES = ["一", "二", "三", "四", "五", "六", "日"]


def _lunar_year_name(lunar_year: int) -> str:
    """返回干支纪年 + 生肖，如 '丙午马年'"""
    gan = TIAN_GAN[(lunar_year - 4) % 10]
    zhi = DI_ZHI[(lunar_year - 4) % 12]
    shengxiao = SHENG_XIAO[(lunar_year - 4) % 12]
    return f"{gan}{zhi}{shengxiao}年"


def _lunar_month_name(lunar_month: int, is_leap: bool) -> str:
    """返回农历月份名，如 '四月'、'闰四月'"""
    name = LUNAR_MONTH_NAMES[lunar_month]
    return f"闰{name}" if is_leap else name


def _lunar_day_name(lunar_day: int) -> str:
    """返回农历日期名，如 '初三'、'廿三'"""
    return LUNAR_DAY_NAMES[lunar_day]


def _get_solar_term(d: date) -> str | None:
    """返回当天的节气名，如果不是节气则返回 None"""
    try:
        # zhdate 支持查询节气
        term = zhdate.ZhDate.get_solar_term(d.year, d.month, d.day)
        return term
    except Exception:
        return None


def _get_festival(d: date, lunar: zhdate.ZhDate) -> str | None:
    """返回当天的节日名（公历优先，农历其次）"""
    # 公历节日
    solar_key = (d.month, d.day)
    if solar_key in SOLAR_FESTIVALS:
        return SOLAR_FESTIVALS[solar_key]

    # 农历节日
    lunar_key = (lunar.lunar_month, lunar.lunar_day)
    if lunar_key in LUNAR_FESTIVALS:
        festival = LUNAR_FESTIVALS[lunar_key]
        # 除夕特殊处理：如果腊月三十不存在（小月），用腊月廿九
        return festival

    # 检查除夕（腊月最后一天）
    # 如果今天腊月三十不存在，那腊月廿九就是除夕
    if lunar.lunar_month == 12:
        # 尝试判断是否是这个农历年的最后一天
        pass  # zhdate 的除夕判断比较复杂，先留后用

    return None


def _get_theme(d: date, solar_term: str | None, festival: str | None) -> dict:
    """根据节气/节日/星期返回当天主题"""
    # 重要节气覆盖（二十四节气日）
    if solar_term:
        return {"name": solar_term, "direction": "节气氛围、自然、时令"}

    # 重要节日覆盖
    if festival:
        return {"name": festival, "direction": "节日氛围、传统、祝福"}

    # 星期主题
    return WEEKDAY_THEMES[d.weekday()]


def get_day_info(target_date: date) -> dict:
    """
    获取指定日期的完整信息。

    Args:
        target_date: 目标公历日期

    Returns:
        {
            "date": date对象,
            "solar_date": "2026-06-09",
            "weekday": "二",
            "weekday_num": 2,
            "lunar_year_name": "丙午马年",
            "lunar_month_name": "四月",
            "lunar_day_name": "廿三",
            "lunar_display": "丙午马年 四月廿三",
            "solar_term": "芒种" | None,
            "festival": "端午节" | None,
            "theme": {"name": "爱情", "direction": "..."},
        }
    """
    lunar = zhdate.ZhDate.from_datetime(datetime(target_date.year, target_date.month, target_date.day))
    solar_term = _get_solar_term(target_date)
    festival = _get_festival(target_date, lunar)
    theme = _get_theme(target_date, solar_term, festival)

    return {
        "date": target_date,
        "solar_date": target_date.strftime("%Y-%m-%d"),
        "weekday": WEEKDAY_NAMES[target_date.weekday()],
        "weekday_num": target_date.weekday(),
        "lunar_year_name": _lunar_year_name(lunar.lunar_year),
        "lunar_month_name": _lunar_month_name(lunar.lunar_month, lunar.leap_month),
        "lunar_day_name": _lunar_day_name(lunar.lunar_day),
        "lunar_display": f"{_lunar_year_name(lunar.lunar_year)} {_lunar_month_name(lunar.lunar_month, lunar.leap_month)}{_lunar_day_name(lunar.lunar_day)}日",
        "solar_term": solar_term,
        "festival": festival,
        "theme": theme,
    }


if __name__ == "__main__":
    # 测试：明天
    tomorrow = date.today() + timedelta(days=1)
    info = get_day_info(tomorrow)
    for k, v in info.items():
        print(f"  {k}: {v}")
