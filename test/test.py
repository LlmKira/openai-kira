# -*- coding: utf-8 -*-
# @Time    : 1/2/23 1:31 AM
# @FileName: test.py
# @Software: PyCharm
# @Github    ：sudoskys
import asyncio

# 最小单元测试
import src.openai_kira as openai_kira
import setting

print(openai_kira.RedisConfig())

openai_kira.setting.openaiApiKey = setting.ApiKey

print(openai_kira.setting.openaiApiKey)


async def completion():
    try:
        response = await openai_kira.Completion().create(model="text-davinci-003",
                                                         prompt="Say this is a test",
                                                         temperature=0,
                                                         max_tokens=20)
        # TEST
        print(response)
        print(type(response))
    except Exception as e:
        print(e)
        if "Incorrect API key provided" in str(e):
            print("OK", e)
        else:
            print("NO", e)


receiver = openai_kira.Chat.Chatbot(
    conversation_id=-10086,
    call_func=None,  # Api_keys.pop_api_key,
    start_sequ="Ai:",
    restart_sequ="Human:",
)


async def chat():
    response = await receiver.get_chat_response(model="text-davinci-003",
                                                prompt="我爱你啊",
                                                max_tokens=500,
                                                role="你扮演",
                                                web_enhance_server={"time": ""},
                                                optimizer=openai_kira.Chat.Optimizer.MatrixPoint
                                                )
    print(response)


async def Moderation():
    response = await openai_kira.Moderations().create(input="Kill You！")
    print(response)


async def Sentiment():
    _sentence_list = [
        "你是？",
        "我没那么多时间也懒得自己",
        "什么是？",
        "玉玉了，紫砂了",
        "我知道了",
        "主播抑郁了，自杀了",
        "公主也能看啊",
        "换谁都被吓走吧"
    ]
    for item in _sentence_list:
        print(item)
        response = openai_kira.utils.Talk.Talk.sentiment(item)
        print(response)


# asyncio.run(completion())
# asyncio.run(chat())
# asyncio.run(Moderation())
asyncio.run(Sentiment())
