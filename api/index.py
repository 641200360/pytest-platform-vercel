# 文件路径: api/index.py

import subprocess
import sys
import os
from flask import Flask, jsonify, render_template_string

# Vercel 会自动寻找名为 'app' 的 Flask 实例
app = Flask(__name__)


@app.route('/')
def index():
    """
    渲染主页面，包含完整的 HTML 和 JavaScript 前端代码。
    """
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>自动化测试平台</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 20px; background-color: #f4f4f9; }
            h1 { text-align: center; color: #333; }
            #run-button { display: block; width: 200px; margin: 20px auto; padding: 12px; font-size: 16px; color: white; background-color: #007bff; border: none; border-radius: 5px; cursor: pointer; }
            #run-button:disabled { background-color: #aaa; }
            #results { margin-top: 30px; background-color: #2d333b; color: #cdd9e5; padding: 15px; border-radius: 5px; white-space: pre-wrap; font-family: "SF Mono", "Consolas", "Liberation Mono", Menlo, Courier, monospace; }
        </style>
    </head>
    <body>
        <h1>自动化测试平台原型</h1>
        <button id="run-button" onclick="runTests()">开始运行测试</button>
        <div id="results">点击按钮开始测试...</div>

        <script>
            async function runTests() {
                const button = document.getElementById('run-button');
                const resultsDiv = document.getElementById('results');

                // 禁用按钮并显示加载状态
                button.disabled = true;
                resultsDiv.textContent = '测试正在运行中，请稍候...';

                try {
                    // 调用后端的 /run-tests 接口
                    const response = await fetch('/run-tests');
                    const data = await response.json();

                    // 将后端返回的测试输出显示在页面上
                    resultsDiv.textContent = data.output;
                } catch (error) {
                    resultsDiv.textContent = '请求失败: ' + error;
                    console.error('Error:', error);
                } finally {
                    // 重新启用按钮
                    button.disabled = false;
                }
            }
        </script>
    </body>
    </html>
    """)


@app.route('/run-tests')
def run_tests():
    """
    这个接口会调用系统的命令行来执行 pytest。
    """
    try:
        # 使用健壮的方式定位 tests 文件夹，确保在 Vercel 环境中也能找到
        # __file__ 指的是当前文件(index.py)的路径
        # os.path.dirname(__file__) 是 /api 文件夹的路径
        # os.path.join(..., '..', 'tests') 表示从 /api 文件夹向上一级，再进入 tests 文件夹
        tests_dir = os.path.join(os.path.dirname(__file__), '..', 'tests')
        command = [sys.executable, '-m', 'pytest', tests_dir]
        
        # 复制当前环境变量，并强制设置 Python I/O 编码为 UTF-8
        # 这能确保 pytest 的输出流是 UTF-8，解决部署后的中文乱码问题
        run_env = os.environ.copy()
        run_env['PYTHONIOENCODING'] = 'UTF-8'

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=run_env
        )

        # 因为我们确保了输出是 UTF-8，所以可以直接用 'utf-8' 来解码
        stdout_str = result.stdout.decode('utf-8', errors='replace')
        stderr_str = result.stderr.decode('utf-8', errors='replace')

        full_output = stdout_str + stderr_str
        
        return jsonify({'output': full_output})

    except Exception as e:
        return jsonify({'output': f"执行测试时发生错误: {str(e)}"})

# 注意: 本地启动的 if __name__ == '__main__': app.run(...) 代码块已被移除
