import shutil

from flask import Flask, request, jsonify, render_template
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

# Load benchmark instructions
with open('benchmark_data/benchmark_instructions.json', 'r') as f:
    benchmark_instructions = json.load(f)


@app.route('/')
def index():
    return render_template('index_static.html')


@app.route('/api/process_benchmark', methods=['POST'])
def process_benchmark():
    data = request.json
    benchmark_id = data.get('id')

    if not benchmark_id or not 1 <= int(benchmark_id) <= 100:
        return jsonify({'error': 'Invalid benchmark ID. Please provide a number between 1 and 100.'}), 400

    try:
        # Get the instruction for the given benchmark ID
        instruction = benchmark_instructions[int(benchmark_id) - 1]

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
        result = mainworkflow(instruction['expert_instruction'], instruction['simple_instruction'], workspace)

        # Read the generated figure
        with open(result['figure_path'], 'rb') as img_file:
            plot_data = base64.b64encode(img_file.read()).decode()

        return jsonify({
            'status': 'success',
            'instruction': instruction['simple_instruction'],
            'code': result['code'],
            'visual_feedback': result['visual_feedback'],
            'plot': plot_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
