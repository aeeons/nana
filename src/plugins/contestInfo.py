from nonebot import on_command, on_message
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
import time
import nonebot
import requests, json

from nonebot import require

LEETCODE_URL = "https://leetcode-cn.com/problemset/all/"
base_url = 'https://leetcode-cn.com'

a = ""


def GetCodeforces():
    url = requests.get("https://codeforces.com/api/contest.list?gym=false")
    text = url.text
    contestsData = json.loads(text)
    strr = "[ codeforces ]\n"
    if (contestsData['status'] == 'OK'):
        contests = contestsData['result']
        res = contests[0]
        if (res['relativeTimeSeconds'] > 0):
            strr = strr + "No contests recently ." + "\n"
            return strr
        for contest in contests:
            if (contest['relativeTimeSeconds'] < 0):
                res = contest
            else:
                strr = strr + res['name'] + " " + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                time.localtime(res['startTimeSeconds'])) + "\n"
                return strr
    else:
        strr = strr + 'Codeforces API is abnormal .' + "\n"
        return strr


def GetContestsInfo():
    returnStr = ""
    headersLogin = {
        "Request Method": "POST",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
    }
    url = "https://ac.nowcoder.com/acm/calendar/contest?token=&month=2021-12&_="
    res = requests.get(url, headersLogin)
    res = json.loads(res.text)
    codeforces = {}
    NowCoder = {}
    AtCoder = {}
    UOJ = {}
    contests = res['data']
    for contest in contests:
        endTime = int(contest['endTime'])
        startTime = int(contest['startTime'])
        if endTime / 1000 < int(time.time()) or startTime / 1000 > int(time.time()) + 604800:
            continue
        name = contest['contestName'].strip()
        # if contest['ojName'] == "CodeForces" and len(codeforces) < 2:
        #     codeforces[name] = startTime
        if contest['ojName'] == "NowCoder" and len(NowCoder) < 2:
            NowCoder[name] = startTime
        if contest['ojName'] == "AtCoder" and len(AtCoder) < 2:
            AtCoder[name] = startTime
        if contest['ojName'] == "UOJ" and len(UOJ) < 2:
            UOJ[name] = startTime
    # returnStr += "[ codeforces ]\n"
    # print('[ codeforces ]')
    # for i in codeforces:
    #     res = int(codeforces[i])
    #     endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(res / 1000))
    #     returnStr += i + " " + endTime + "\n"
    # print(i + " " + endTime)
    returnStr += "[ NowCoder ]\n"
    # print('[ NowCoder ]')
    for i in NowCoder:
        res = int(NowCoder[i])
        endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(res / 1000))
        returnStr += i + " " + endTime + "\n"
        # print(i + " " + endTime)

    returnStr += "[ AtCoder ]\n"
    # print('[ AtCoder ]')
    for i in AtCoder:
        res = int(AtCoder[i])
        endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(res / 1000))
        returnStr += i + " " + endTime + "\n"
        # print(i + " " + endTime)

    returnStr += "[ UOJ ]\n"
    # print('[ UOJ ]')
    for i in UOJ:
        res = int(UOJ[i])
        endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(res / 1000))
        returnStr += i + " " + endTime + "\n"
        # print(i + " " + endTime)
    return returnStr


contestInfo = []
updataTime = []
updata = on_message()


@updata.handle()
async def updataContest(bot: Bot, event: Event, state: dict):
    a = time.localtime()
    if a.tm_hour == 19:
        await bot.send_msg(
            message_type="group",
            group_id=int(1124693419),
            message='开始更新'
        )
        updataTime.append(str(a.tm_year) + "/" + str(a.tm_mon) + "/" + str(a.tm_mday))
        contestInfo.append(GetCodeforces() + GetContestsInfo())
        await bot.send_msg(
            message_type="group",
            group_id=int(1124693419),
            message='更新成功' + updataTime[0]
        )


zuoye = on_command("最近比赛")


@zuoye.handle()
async def SendCodeforces(bot: Bot, event: Event, state: dict):
    strr = a + "[10] 「唔 nana已经为你准备好比赛信息了」\n"
    await bot.send(
        event=event,
        message=strr + contestInfo[0] + "\n[ 该数据更新于 " + updataTime[0] + " ]"
    )
