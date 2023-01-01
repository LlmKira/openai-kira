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
