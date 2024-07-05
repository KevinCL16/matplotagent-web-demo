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

# Load benchmark instructions
with open('benchmark_data/benchmark_instructions.json', 'r') as f:
    benchmark_instructions = json.load(f)


@app.route('/')
def index():
    return render_template('index_dynamic.html')


@socketio.on('run_benchmark')
def handle_benchmark(data):
    benchmark_id = data.get('id')

    if not benchmark_id or not 1 <= int(benchmark_id) <= 100:
        emit('error', {'error': '无效的 benchmark ID。请提供 1 到 100 之间的数字。'})
        return

    try:
        # Get the instruction for the given benchmark ID
        instruction = benchmark_instructions[int(benchmark_id) - 1]

        # 发送指令更新
        emit('instruction_update', {'instruction': instruction['simple_instruction']})

        workspace = f"D:\ComputerScience\CODES\MatPlotAgent-main\workspace\example_{benchmark_id}"

        # 检查工作目录是否存在,如果不存在则创建
        if not os.path.exists(workspace):
            os.makedirs(workspace)
            print(f"已创建工作目录: {workspace}")
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

        print("执行 mainworkflow")

        def update_callback(expanded_instruction=None, code=None, visual_feedback=None, figure=None, terminal_output=None):
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

        result = mainworkflow(instruction['expert_instruction'], instruction['simple_instruction'], workspace, update_callback)
        emit('benchmark_complete', {'status': 'success'})

    except Exception as e:
        emit('error', {'error': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)