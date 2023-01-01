# -*- coding: utf-8 -*-
# @Time    : 12/5/22 9:54 PM
# @FileName: __init__.py
# @Software: PyCharm
# @Github    ：sudoskys
from .Chat import Chatbot
from .resouce import Completion

from .setting import RedisConfig
from .setting import openaiApiKey, redisSetting, dbFile, proxyUrl, webServerUrlFilter, webServerStopSentence

RedisConfig = RedisConfig
openaiApiKey = openaiApiKey
redisSetting = redisSetting
dbFile = dbFile
proxyUrl = proxyUrl
webServerUrlFilter = webServerUrlFilter
webServerStopSentence = webServerStopSentence
