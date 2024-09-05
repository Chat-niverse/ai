from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_request():
    """백엔드 서버로부터 데이터를 받아 처리하고 결과를 다시 전송하는 엔드포인트"""
    data = request.json
    user_input = data.get('input')
    callback_url = data.get('callback_url')  # 결과를 전송할 백엔드 서버의 URL

    # 1. 입력을 받았다는 상태를 먼저 백엔드 서버로 전송
    status_update = {'status': 'received', 'message': 'Input received by AI server'}
    try:
        status_response = requests.post(callback_url, json=status_update)
        status_response.raise_for_status()
        print("입력 상태 업데이트를 백엔드 서버로 전송했습니다.")
    except requests.exceptions.RequestException as e:
        print(f"입력 상태 업데이트 전송 중 오류 발생: {e}")
        return jsonify({'status': 'failure', 'message': 'Failed to update status'}), 500

    story = '테스트 스토리'
    label = '테스트 라벨'

    # 결과를 JSON 파일로 저장
    result_data = {
        'intent': story,
        'message': label,
    }
    with open('result.json', 'w') as json_file:
        json.dump(result_data, json_file)

    # 3. 처리된 결과를 백엔드 서버로 전송
    try:
        response = requests.post(callback_url, json=result_data)
        response.raise_for_status()
        return jsonify({'status': 'success', 'message': 'Result sent to backend server'}), 200
    except requests.exceptions.RequestException as e:
        print(f"결과 전송 중 오류 발생: {e}")
        return jsonify({'status': 'failure', 'message': 'Failed to send result'}), 500

def run_ai_server():
    """AI 서버 실행"""
    app.run(host='0.0.0.0', port=5000)  # AI 서버는 5000 포트에서 실행

if __name__ == '__main__':
    # AI 서버 실행
    run_ai_server()