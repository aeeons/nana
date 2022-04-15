from nonebot import on_command, on_message, on_regex
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
import time
import nonebot
import requests, json
import os
from ContestsSpider import atcoderSpider, codeforcesSpider
from ContestsSpider import nowcoderSpider

from nonebot import require

contestUrl = []
data = ""


def GetContests():
    atcoderContest = atcoderSpider.getContestsList()[0]
    codeforcsContest = codeforcesSpider.getContestsList()[0]
    nowcoderContests = nowcoderSpider.getContestsList()
    index = 0
    contestInform = ""
    if 'name' in atcoderContest:
        contestInform += '「' + str(index) + '」 ' + atcoderContest['name'] + '\n' + atcoderContest['time'] + '\n'
        contestUrl.append(atcoderContest['url'])
        index += 1

    if 'name' in codeforcsContest:
        contestInform += '「' + str(index) + '」 ' + codeforcsContest['name'] + '\n' + codeforcsContest['time'] + '\n'
        contestUrl.append(codeforcsContest['url'])
        index += 1

    for nowcoderContest in nowcoderContests:
        contestInform += '「' + str(index) + '」 ' + nowcoderContest[0]['name'] + '\n' + nowcoderContest[0]['time'] + '\n'
        contestUrl.append(nowcoderContest[0]['url'])
        index += 1

    with open(os.getcwd() + "/src/plugins/ContestsSpider/contestInforms.txt", encoding='utf-8', mode='w+') as f_obj:
        f_obj.write(contestInform)
    f_obj.close()

    return contestInform


scheduler = require('nonebot_plugin_apscheduler').scheduler


@scheduler.scheduled_job('cron', hour='01', minute='10', id='UpdateContest')
async def UpdateContest():
    (bot,) = nonebot.get_bots().values()
    GetContests()
    await bot.send_msg(
        message_type="group",
        group_id=int(1124693419),
        message='三点几嚟，做碌鸠啊做！做这么多，老板不会心疼你的,饮茶先啦！'
    )


zuoye = on_command("最近比赛")


@zuoye.handle()
async def SendCodeforces(bot: Bot, event: Event, state: dict):
    updataTime = []

    with open(os.getcwd() + "/src/plugins/ContestsSpider/contestInforms.txt", encoding='utf-8') as f_obj:
        data = f_obj.read()
    f_obj.close()

    if len(data) == 0:
        GetContests()
        with open(os.getcwd() + "/src/plugins/ContestsSpider/contestInforms.txt", encoding='utf-8') as f_obj:
            data = f_obj.read()
        f_obj.close()

    now = time.localtime()
    updataTime.append(str(now.tm_year) + "/" + str(now.tm_mon) + "/" + str(now.tm_mday))
    strr = "[10] 「唔 nana已经为你准备好比赛信息了」\n"
    strr += str(os.getcwd()) + "/ContestsSpider/contestInforms.txt"
    await bot.send(
        event=event,
        message=strr + "[ 比赛数据更新于 " + updataTime[0] + " ]" + '\n' + data
    )


pattern = '比赛链接&#91;(.*?)\&#93;'

query = on_regex(pattern, flags=0, rule=None)


@query.handle()
async def queryInfo(bot: Bot, event: Event, state: dict):
    urlId = int(state['_matched_groups'][0])

    await bot.send(
        event=event,
        message=contestUrl[urlId]
    )
