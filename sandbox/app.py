from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import subprocess
import psutil
from werkzeug.utils import secure_filename
import shutil
import threading

app = Flask(__name__)
CORS(app)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['CACHE_TYPE'] = "null"

ENGINE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'engine')
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_flows_filename(address):
    domain = re.sub(r'^(http|https)://', '', address)
    domain = re.sub(r'[:/]', '_', domain)
    domain = re.sub(r'[<>:"/\\|?*]', '', domain)
    return os.path.join(ENGINE_DIR, f'flows({domain[:50]})')

is_service_running = False
service_process = None

@app.route('/execute_combined', methods=['POST'])
def execute_combined_command():
    data = request.json
    address = data.get('address')
    if not address or not validate_address(address):
        return jsonify({'error': '请输入正确的IP地址或域名格式（包含http/https）'}), 400

    flows_file = get_flows_filename(address)
    commands = [
        f"mitmweb --ssl-insecure",
        f"rad_windows_amd64.exe -t {address} --http-proxy 127.0.0.1:8080"
    ]
    
    responses = []

    def run_command(command):
        try:
            print(f"Executing command: {command}")
            process = subprocess.Popen(command, shell=True, cwd=ENGINE_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
            stdout, stderr = process.communicate()
            responses.append({
                'command': command,
                'stdout': stdout,
                'stderr': stderr,
                'returncode': process.returncode
            })
        except Exception as e:
            responses.append({
                'command': command,
                'error': str(e)
            })
    
    threads = []
    for command in commands:
        thread = threading.Thread(target=run_command, args=(command,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    return jsonify(responses)

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '未选择文件'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file.save(file_path)
    return jsonify({'success': True, 'filename': filename})

@app.route('/start_service', methods=['POST'])
def start_service():
    global is_service_running, service_process
    data = request.json
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': '请先上传文件'}), 400
    
    if is_service_running:
        return jsonify({'error': '服务已经在运行，请先停止当前服务'}), 400
    
    try:
        cache_dir = os.path.join(ENGINE_DIR, 'cache')
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
        os.makedirs(cache_dir)

        target_port = 12355
        processes_to_terminate = []
        for proc in psutil.process_iter(['pid', 'name']):
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == target_port and proc.info['name'] not in ('System Idle Process', 'System'):
                    processes_to_terminate.append(proc)
        
        for proc in processes_to_terminate:
            try:
                print(f"Terminating process {proc.info['pid']} on port {target_port}")
                proc.terminate()
                proc.wait()
            except psutil.NoSuchProcess:
                print(f"Process {proc.info['pid']} no longer exists")

        if service_process:
            service_process.terminate()
            service_process.wait()

        command = f"mitm.exe -f {os.path.join(UPLOAD_FOLDER, filename)}"
        print(f"Executing command: {command}")
        service_process = subprocess.Popen(command, shell=True, cwd=ENGINE_DIR)
        is_service_running = True
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stop_service', methods=['POST'])
def stop_service():
    global is_service_running, service_process
    if not is_service_running:
        return jsonify({'error': '当前未运行服务，无需停止'}), 400
    
    try:
        target_port = 12355
        processes_to_terminate = []
        for proc in psutil.process_iter(['pid', 'name']):
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == target_port and proc.info['name'] not in ('System Idle Process', 'System'):
                    processes_to_terminate.append(proc)
        
        for proc in processes_to_terminate:
            try:
                print(f"Terminating process {proc.info['pid']} on port {target_port}")
                proc.terminate()
                proc.wait()
            except psutil.NoSuchProcess:
                print(f"Process {proc.info['pid']} no longer exists")

        if service_process:
            service_process.terminate()
            service_process.wait()

        is_service_running = False
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stop_scan', methods=['POST'])
def stop_scan():
    try:
        target_port = 8081
        processes_to_terminate = []
        for proc in psutil.process_iter(['pid', 'name']):
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == target_port and proc.info['name'] not in ('System Idle Process', 'System'):
                    processes_to_terminate.append(proc)
        
        for proc in processes_to_terminate:
            try:
                print(f"Terminating process {proc.info['pid']} on port {target_port}")
                proc.terminate()
                proc.wait()
            except psutil.NoSuchProcess:
                print(f"Process {proc.info['pid']} no longer exists")

        return jsonify({'success': True, 'message': '爬取已停止'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.cache_control.no_cache = True
    response.cache_control.must_revalidate = True
    response.cache_control.max_age = 0
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

def validate_address(addr):
    url_regex = re.compile(r'^(http|https)://[a-zA-Z0-9.-]+(:\d+)?(\/.*)?$')
    return bool(url_regex.match(addr))

if __name__ == '__main__':
    app.run(port=5050)
