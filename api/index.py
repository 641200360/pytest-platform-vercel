# 文件路径: api/index.py

import subprocess
import sys
import os
from flask import Flask, jsonify, render_template_string

# Vercel 会自动寻找名为 'app' 的 Flask 实例
app = Flask(__name__)


@app.route('/')
def index():
    # ... (前端HTML代码保持不变) ...
    return render_template_string("""
    <!DOCTYPE html>
    <!-- ... 省略您之前的HTML和JavaScript代码 ... -->
    </html>
    """)


@app.route('/run-tests')
def run_tests():
    # 告诉 Vercel pytest 的目标文件夹在哪里
    # os.path.realpath('') 会获取当前工作目录的绝对路径
    test_dir = os.path.join(os.path.realpath(''), 'tests')
    command = [sys.executable, '-m', 'pytest', test_dir]

    run_env = os.environ.copy()
    run_env['PYTHONIOENCODING'] = 'UTF-8'

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=run_env
    )

    stdout_str = result.stdout.decode('utf-8', errors='replace')
    stderr_str = result.stderr.decode('utf-8', errors='replace')

    full_output = stdout_str + stderr_str

    return jsonify({'output': full_output})

# 注意：本地启动的 app.run() 代码块已移除
