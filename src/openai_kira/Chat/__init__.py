# -*- coding: utf-8 -*-
# @Time    : 12/6/22 12:02 PM
# @FileName: chat.py
# @Software: PyCharm
# @Github    ：sudoskys

import json
import os
import random
from .Optimizer import SinglePoint, convert_msgflow_to_list
# 基于 Completion 上层
from ..resouce import Completion
from ..utils import setting
# Tool
from ..utils.Talk import Talk
from ..utils.data import MsgFlow
from loguru import logger


class Chatbot(object):
    def __init__(self,
                 api_key: str = None,
                 conversation_id: int = 1,
                 token_limit: int = 3700,
                 restart_sequ: str = "\nSomeone:",
                 start_sequ: str = "\nReply:",
                 call_func=None
                 ):
        """
        chatGPT 的实现由上下文实现，所以我会做一个存储器来获得上下文
        :param api_key: api key
        :param conversation_id: 对话 ID
        :param token_limit: 总限制
        :param restart_sequ: Human
        :param start_sequ: Ai
        :param call_func: 回调
        """
        if api_key is None:
            api_key = setting.openaiApiKey
        if isinstance(api_key, list):
            api_key: list
            if not api_key:
                raise RuntimeError("NO KEY")
            api_key = random.choice(api_key)
            api_key: str
        self.__api_key = api_key
        if not api_key:
            raise RuntimeError("NO KEY")
        self.conversation_id = str(conversation_id)
        self._MsgFlow = MsgFlow(uid=self.conversation_id)
        self._start_sequence = start_sequ
        self._restart_sequence = restart_sequ
        # 防止木头
        if not self._start_sequence.strip().endswith(":"):
            self._start_sequence = self._start_sequence + ":"
        if not self._restart_sequence.strip().endswith(":"):
            self._restart_sequence = self._restart_sequence + ":"
        self.__call_func = call_func
        self.__token_limit = token_limit

    def reset_chat(self):
        # Forgets conversation
        return self._MsgFlow.forget()

    def record_message(self, ask, reply):
        """
        随意填充消息桶
        """
        _msg = {"weight": [], "ask": f"{ask}", "reply": f"{reply}"}
        # 存储成对的对话
        self._MsgFlow.saveMsg(msg=_msg)
        return _msg

    def read_memory(self, plain_text: bool = False, sign: bool = False) -> list:
        """
        读取记忆桶
        :param sign: 是否签名
        :param plain_text: 是否转化为列表
        """
        _result = self._MsgFlow.read()
        if plain_text:
            _result = convert_msgflow_to_list(msg_list=_result, sign=sign)
        return _result

    def record_dialogue(self, prompt, response):
        """
        回复填充进消息桶
        """
        REPLY = []
        Choice = response.get("choices")
        if Choice:
            for item in Choice:
                _text = item.get("text")
                REPLY.append(_text)
        if not REPLY:
            REPLY = [""]
        # 构建一轮对话场所
        _msg = {"weight": [], "ask": f"{self._restart_sequence}{prompt}", "reply": f"{self._start_sequence}{REPLY[0]}"}
        # 存储成对的对话
        self._MsgFlow.saveMsg(msg=_msg)
        return _msg

    def get_conversation_hash(self):
        import hashlib
        my_string = str(self.conversation_id)
        # 使用 hashlib 模块中的 sha256 算法创建一个散列对象
        hash_object = hashlib.sha256(my_string.encode())
        return hash_object.hexdigest()

    @staticmethod
    def zip_str(_item):
        # 读取字典
        path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), ".", "vocab.json")
        )
        with open(path, encoding="utf8") as f:
            target = json.loads(f.read())
        # 遍历字典键值对
        for key, value in target.items():
            # 使用 str.replace() 方法替换字符串中的键
            _item = _item.replace(key, value)
        return _item

    async def get_chat_response(self,
                                prompt: str,
                                max_tokens: int = 500,
                                model: str = "text-davinci-003",
                                character: list = None,
                                head: str = None,
                                role: str = "",
                                optimizer: Optimizer = None,
                                web_enhance_server: dict = None) -> dict:
        """
        异步的，得到对话上下文
        :param web_enhance_server: {"type":["https://www.exp.com/search?q={}"]} 格式如此
        :param role:
        :param head: 预设技巧
        :param max_tokens: 限制返回字符数量
        :param model: 模型选择
        :param prompt: 提示词
        :param optimizer: 优化器
        :param character: 性格提示词，列表字符串
        :return:
        """
        # 预设
        if optimizer is None:
            optimizer = Optimizer.MatrixPoint
        if character is None:
            character = ["educated", "clever", "friendly", "lovely", "talkative",
                         "omniscient", "awesome"]
        _character = ",".join(character)
        _role = f"With {self._start_sequence.strip(':')},她是{_character}的助手.\n"
        if role:
            if 7 < len(f"{role}") < 500:
                _role = f"With awesome clever {self._start_sequence}{role}.\n"
        if head is None:
            head = f"{self._restart_sequence}让我们开始.\n"
        _header = f"{_role}{head}"
        # 构建主体
        _prompt_s = [f"{self._restart_sequence}{prompt}."]
        _prompt_memory = self.read_memory(plain_text=False)
        # 占位限制
        _extra_token = int(
            len(_prompt_memory) +
            Talk.tokenizer(self._start_sequence) +
            max_tokens +
            Talk.tokenizer(_header + _prompt_s[0]))
        _prompt_list = []
        # 中间件
        _appendix = await self.Prehance(prompt=prompt, table=web_enhance_server)
        start_token = int(Talk.tokenizer(_appendix))
        _prompt_list.append(_appendix)
        # 记忆池策略
        _prompt_apple = optimizer(
            prompt=prompt,
            start_token=start_token,
            memory=_prompt_memory,
            extra_token=_extra_token,
            token_limit=self.__token_limit,
        ).run()
        #
        _prompt_list.extend(_prompt_apple)
        _prompt_list.extend(_prompt_s)
        # 拼接提示词汇
        _prompt = '\n'.join(_prompt_list) + f"\n{self._start_sequence}"
        # 重切割
        _limit = self.__token_limit - max_tokens - Talk.tokenizer(_header)
        _mk = _limit if _limit > 0 else 0
        while Talk.tokenizer(_prompt) > _mk:
            _prompt = _prompt[1:]
        _prompt = _header + _prompt
        # print(_prompt)
        # 响应
        response = await Completion(api_key=self.__api_key, call_func=self.__call_func).create(
            model=model,
            prompt=_prompt,
            temperature=0.9,
            max_tokens=max_tokens,
            top_p=1,
            n=1,
            frequency_penalty=0,
            presence_penalty=0.5,
            user=str(self.get_conversation_hash()),
            stop=[f"{self._start_sequence}", f"{self._restart_sequence}"],
        )
        self.record_dialogue(prompt=prompt, response=response)
        return response

    async def Prehance(self, table: dict, prompt: str) -> str:
        _append = "-"
        _return = []
        if not all([table, prompt]):
            return _append
        from .module.platform import ChatPlugin, PluginParam
        processor = ChatPlugin()
        for plugin in table.keys():
            processed = await processor.process(param=PluginParam(text=prompt, server=table), plugins=[plugin])
            _return.extend(processed)
        reply = "\n".join(_return) if _return else ""
        reply = reply[:700]
        logger.debug(f"AllPluginReturn:{reply}")
        return reply


# OLD
"""

    @staticmethod
    def str_prompt(prompt: str) -> list:
        range_list = prompt.split("\n")

        # 如果当前项不包含 `:`，则将其并入前一项中
        result = [range_list[i] + range_list[i + 1] if ":" not in range_list[i] else range_list[i] for i in
                  range(len(range_list))]
        # 使用列表推导式过滤掉空白项
        filtered_result = [x for x in result if x != ""]
        # 输出处理后的结果
        return filtered_result
"""
