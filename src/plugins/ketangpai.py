from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
import json
import time

import requests

token = "3f52b53e7ce4bfda93ae0e8e169fe367b2ce8d5d8113445edc1d6deb2fef2f8f"
urlLogin = "https://openapiv51.ketangpai.com//CourseApi/semesterCourseList"
headersLogin = {
    "Request Method": "POST",
    "token": token,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
    "isstudy": "1",
    "search": "",
    "semester": "2021-2022",
    "term": "2",
    "reqtimestamp": "'.time().'"
}


#  "mstatus": 0:未提交 1:已提交 2:已批改阅分 3:已批改

def Login(token):
    result = requests.post(urlLogin, headersLogin)
    userData = result.json()
    # print(userData['status'])
    if userData['status'] == 1:
        return userData['data']


url2 = "https://openapiv51.ketangpai.com//FutureV2/CourseMeans/getCourseContent"

zuoye = on_command("作业")


@zuoye.handle()
async def GetCourseContent(bot: Bot, event: Event, state: dict):
    contexts = Login(token)
    str = "[2] 「快去写作业啊喂!」\n"
    for context in contexts:
        id = context['id']
        headers2 = {
            "Request Method": "POST",
            "token": token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
            "contenttype": 4,
            "dirid": 0,
            "lessonlink": [],
            "sort": [],
            "page": 1,
            "limit": 100,
            "desc": 3,
            "courserole": 0,
            "reqtimestamp": 1639575903985,
            "courseid": id
        }

        contextInfo = requests.post(url2, headers2)
        contextInfoM = contextInfo.json()
        i = 0
        if contextInfoM['data']['list'] != []:
            # print(context['coursename'])
            for contextWork in contextInfoM['data']['list']:
                i = i + 1
                res = int(contextWork['endtime'])
                if contextWork['mstatus'] == 0:
                    if i == 1:
                        str = str + "[-- " + context['coursename'] + " --]" + "\n"
                    endTime = time.strftime("%m-%d %H:%M:%S", time.localtime(res))
                    str = str + "[ " + contextWork['title'] + " ] End Time: " + endTime

    await bot.send(
        event=event,
        message=str
    )
