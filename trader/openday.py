# fetch opening day data from TWSE
# https://www.twse.com.tw/zh/holidaySchedule/holidaySchedule
# Example data:
# 名稱,日期,星期,說明,備註(* : 市場無交易，僅辦理結算交割作業。o : 交易日。)
# "中華民國開國紀念日","1月1日","日","依規定放假1日。<br>1月1日適逢星期日，於1月2日（星期一）補假1日。",""
import json
from datetime import datetime
from pathlib import Path

import requests

HOLIDAY_FILE = Path("holiday.json")


def download_holiday():
    """Download opening day data from TWSE"""
    holiday_url = f"https://www.twse.com.tw/holidaySchedule/holidaySchedule?response=csv&queryYear={datetime.now().year}"
    res = requests.get(holiday_url, timeout=5)
    res.raise_for_status()
    res.encoding = "big5"
    # remove first and second line
    lines = res.text.splitlines()[2:]
    result = []
    for line in lines:
        _, date, weekday, _, note = line.split(",")
        if weekday == '"六"' or weekday == '"日"' or note == '"o"':
            continue
        date = datetime.strptime(date, '"%m月%d日"').replace(year=datetime.now().year)
        result.append(date.strftime("%Y-%m-%d"))
    with open(HOLIDAY_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)


def is_opening(check_date: datetime = datetime.today()) -> bool:
    """Check if today is opening day"""
    if not HOLIDAY_FILE.exists():
        download_holiday()
    with open(HOLIDAY_FILE, encoding="utf-8") as f:
        holiday = json.load(f)
    # 判斷今天是不是週末
    return check_date.strftime("%Y-%m-%d") not in holiday and check_date.weekday() not in [5, 6]
