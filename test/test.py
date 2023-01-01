# -*- coding: utf-8 -*-
# @Time    : 1/2/23 1:31 AM
# @FileName: test.py
# @Software: PyCharm
# @Github    ：sudoskys
import asyncio

# 最小单元测试
import src.openai_kira as openai_kira

print(openai_kira.RedisConfig())
openai_kira.setting.openaiApiKey = ["122"]

print(openai_kira.setting.openaiApiKey)


async def main():
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
        if "Incorrect API key provided" in e:
            print("OK")
        else:
            print("NO")


asyncio.run(main())
