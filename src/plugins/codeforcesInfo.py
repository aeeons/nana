from nonebot import on_command, on_regex
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
import time
import requests, json

pattern = '查分&#91;(.*?)\&#93;'

query = on_regex(pattern, flags=0, rule=None)


@query.handle()
async def qeuryInfo(bot: Bot, event: Event, state: dict):
    name = state['_matched_groups'][0]
    url = requests.get("https://codeforces.com/api/user.info?handles=" + name)
    text = url.text
    userInfo = json.loads(text)
    refStr = "[3] "
    if (userInfo['status'] == "OK"):
        nowRating = userInfo['result'][0]['rating']
        maxRating = userInfo['result'][0]['maxRating']
        refStr += name + "当前 [ " + str(nowRating) + " ] 分，最高达到 [ " + str(maxRating) + " ] 分"
        await bot.send(
            event=event,
            message=refStr
        )
    else:
        refStr += "「没有这个人啊喂!」"
        await bot.send(
            event=event,
            message=refStr
        )


jmu = on_command("集训队查分")


@jmu.handle()
async def SendCodeforces(bot: Bot, event: Event, state: dict):
    names = ['G_LX', 'CWJ_123', 'hialine', 'solity', 'xanadu', 'hhhhhl', 'Flatday', 'Nakamiya', 'HOW_ALL_HAPPY']
    refStr = "[5] jmu集训队分数\n"
    rankList = []
    for name in names:
        url = requests.get("https://codeforces.com/api/user.info?handles=" + name)
        text = url.text
        userInfo = json.loads(text)
        nowRating = userInfo['result'][0]['rating']
        maxRating = userInfo['result'][0]['maxRating']
        rankTuple = (name, nowRating, maxRating)
        rankList.append(rankTuple)

    rankList = sorted(rankList, key=lambda x: x[1], reverse=True)
    res = 1
    for rank in rankList:
        refStr += 'No.' + str(res) + " " + rank[0] + '\n'
        refStr += "当前 [ " + str(rank[1]) + " ] 分，最高达到 [ " + str(rank[2]) + " ] 分\n"
        res += 1
    await bot.send(
        event=event,
        message=refStr
    )
