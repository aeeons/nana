import requests
from lxml import etree
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
}
url = "https://codeforces.com/contests?complete=true"


def GetCodeforcesContests(nameList):
    contestList = []
    url = requests.get("https://codeforces.com/api/contest.list?gym=false")
    text = url.text
    contestsData = json.loads(text)
    contests = contestsData['result']

    for name in nameList:
        for contest in contests:
            if contest['name'] == name:
                contestMap = {}
                contestMap['name'] = name
                contestMap['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(contest['startTimeSeconds']))
                contestMap['url'] = 'https://codeforces.com/contests/' + str(contest['id'])
                contestList.append(contestMap)
                break

    return contestList


def getTree():
    response = requests.get(url=url, headers=headers)
    return etree.HTML(response.text)


def getContestsList():
    tree = getTree()
    contestsList = tree.xpath('//*[@id="pageContent"]/div[1]/div[1]/div[6]/table//tr')
    contestNameList = []

    for contest in contestsList:
        contestName = contest.xpath('./td[1]/text()')
        if len(contestName) == 0:
            continue

        contestName = contest.xpath('./td[1]/text()')[0].strip('/r').strip()
        contestNameList.append(contestName)

    contestList = GetCodeforcesContests(contestNameList)

    return contestList
