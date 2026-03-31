from config import client, MODEL

class Planner:
    def __init__(self, client, model):
        self.client = client
        self.model = model

    def generate_plan(self, user_query: str) -> str:
        """生成任务执行计划"""
        system_prompt = """你是一个专业的代码任务规划器。
将用户需求分解为清晰、可执行的步骤序列。
每个步骤必须指明要使用的工具。
输出格式严格按照以下示例：

步骤1: 理解需求并规划算法
工具: execute_code
代码: ```python
# 这里写代码

步骤2: 测试代码
工具: execute_code
代码: ```python
测试代码
text"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content