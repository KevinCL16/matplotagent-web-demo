import shutil
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sys
from workflow import mainworkflow
import os
import json
import base64
import io

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# Load benchmark instructions
with open('benchmark_data/benchmark_instructions.json', 'r') as f:
    benchmark_instructions = json.load(f)


@app.route('/')
def index():
    return render_template('index_dynamic.html')


@socketio.on('run_benchmark')
def handle_benchmark(data):
    benchmark_id = data.get('id')
    custom_query = data.get('query')
    model = data.get('model', 'gpt-4o')  # 默认使用 gpt-4o

    if custom_query:
        # 处理自定义查询
        workspace = f"D:\ComputerScience\CODES\MatPlotAgent-main\workspace\custom_query"
        instruction = custom_query
        emit('instruction_update', {'instruction': instruction})
    elif benchmark_id and 1 <= int(benchmark_id) <= 100:
        # 处理benchmark
        instruction = benchmark_instructions[int(benchmark_id) - 1]
        workspace = f"D:\ComputerScience\CODES\MatPlotAgent-main\workspace\example_{benchmark_id}"
        emit('instruction_update', {'instruction': instruction['simple_instruction']})
    else:
        emit('error', {'error': '请提供有效的 benchmark ID（1到100之间的数字）或自定义查询。'})
        return

    try:
        # 检查工作目录是否存在,如果不存在则创建
        if not os.path.exists(workspace):
            os.makedirs(workspace)

        # 清空工作目录
        clear_directory(workspace)
        print(f"已清空工作目录: {workspace}")

        # 如果是benchmark，复制相应的数据
        if not custom_query:
            input_path = f"D:\\ComputerScience\\CODES\\MatPlotAgent-main\\benchmark_data\\data\\{benchmark_id}"
            if os.path.exists(input_path):
                for item in os.listdir(input_path):
                    s = os.path.join(input_path, item)
                    d = os.path.join(workspace, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)
                print(f"已将 {input_path} 的内容复制到 {workspace}")

        print(f"执行 mainworkflow，使用模型: {model}")

        def update_callback(expanded_instruction=None, code=None, visual_feedback=None, figure=None,
                            terminal_output=None):
            if expanded_instruction:
                emit('expanded_instruction_update', {'expanded_instruction': expanded_instruction, 'append': True})
            if code:
                emit('code_update', {'code': code, 'append': True})
            if visual_feedback:
                emit('visual_feedback_update', {'visual_feedback': visual_feedback, 'append': True})
            if figure:
                with open(figure, 'rb') as img_file:
                    plot_data = base64.b64encode(img_file.read()).decode()
                plot_type = 'original' if figure.endswith('novice.png') else 'modified'
                socketio.emit('plot_update', {'type': plot_type, 'data': plot_data})
            if terminal_output:
                emit('terminal_output_update', {'terminal_output': terminal_output, 'append': True})

        # 执行workflow
        if custom_query:
            result = mainworkflow(custom_query, custom_query, workspace, update_callback, model=model)
        else:
            result = mainworkflow(instruction['expert_instruction'], instruction['simple_instruction'], workspace,
                                  update_callback, model=model)

        emit('benchmark_complete', {'status': 'success'})

    except Exception as e:
        emit('error', {'error': str(e)})


if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)