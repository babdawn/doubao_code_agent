from config import client, MODEL

class ToolCaller:
    def __init__(self, client, model):
        self.client = client
        self.model = model

    def execute_plan(self, plan: str, tools: dict) -> dict:
        """从计划中提取代码并执行"""
        import re
        
        # 提取所有Python代码块
        code_blocks = re.findall(r'```python(.*?)```', plan, re.S)
        
        if not code_blocks:
            return {
                "success": False, 
                "error": "计划中未找到可执行的Python代码块",
                "final_code": ""
            }
        
        final_code = code_blocks[-1].strip()  # 执行最后一个代码块
        
        # 执行代码
        from tools.code_executor import execute_code
        result = execute_code(final_code)
        
        if result["success"]:
            return {
                "success": True,
                "final_code": final_code,
                "output": result.get("stdout", "")
            }
        else:
            return {
                "success": False,
                "error": result.get("stderr") or result.get("error", "执行失败"),
                "final_code": final_code
            }