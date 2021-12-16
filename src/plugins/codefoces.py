from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
import time

import requests, json

zuoye = on_command("最近比赛")


@zuoye.handle()
async def GetCodeforces(bot: Bot, event: Event, state: dict):
    url = requests.get("https://codeforces.com/api/contest.list?gym=false")
    text = url.text
    contestsData = json.loads(text)
    strr = ""
    if (contestsData['status'] == 'OK'):
        contests = contestsData['result']
        res = contests[0]
        if (res['relativeTimeSeconds'] > 0):
            strr = strr + "No contests recently ." + "\n"
            await bot.send(
                event=event,
                message=strr
            )
            return
            # print('No contests recently .')
        for contest in contests:
            if (contest['relativeTimeSeconds'] < 0):
                res = contest
            else:
                strr = strr + "The next contests is :" + res['name'] + "\n"
                # strr = strr + "https://codeforces.com/contests/" + str(res['id']) + "\n"
                strr = strr + 'Start time: ' + time.strftime("%Y--%m--%d %H:%M:%S",
                                                             time.localtime(res['startTimeSeconds'])) + "\n"

                await bot.send(
                    event=event,
                    message=strr
                )
                return
    else:
        strr = strr + 'Codeforces API is abnormal .' + "\n"
        # print('Codeforces API is abnormal .')
        await bot.send(
            event=event,
            message=strr
        )
        return
