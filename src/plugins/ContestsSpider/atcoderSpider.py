import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'Connection': 'close'
}
url = "https://atcoder.jp/"


def getTree():
    requests.packages.urllib3.disable_warnings()
    response = requests.get(url=url, headers=headers)
    return etree.HTML(response.text)


def changeName(contestName):
    # print(contestName)
    # ALGO ARTIS Programming Contest 2022（AtCoder Heuristic Contest 010）
    for index in range(len(contestName)):
        if contestName[index] == '（':
            return contestName[index + 1:-1]

    return contestName


def changeTime(contestTime):
    contestTime1 = contestTime[0:11]
    contestTime2 = str(int(contestTime[11:13]) - 1)
    contestTime3 = contestTime[13:19]
    return contestTime1 + contestTime2 + contestTime3
    # print(contestTime1 + contestTime2 + contestTime3)


def getContestsList():
    tree = getTree();
    contestsList = tree.xpath('//div[@id="contest-table-upcoming"]/div/table/tbody/tr')
    contestList = []

    for contest in contestsList:
        # contest = contestsList[i]
        contestMap = {}
        # 2022-04-24 15:00:00+0900
        contestTime = str(contest.xpath('./td[1]//time/text()')[0])
        contestTime = changeTime(contestTime)

        contestName = contest.xpath('./td[2]//a/text()')[0]
        contestName = changeName(contestName)

        contestURL = contest.xpath('./td[2]/small/a/@href')[0]
        contestID = contestURL[10:]
        contestURL = 'https://atcoder.jp' + contestURL

        contestMap['name'] = contestName
        contestMap['time'] = contestTime
        contestMap['id'] = contestID
        contestMap['url'] = contestURL
        contestList.append(contestMap)
    contestMap = {}
    contestList.append(contestMap)

    return contestList
