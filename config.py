import os
from openai import OpenAI

# ARK_API_KEY = os.getenv("ARK_API_KEY")  # 在终端 export ARK_API_KEY=your_key
ARK_API_KEY = "7127d0a4-41ea-4f7b-9a37-92d302011e08"
MODEL = "doubao-seed-1-8-251228"               # 替换为你创建的推理接入点 Model ID

client = OpenAI(
    api_key=ARK_API_KEY,
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)