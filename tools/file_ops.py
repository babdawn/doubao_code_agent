import os
from pathlib import Path

def write_file(path: str, content: str) -> dict:
    Path(path).write_text(content, encoding="utf-8")
    return {"success": True, "message": f"文件已写入: {path}"}

def read_file(path: str) -> dict:
    return {"success": True, "content": Path(path).read_text(encoding="utf-8")}