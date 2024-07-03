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
    return render_template('index_dynamic.html')  # 确保使用支持实时更新的新HTML文件


@socketio.on('run_benchmark')
def handle_benchmark(data):
    benchmark_id = data.get('id')

    if not benchmark_id or not 1 <= int(benchmark_id) <= 100:
        emit('error', {'error': 'Invalid benchmark ID. Please provide a number between 1 and 100.'})
        return

    try:
        # Get the instruction for the given benchmark ID
        instruction = benchmark_instructions[int(benchmark_id) - 1]

        # 发送指令更新
        emit('instruction_update', {'instruction': instruction['simple_instruction']})

        # Process the instruction using mainworkflow
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

        print("执行mainworkflow")

        def update_callback(expanded_instruction=None, code=None, visual_feedback=None, figure=None):
            emit('expanded_instruction_update', {'expanded_instruction': expanded_instruction})
            emit('code_update', {'code': code})
            emit('visual_feedback_update', {'visual_feedback': visual_feedback})

            if figure is not None:
                with open(figure, 'rb') as img_file:
                    plot_data = base64.b64encode(img_file.read()).decode()
                if figure.endswith('novice.png'):
                    emit('original_plot_update', {'plot': plot_data})

                elif figure.endswith('novice_final.png'):
                    emit('modified_plot_update', {'plot': plot_data})

                else:
                    pass

        result = mainworkflow(instruction['expert_instruction'], instruction['simple_instruction'], workspace, update_callback)

        emit('benchmark_complete', {'status': 'success'})

    except Exception as e:
        emit('error', {'error': str(e)})


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)