from config import client, MODEL
from modules.planner import Planner
from modules.tool_caller import ToolCaller
from modules.executor import Executor
from modules.self_repair import SelfRepair
from tools.code_executor import execute_code
from tools.file_ops import write_file, read_file

class DoubaoCodeAgent:
    def __init__(self, max_repair=2):
        self.planner = Planner(client, MODEL)
        self.tool_caller = ToolCaller(client, MODEL)
        self.executor = Executor()
        self.self_repair = SelfRepair(client, MODEL, max_repair)
        self.tools = {
            "execute_code": execute_code,
            "write_file": write_file,
            "read_file": read_file
        }

    def run(self, user_query: str) -> str:
        print("🔍 任务规划...")
        plan = self.planner.generate_plan(user_query)
        
        print("🛠️ 开始执行...")
        result = self._execute_with_repair(plan, user_query)
        
        print("✅ 最终结果生成完成")
        return result

    def _execute_with_repair(self, plan: str, original_query: str):
        for attempt in range(self.self_repair.max_repair + 1):
            execution_result = self.tool_caller.execute_plan(plan, self.tools)
            
            if execution_result["success"]:
                return execution_result["final_code"]
            
            if attempt == self.self_repair.max_repair:
                return f"❌ 执行失败（已修复{attempt}次）\n{execution_result['error']}"
            
            print(f"🔄 第{attempt+1}次自我修复...")
            plan = self.self_repair.repair(plan, execution_result["error"], original_query)
        
        return "执行完成"