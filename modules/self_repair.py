from config import client, MODEL

class SelfRepair:
    def __init__(self, client, model, max_repair=2):
        self.client = client
        self.model = model
        self.max_repair = max_repair

    def repair(self, old_plan: str, error_msg: str, original_query: str) -> str:
        """自我修复"""
        repair_prompt = f"""【原任务】
{original_query}

【之前的执行计划】
{old_plan}

【执行错误信息】
{error_msg}

请作为专业代码调试专家，仔细分析错误原因，给出**修复后的完整执行计划**和修正后的正确代码。"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个经验丰富的代码自我修复专家，擅长诊断错误并生成修正代码。"},
                {"role": "user", "content": repair_prompt}
            ],
            temperature=0.2,
            max_tokens=2500
        )
        return response.choices[0].message.content