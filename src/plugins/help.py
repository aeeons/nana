from nonebot import on_command, on_regex
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
import time
import requests, json

pattern = '查询&#91;(\d*-{0,1}\d*)\&#93;'


def load_json(path):
    lines = []  # 第一步：定义一个列表， 打开文件
    with open(path, encoding='utf-8') as f:
        for row in f.readlines():  # 第二步：读取文件内容
            lines.append(row)  # 第四步：将过滤后的行添加到列表中.
    return json.loads("\n".join(lines))


query = on_regex(pattern, flags=0, rule=None)


@query.handle()
async def queryCommand(bot: Bot, event: Event, state: dict):
    result = load_json("/root/nana/src/plugins/commandList.json")
    sendStr = "[1] "
    id = state['_matched_groups'][0]
    if id in result:
        sendStr = sendStr + result[id]['introduce']
        await bot.send(
            event=event,
            message=sendStr
        )
    else:
        sendStr = sendStr + "没有这个命令哦"
        await bot.send(
            event=event,
            message=sendStr
        )
