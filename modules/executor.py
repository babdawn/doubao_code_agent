class Executor:
    def __init__(self):
        pass

    def verify(self, code: str) -> dict:
        """代码验证（可后续扩展）"""
        from tools.code_executor import execute_code
        result = execute_code(code)
        
        return {
            "success": result["success"],
            "output": result.get("stdout", ""),
            "error": result.get("stderr", "")
        }