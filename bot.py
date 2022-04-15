#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

# Custom your logger
#
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)
from apscheduler.schedulers.background import BackgroundScheduler

# You can pass some keyword args config to init function
nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

nonebot.load_builtin_plugins()
nonebot.load_plugins("src/plugins")
nonebot.load_from_toml("pyproject.toml")

# Please DO NOT modify this file unless you know what you are doing!
# As an alternative, you should use command `nb` or modify `pyproject.toml` to load plugins

CQHTTP_WS_URLS = {"2429903694": "ws://127.0.0.1:8080/"}

if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
    nonebot.init(apscheduler_autostart=True)
    nonebot.init(apscheduler_config={
        "apscheduler.timezone": "Asia/Shanghai"
    })
