# openai-kira

Openai GPT3 ChatBot 框架包，在未公开前快速实现类 ChatGPT接入（公开后就接入chatGPT），打包成依赖的玩具。提供 redis 和 文件数据库
两个选择，非常好工作。

## 使用

`pip install -U openai-kira`

**init**

```python
import openai_kira
# 
openai_kira.setting.redisSetting = openai_kira.setting.RedisConfig()
openai_kira.setting.dbFile = "openai_msg.db"
openai_kira.setting.openaiApiKey = ["key","key2"]
openai_kira.setting.proxyUrl =None # "127.0.0.1"
# 插件的设置
openai_kira.setting.webServerUrlFilter = False
openai_kira.setting.webServerStopSentence = ["广告", "营销号"]
```

## 实例

```python
from openai_kira import Chat

receiver = Chat.Chatbot(
    conversation_id="10086",
    call_func=None,  # Api_keys.pop_api_key,
    start_sequ=None,
    restart_sequ=None,
)
response = await receiver.get_chat_response(model="text-davinci-003",
                                            prompt="你好",
                                            max_tokens=500,
                                            role="你扮演...",
                                            web_enhance_server={"time": ""}
                                            )
```

```python
import openai_kira

response = await openai_kira.Completion(call_func=None).create(
    model="text-davinci-003",
    prompt=str("你好"),
    temperature=0.2,
    frequency_penalty=1,
    max_tokens=500
)
```

## 插件

**目前的插件**

| plugins   | desc      | value/server                                          | use                                   |
|-----------|-----------|-------------------------------------------------------|---------------------------------------|
| `time`    | now time  | `""`,no need                                          | `明昨今天`....                            |
| `week`    | week time | `""`,no need                                          | `周几` .....                            |
| `search`  | 搜索引擎支持    | `["some.com?searchword={}"]`,must need                | `查询` `你知道` len<80 / end with`?`len<15 |
| `duckgo`  | 搜索引擎支持    | `""`,no need,but need `pip install duckduckgo_search` | `查询` `你知道` len<80 / end with`?`len<15 |
| `details` | 分步回答问题    | `""`,no need                                          | Ask for help `how to`                 |

## 插件开发

`openai_kira/Chat/module/plugin` 的插件提供外部链接支持。

在记忆池和分析 之间有一个 中间件，可以提供一定的联网检索支持和操作支持。可以对接其他 Api 的服务进行加料。

**Prompt Injection**

使用 `“”` `[]` 来强调内容，获得可能的支持。

### 开发技巧

首先在 `openai_kira/Chat/module/plugin` 创建一个文件，文件名不要带下划线（`_`）。

**模板**

```python
from ..platform import ChatPlugin, PluginConfig
from ._plugin_tool import PromptTool
import os
from loguru import logger

modulename = os.path.basename(__file__).strip(".py")


# 注册插件
@ChatPlugin.plugin_register(modulename)
class Week(object):
    def __init__(self):
        """属性"""
        self._server = None
        self._text = None
        self._week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        self._week_key = ["星期", "星期几", "时间", "周几", "周一", "周二", "周三", "周四", "周五", "周六"]

    def requirements(self):
        return []

    async def check(self, params: PluginConfig) -> bool:
        """
        条件方法
        """
        if PromptTool.isStrIn(prompt=params.text, keywords=self._week_list + self._week_key):
            return True
        return False

    async def process(self, params: PluginConfig) -> list:
        """处理数据，返回列表，请自行进行错误处理！"""
        _return = []
        self._text = params.text
        # 校验
        if not all([self._text]):
            return []
        # GET
        from datetime import datetime, timedelta, timezone
        utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
        bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
        onw = bj_dt.weekday()
        _return.append(f"Now {self._week_list[onw]}")
        # LOGGER
        logger.trace(_return)
        return _return
```

`openai_kira/Chat/module/plugin/_plugin_tool.py` 提供了一些工具类，欢迎 PR

**测试**

你无法在模块包内直接测试，请运行 `openai_kira/Chat/test_module.py` 文件测试模块，prompt 要符合 check。

另外，你可以在模块中放心使用 `from loguru import logger` + `logger.trace(_return)` 来调试查看模块变量，trace
等级的日志不会被生产环境输出。

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
