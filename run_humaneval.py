# run_humaneval.py — 放在 doubao_code_agent 根目录
import re
from human_eval.data import write_jsonl, read_problems
from human_eval.execution import check_correctness

from agent import DoubaoCodeAgent

# 单次测试执行超时（秒），与 human-eval 常见设置一致
EXECUTION_TIMEOUT = 3.0


def _extract_code_block(text: str) -> str:
    """从模型输出中提取 Python 代码（优先 ```python，否则任意 ```）。"""
    if not text:
        return ""
    if "```python" in text.lower():
        m = re.search(
            r"```python\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE
        )
        if m:
            return m.group(1).strip()
    if "```" in text:
        m = re.search(r"```\s*\w*\s*(.*?)\s*```", text, re.DOTALL)
        if m:
            return m.group(1).strip()
    return text.strip()


def _humaneval_completion_suffix(problem: dict, generated: str) -> str:
    """
    human_eval 要求传入的 completion 仅为接在 problem['prompt'] 之后的续写。
    若模型重复输出了整段 prompt 或整函数，则剥去重复前缀。
    """
    g = _extract_code_block(generated)
    if not g:
        return "    pass  # empty\n"

    p = problem["prompt"]
    pn = p.replace("\r\n", "\n")
    gn = g.replace("\r\n", "\n")

    while gn.startswith(pn):
        gn = gn[len(pn) :].lstrip("\n\r")

    return gn if gn.endswith("\n") else gn + "\n"


def generate_completion_suffix(problem: dict, agent: DoubaoCodeAgent) -> str:
    """调用 Agent，返回可供 human_eval 使用的 completion 后缀（不含 problem['prompt']）。"""
    prompt = f"""请根据以下函数描述，生成完整的可运行 Python 函数代码。
只需要输出函数实现，不要加额外解释。

{problem['prompt']}

函数签名已给出，请补全函数体。"""

    try:
        generated = agent.run(prompt)
        return _humaneval_completion_suffix(problem, generated)
    except Exception as e:
        print(f"生成失败: {e}")
        return "    pass  # 生成失败\n"


def evaluate_on_humaneval(samples: int = 164, max_repair: int = 2) -> float:
    problems = read_problems()
    problems = dict(list(problems.items())[:samples])

    agent = DoubaoCodeAgent(max_repair=max_repair)

    results = []
    correct_count = 0

    print(
        f"开始 HumanEval 评测 ({samples} 个问题, 自我修复次数: {max_repair})...\n"
    )

    for task_id, problem in problems.items():
        print(f"正在处理 {task_id} ...")
        suffix = generate_completion_suffix(problem, agent)
        check_result = check_correctness(
            problem, suffix, timeout=EXECUTION_TIMEOUT
        )

        passed = check_result["passed"]
        full_source = problem["prompt"] + suffix
        results.append(
            {
                "task_id": task_id,
                "completion": full_source,
                "passed": passed,
                "harness_result": check_result.get("result"),
            }
        )

        if passed:
            correct_count += 1

        rate = correct_count / len(results)
        status = "通过" if passed else "未通过"
        detail = ""
        if not passed and check_result.get("result"):
            detail = f"  ({check_result['result']})"
        print(f"  → {status}  当前通过率: {rate:.1%}{detail}\n")

    pass_rate = correct_count / len(results) * 100
    print("\nHumanEval 评测完成")
    print(f"通过数: {correct_count}/{len(results)}")
    print(f"通过率 (pass@1): {pass_rate:.2f}%")

    write_jsonl("humaneval_results.jsonl", results)
    return pass_rate


if __name__ == "__main__":
    evaluate_on_humaneval(samples=20, max_repair=2)
    # evaluate_on_humaneval(samples=164, max_repair=2)
