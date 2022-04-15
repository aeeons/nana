import json
import random
import os
import nonebot
import requests
import base64
import io
from aiocqhttp import MessageSegment
from nonebot import require
from nonebot.adapters.cqhttp import Bot, Event, Message

scheduler = require('nonebot_plugin_apscheduler').scheduler


@scheduler.scheduled_job('cron', hour='01', minute='10', id='yincha')
async def yincha():
    (bot,) = nonebot.get_bots().values()
    await bot.send_msg(
        message_type="group",
        group_id=int(1124693419),
        message='三点几嚟，做碌鸠啊做！做这么多，老板不会心疼你的,饮茶先啦！'
    )
