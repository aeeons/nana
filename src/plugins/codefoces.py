from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
import time
import nonebot
import requests, json

from nonebot import require

LEETCODE_URL = "https://leetcode-cn.com/problemset/all/"
base_url = 'https://leetcode-cn.com'


def get_leetcode_question_everyday() -> str:
    try:
        resp = requests.get(url=LEETCODE_URL)
        response = requests.post(base_url + "/graphql", json={
            "operationName": "questionOfToday",
            "variables": {},
            "query": "query questionOfToday { todayRecord {   question {     questionFrontendId     questionTitleSlug     __typename   }   lastSubmission {     id     __typename   }   date   userStatus   __typename }}"
        })

        leetcodeTitle = json.loads(response.text).get('data').get('todayRecord')[0].get("question").get(
            'questionTitleSlug')

        # 获取今日每日一题的所有信息
        url = base_url + "/problems/" + leetcodeTitle
        response = requests.post(base_url + "/graphql",
                                 json={"operationName": "questionData", "variables": {"titleSlug": leetcodeTitle},
                                       "query": "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    questionFrontendId    boundTopicId    title    titleSlug    content    translatedTitle    translatedContent    isPaidOnly    difficulty    likes    dislikes    isLiked    similarQuestions    contributors {      username      profileUrl      avatarUrl      __typename    }    langToValidPlayground    topicTags {      name      slug      translatedName      __typename    }    companyTagStats    codeSnippets {      lang      langSlug      code      __typename    }    stats    hints    solution {      id      canSeeDetail      __typename    }    status    sampleTestCase    metaData    judgerAvailable    judgeType    mysqlSchemas    enableRunCode    envInfo    book {      id      bookName      pressName      source      shortDescription      fullDescription      bookImgUrl      pressImgUrl      productUrl      __typename    }    isSubscribed    isDailyQuestion    dailyRecordStatus    editorType    ugcQuestionId    style    __typename  }}"})
        # 转化成json格式
        jsonText = json.loads(response.text).get('data').get("question")
        # 题目题号
        no = jsonText.get('questionFrontendId')
        # 题名（中文）
        leetcodeTitle = jsonText.get('translatedTitle')
        # 题目难度级别
        level = jsonText.get('difficulty')
        # 题目内容
        context = jsonText.get('translatedContent')

        nonebot.log.logger.info("html:{}".format(json.dumps(jsonText)))
        return json.dumps(jsonText)
    except Exception as ex:
        raise ex


def send_leetcode():
    question = get_leetcode_question_everyday()
    nonebot.log.logger.info("question:{}".format(question))
    # 转化成json格式
    jsonText = json.loads(question)
    # 题目题号
    no = jsonText.get('questionFrontendId')
    # 题名（中文）
    leetcodeTitle = jsonText.get('translatedTitle')
    # 提名 (英文)
    titleSlug = jsonText.get('titleSlug')
    # 题目难度级别
    level = jsonText.get('difficulty')
    # 题目内容
    context = jsonText.get('translatedContent')
    # 题目链接
    link = "https://leetcode-cn.com/problems/{}/".format(titleSlug)
    return "no:{}\ntitle:{}\nlevel:{}\nlink:{}".format(no, leetcodeTitle, level, link)


scheduler = require("nonebot_plugin_apscheduler").scheduler

a = ""


@scheduler.scheduled_job('cron', hour=15, jitter=30, id='updata')
async def match_checker():
    try:
        bot: Bot = get_bot()  # 当未连接bot时返回
    except ValueError:
        return
    await bot.send(
        event=event,
        message="更新cf信息成功"
    )


def GetCodeforces():
    url = requests.get("https://codeforces.com/api/contest.list?gym=false")
    text = url.text
    contestsData = json.loads(text)
    strr = "[codeforces:]\n"
    if (contestsData['status'] == 'OK'):
        contests = contestsData['result']
        res = contests[0]
        if (res['relativeTimeSeconds'] > 0):
            strr = strr + "No contests recently ." + "\n"
            return strr
            # print('No contests recently .')
        for contest in contests:
            if (contest['relativeTimeSeconds'] < 0):
                res = contest
            else:
                strr = strr + res['name'] + "\n"
                # strr = strr + "https://codeforces.com/contests/" + str(res['id']) + "\n"
                strr = strr + 'time: ' + time.strftime("%Y-%m-%d %H:%M:%S",
                                                       time.localtime(res['startTimeSeconds'])) + "\n"
                return strr
    else:
        strr = strr + 'Codeforces API is abnormal .' + "\n"
        # print('Codeforces API is abnormal .')
        return strr


zuoye = on_command("最近比赛")


@zuoye.handle()
async def SendCodeforces(bot: Bot, event: Event, state: dict):
    strr = a + "[10] 「唔 nana已经为你准备好比赛信息了」\n"
    await bot.send(
        event=event,
        message=strr + GetCodeforces()
    )
