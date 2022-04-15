import requests
from lxml import etree
import json

# -*- coding: UTF-8 -*-

import requests
from lxml import etree
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'Connection': 'close'
}
url = ["https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=13",
       "https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=14"]


def getTree():
    trees = []
    for i in range(2):
        response = requests.get(url=url[i], headers=headers)
        trees.append(etree.HTML(response.text))
    return trees


def changeTime(contestTime):
    # 比赛时间：    2022-04-17 13:00
    #  至     2022-04-17 18:00
    #  (时长:5小时)

    newTime = ""
    block = False
    for ch in contestTime:
        if ch == '\n' or (ch == ' ' and block == True):
            continue
        if ch == '(':
            break
        newTime += ch
        block = True if ch == ' ' else False

    return newTime[6:]


def checkName(contestName):
    if contestName.find("大学") != -1 or contestName.find("学院") != -1:
        return True
    if contestName.find("小白") != -1:
        return True
    if contestName.find("练习") != -1:
        return True
    if contestName.find("挑战") != -1:
        return True
    return False


def getContestsList():
    tree = getTree()
    contestsLists = []
    for i in range(2):
        List = tree[i].xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div')
        del List[0]
        contestsLists.append(List)

    contestLists = []

    for contestsList in contestsLists:
        contestList = []
        for contest in contestsList:
            contestMap = {}
            contestName = contest.xpath('./div[2]/div[1]/h4/a/text()')[0]
            if checkName(contestName) == False:
                continue
            # print(contestName)

            contestTime = contest.xpath('./div[2]/div[1]/ul/li[2]/text()')[0]
            contestTime = changeTime(contestTime)
            # print(contestTime[6:])

            j = 0
            while j < len(contestName):
                if contestName[j].isdigit():
                    break
                j += 1

            contestURL = contest.xpath('./div[2]/div[1]/h4/a/@href')[0]
            contestID = int(contestURL[13:])
            contestURL = 'https://ac.nowcoder.com' + contestURL

            contestMap['name'] = contestName
            contestMap['time'] = contestTime
            contestMap['url'] = contestURL
            contestList.append(contestMap)
        contestLists.append(contestList)

    return contestLists
