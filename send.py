from flask import Flask, request, jsonify
import json
import requests
from status import set_character_stats  # status.py의 함수 임포트
from game import get_main_story, generate_next_story   # game.py의 함수 임포트

app = Flask(__name__)

@app.route('/ai/process', methods=['POST'])
def process_request():
    """백엔드로부터 JSON 파일을 받아 처리하고 게임 진행에 따라 적절한 함수를 호출하는 엔드포인트"""

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
    backend_callback_url = "http://43.200.1.120/api/callback" # 결과를 전송할 백엔드 서버의 URL

    # 주요 게임 데이터 확인
    username = data.get('username')
    worldview = data.get('worldview')
    charsetting = data.get('charsetting')
    aim = data.get('aim')
    playlog = data.get('playlog')
    dice = data.get('dice')
    selectedchoice = data.get('selectedchoice')

    # 데이터 검증: 필수 데이터 확인
    required_fields = [username, worldview, charsetting, aim]
    if any(field is None for field in required_fields):
        return jsonify({'status': 'failure', 'message': 'Missing required fields'}), 400

    # 처음 입력: 캐릭터 설정이 있고 나머지가 None인 경우
    if all(value is None for value in [playlog, dice, selectedchoice]):
        # 캐릭터 스탯 설정
        status = set_character_stats(charsetting)  # status.py의 함수 호출
        data['status'] = status

        # main_story 호출
        story, choices_list= get_main_story(worldview, charsetting, aim)
        data['nextstory'] = story
        data['choices'] = choices_list
        data['life'] = 3
        image_url = None
        data['imageurl'] = image_url

    else:
        # 이후 입력: 다음 스토리 진행
        next_story, choices_list, status_change, inventory_change, life_change, endding = generate_next_story(selectedchoice)
        data['choices'] = choices_list
        data['status'] = status_change
        data['inventory'] = inventory_change
        data['life'] = life_change
        data['gptsays'] = endding
        data['nextstory'] = next_story
        data['playlog'] = None
        data['dice'] = None
        data['selectedchoice'] = None
        data['worldview'] = None
        data['charsetting'] = None
        data['aim'] = None

    # 백엔드로 결과 전송
    if not backend_callback_url:
        return jsonify({'status': 'failure', 'message': 'Backend callback URL is missing'}), 400

    try:
        backend_response = requests.post(backend_callback_url, json=data)
        backend_response.raise_for_status()
        print("데이터를 백엔드 서버로 전송했습니다.")

        # 백엔드로 전송한 데이터를 응답에 포함시킴
        return jsonify({
            'status': 'success',
            'message': 'Data sent to backend server',
            'sent_data': data  # 보낸 데이터를 응답에 포함
        }), 200

    except requests.exceptions.RequestException as e:
        print(f"데이터 전송 중 오류 발생: {e}")
        return jsonify({'status': 'failure', 'message': 'Failed to send data to backend server'}), 500

@app.route('/ai/callback', methods=['POST'])
def callback():
    """콜백 요청을 처리하는 엔드포인트"""
    data = request.get_json()
    print("콜백 데이터 수신:", data)
    return jsonify({'status': 'success', 'message': 'Callback received successfully'}), 200

def run_ai_server():
    """AI 서버 실행"""
    app.run(host='43.200.1.120', port=5000)  # AI 서버는 5000 포트에서 실행

if __name__ == '__main__':
    # AI 서버 실행
    run_ai_server()
