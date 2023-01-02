# openai-kira

Openai GPT3 ChatBot 框架包，在未公开前快速实现类 ChatGPT接入（公开后就接入chatGPT），打包成依赖的玩具。提供 redis 和 文件数据库
两个选择。

## Use

`pip install -U openai-kira`

**init**

```python
import openai_kira

# 
openai_kira.setting.redisSetting = openai_kira.setting.RedisConfig()
openai_kira.setting.dbFile = "openai_msg.db"
openai_kira.setting.openaiApiKey = ["key", "key2"]
openai_kira.setting.proxyUrl = None  # "127.0.0.1"
# 插件的设置
openai_kira.setting.webServerUrlFilter = False
openai_kira.setting.webServerStopSentence = ["广告", "营销号"]
```

## Exp

```python
import asyncio

import openai_kira
from openai_kira import Chat

print(openai_kira.RedisConfig())
openai_kira.setting.openaiApiKey = ["key"]

receiver = Chat.Chatbot(
    conversation_id=10086,
    call_func=None,  # Api_keys.pop_api_key,
    start_sequ="Ai:",
    restart_sequ="Human:",
)


async def main():
    response = await receiver.get_chat_response(model="text-davinci-003",
                                                prompt="你好",
                                                max_tokens=500,
                                                role="你扮演...",
                                                web_enhance_server={"time": ""}
                                                )
    print(response)


asyncio.run(main())
```

```python
import asyncio
import openai_kira

print(openai_kira.RedisConfig())
openai_kira.setting.openaiApiKey = ["key"]
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
```

## Plugin

**Table**

| plugins   | desc              | value/server                                          | use                                   |
|-----------|-------------------|-------------------------------------------------------|---------------------------------------|
| `time`    | now time          | `""`,no need                                          | `明昨今天`....                            |
| `week`    | week time         | `""`,no need                                          | `周几` .....                            |
| `search`  | Web Search        | `["some.com?searchword={}"]`,must need                | `查询` `你知道` len<80 / end with`?`len<15 |
| `duckgo`  | Web Search        | `""`,no need,but need `pip install duckduckgo_search` | `查询` `你知道` len<80 / end with`?`len<15 |
| `details` | answer with steps | `""`,no need                                          | Ask for help `how to`                 |

## Plugin dev

There is a middleware between the memory pool and the analytics that provides some networked retrieval support and
operational support. It can be spiked with services that interface to other Api's.

**Prompt Injection**

Use `""` `[]` to emphasise content.

### Exp

First create a file in `openai_kira/Chat/module/plugin` without underscores (`_`) in the file name.

**Template**

```python
from ..platform import ChatPlugin, PluginConfig
from ._plugin_tool import PromptTool
import os
from loguru import logger

modulename = os.path.basename(__file__).strip(".py")


@ChatPlugin.plugin_register(modulename)
class Week(object):
    def __init__(self):
        self._server = None
        self._text = None
        self._time = ["time", "多少天", "几天", "时间", "几点", "今天", "昨天", "明天", "几月", "几月", "几号",
                      "几个月",
                      "天前"]

    def requirements(self):
        return []

    async def check(self, params: PluginConfig) -> bool:
        if PromptTool.isStrIn(prompt=params.text, keywords=self._time):
            return True
        return False

    async def process(self, params: PluginConfig) -> list:
        _return = []
        self._text = params.text
        # 校验
        if not all([self._text]):
            return []
        # GET
        from datetime import datetime, timedelta, timezone
        utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
        bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
        now = bj_dt.strftime("%Y-%m-%d %H:%M")
        _return.append(f"Current Time UTC8 {now}")
        # LOGGER
        logger.trace(_return)
        return _return
```

`openai_kira/Chat/module/plugin/_plugin_tool.py` provides some tool classes, PR is welcome

**Testing**

You cannot test directly from within the module package, please run the `openai_kira/Chat/test_module.py` file to test
the module, with the prompt matching check.

Alternatively, you can safely use `from loguru import logger` + `logger.trace(_return)` in the module to debug the
module variables and the trace level logs will not be output by the production environment.

## 结构

```markdown
.
└── openai_kira
├── api
│ ├── api_url.json
│ ├── api_utils.py
│ ├── network.py
├── Chat
│ ├── __init__.py
│ ├── module
│ ├── Summer.py
│ ├── test_module.py
│ ├── text_analysis_tools
│ └── vocab.json
├── __init__.py
├── requirements.txt
├── resouce
│ ├── completion.py
│ ├── __init__.py
└── utils
├── data.py
├── Network.py
└── Talk.py
```

## EULA(end-user-license-agreement)

**cn**

1. 自行因为不当操作导致的损失。
2. 本项目并非官方项目。
3. 因为安全事故导致的损失我不负责。
4. 如果你愿意，可以赞助我。

**en**

1. the damage caused by improper operation on its own.
2. This is not an official project.
3. I am not responsible for any damage caused by safety incidents.
4. you can sponsor me if you wish.
