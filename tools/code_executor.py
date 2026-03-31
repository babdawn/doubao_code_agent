import subprocess
import tempfile
import os
from pathlib import Path

def execute_code(code: str, timeout: int = 30) -> dict:
    """安全执行Python代码"""
    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = Path(tmpdir) / "exec.py"
        script_path.write_text(code, encoding="utf-8")
        
        try:
            result = subprocess.run(
                ["python", str(script_path)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=tmpdir
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "code": code
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "执行超时"}
        except Exception as e:
            return {"success": False, "error": str(e)}