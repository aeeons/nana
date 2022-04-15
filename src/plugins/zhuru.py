from nonebot import on_command, on_regex
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
import time
import requests, json

zhuru = on_command("注入")


@zhuru.handle()
async def zhuru(bot: Bot, event: Event, state: dict):
    strr = "[4] 「唔 注入进来了www」\n"
    await bot.send(
        event=event,
        message=strr
    )
