import os
import csv
import time
import pathlib
import requests
from datetime import datetime

# 这地方填房间号和uid
room_id = 21013446
uid = 387636363

now_time = datetime.now().strftime('%Y年%m月%d日%H时%M分%S秒')

def reqGuardList(page):
    res = requests.get("https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList", {
        "roomid" : room_id,
        "page" : page,
        "ruid" : uid,
        "page_size" : 29
    })
    res.encoding = "utf-8"
    return res.json()

pathlib.Path('舰队成员名单', encoding='utf-8').mkdir(parents=True,exist_ok=True)

def storeData(li):
    with open(os.path.join("舰队成员名单\{timeis}.csv".format(timeis = now_time)), 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, delimiter = ",", 
            fieldnames = ["uid", "名字", "排名", "舰队等级", "粉丝牌等级"])
        for guard in li:
            writer.writerow({
                "uid" : guard["uid"], 
                "名字" : guard["username"], 
                "排名" : guard["rank"], 
                "舰队等级" : guardLevelConvert(guard["guard_level"]),
                "粉丝牌等级" : guard["medal_info"]["medal_level"]
            })
        f.close()

def guardLevelConvert(guard_level):
    level = {
        1 : "总督",
        2 : "提督",
        3 : "舰长"
    }
    return level.get(guard_level)

data = reqGuardList(1)
total_page = data["data"]["info"]["page"]

with open(os.path.join("舰队成员名单\{timeis}.csv".format(timeis = now_time)), 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, delimiter = ",", 
        fieldnames = ["uid", "名字", "排名", "舰队等级", "粉丝牌等级"])
    writer.writeheader()
    for guard in data["data"]["top3"]:
            writer.writerow({
                "uid" : guard["uid"], 
                "名字" : guard["username"], 
                "排名" : guard["rank"], 
                "舰队等级" : guardLevelConvert(guard["guard_level"]),
                "粉丝牌等级" : guard["medal_info"]["medal_level"]
            })
    f.close()

print("舰队共有{num}位成员，合计{total_page}页\n正在输出第1页，合计{total_page}页"
    .format(num = data["data"]["info"]["num"], total_page = total_page), )
storeData(data["data"]["list"])

for i in range(2, total_page + 1):
    time.sleep(5)
    print("正在输出第{page}页，合计{total_page}页".format(page = i, total_page = total_page), )
    data = reqGuardList(i)
    storeData(data["data"]["list"])

print("{page}页已合并完成，请打开文档查看"
    .format(num = data["data"]["info"]["num"], page = i), )
