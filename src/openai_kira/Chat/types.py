# -*- coding: utf-8 -*-
# @Time    : 1/8/23 11:00 AM
# @FileName: types.py
# @Software: PyCharm
# @Github    ：sudoskys
from pydantic import BaseModel


class MemeryItem(BaseModel):
    ask: str
    reply: str
    weight: list = []
