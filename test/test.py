# -*- coding: utf-8 -*-
# @Time    : 1/2/23 1:31 AM
# @FileName: test.py
# @Software: PyCharm
# @Github    ：sudoskys
import asyncio
import os

# 最小单元测试
import src.openai_kira as openai_kira

openai_kira.setting.openaiApiKey = ["122"]

print(openai_kira.setting.openaiApiKey)


async def main():
    response = await openai_kira.Completion().create(model="text-davinci-003",
                                                     prompt="Say this is a test",
                                                     temperature=0,
                                                     max_tokens=20)
    # TEST
    print(response)
    print(type(response))


asyncio.run(main())
