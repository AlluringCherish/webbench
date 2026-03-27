import os
from typing import List

def read_file_lines(filepath: str) -> List[str]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.readlines()

def write_file_lines_atomic(filepath: str, lines: List[str]) -> None:
    temp_path = filepath + '.tmp'
    with open(temp_path, 'w', encoding='utf-8') as f:
        for line in lines:
            if not line.endswith('\n'):
                line += '\n'
            f.write(line)
    os.replace(temp_path, filepath)
