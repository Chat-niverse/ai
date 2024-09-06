from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_request():
    """백엔드로부터 JSON 파일을 받아 처리하고 결과를 다시 백엔드로 전송하는 엔드포인트"""

    # JSON 파일 받기
    if 'file' not in request.files:
        return jsonify({'status': 'failure', 'message': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'status': 'failure', 'message': 'No file selected for uploading'}), 400

    try:
        data = json.load(file)  # JSON 파일을 파싱합니다.
    except json.JSONDecodeError:
        print("JSON 디코딩 오류: 파일이 유효한 JSON 형식이 아닙니다.")
        return jsonify({'status': 'failure', 'message': 'Invalid JSON format in file'}), 400

    # 백엔드 서버로 결과를 전송할 URL 추출
    backend_callback_url = data.get('callback_url')  # 결과를 전송할 백엔드 서버의 URL

    # 주요 게임 데이터 확인
    username = data.get('username')
    worldview = data.get('worldview')
    charsetting = data.get('charsetting')
    aim = data.get('aim')
    status = data.get('status')
    life = data.get('life')
    inventory = data.get('inventory')
    playlog = data.get('playlog')
    gameending = data.get('gameending')
    gptsays = data.get('gptsays')

    # 데이터 검증: 필수 데이터 확인
    required_fields = [username, worldview, charsetting, aim]
    if any(field is None for field in required_fields):
        return jsonify({'status': 'failure', 'message': 'Missing required fields'}), 400

    # 후속 요청인 경우, 백엔드로 데이터 전송
    if not backend_callback_url:
        return jsonify({'status': 'failure', 'message': 'Backend callback URL is missing'}), 400

    # 동일한 JSON 파일 형식으로 백엔드로 전송
    try:
        backend_response = requests.post(backend_callback_url, json=data)
        backend_response.raise_for_status()
        print("데이터를 백엔드 서버로 전송했습니다.")
        return jsonify({'status': 'success', 'message': 'Data sent to backend server'}), 200

    except requests.exceptions.RequestException as e:
        print(f"데이터 전송 중 오류 발생: {e}")
        return jsonify({'status': 'failure', 'message': 'Failed to send data to backend server'}), 500

def run_ai_server():
    """AI 서버 실행"""
    app.run(host='0.0.0.0', port=5000)  # AI 서버는 5000 포트에서 실행

if __name__ == '__main__':
    # AI 서버 실행
    run_ai_server()
