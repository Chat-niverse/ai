from flask import Flask, request, jsonify
import json
import requests
from game import get_main_story, parse_gpt_response  # 필요한 함수 임포트

app = Flask(__name__)

@app.route('/ai/process', methods=['POST'])
def process_request():
    """백엔드로부터 JSON 데이터를 받아 처리하고 게임 진행에 따라 적절한 함수를 호출하는 엔드포인트"""

    try:
        # JSON 데이터를 요청의 body에서 가져옴
        data = request.get_json()
        if data is None:
            return jsonify({'status': 'failure', 'message': 'Invalid or missing JSON data in the request'}), 400
    except json.JSONDecodeError:
        return jsonify({'status': 'failure', 'message': 'Invalid JSON format in body'}), 400

    # 주요 게임 데이터 확인
    username = data.get('username')
    worldview = data.get('worldview')
    charsetting = data.get('charsetting')
    aim = data.get('aim')
    playlog = data.get('playlog')
    selectedchoice = data.get('selectedchoice')

    # 데이터 검증: 필수 데이터 확인
    required_fields = [username, worldview, charsetting, aim]
    if any(field is None for field in required_fields):
        return jsonify({'status': 'failure', 'message': 'Missing required fields'}), 400

    # 처음 입력: 캐릭터 설정이 있고 나머지가 None인 경우
    if all(value is None for value in [playlog, selectedchoice]):
        # main_story 호출
        story_response = get_main_story(worldview, charsetting, aim, playlog, selectedchoice)
        # GPT 응답을 JSON 형식으로 변환
        processed_data = parse_gpt_response(story_response)

    else:
        # 이후 입력: 다음 스토리 진행
        next_story, choices_list, status_change, inventory_change, life_change, ending = get_main_story(worldview, charsetting, aim, playlog, selectedchoice)
        # 적절한 JSON 형식으로 데이터 가공
        processed_data = {
            'nextstory': next_story,
            'choices': choices_list,
            'status': status_change,
            'inventory': inventory_change,
            'life': life_change,
            'gptsays': ending,
            'playlog': playlog,
            'selectedchoice': selectedchoice,
            'worldview': worldview,
            'charsetting': charsetting,
            'aim': aim
        }

    # 백엔드로 결과 전송할 URL
    backend_url = "http://your-backend-server-url/endpoint"  # 실제 백엔드 서버 URL로 교체

    try:
        # 백엔드 서버로 결과 전송
        response = requests.post(backend_url, json=processed_data)
        response.raise_for_status()  # 요청이 성공하지 않으면 예외 발생
        return jsonify({
            'status': 'success',
            'message': 'Game data processed and sent to backend successfully',
            'backend_response': response.json()  # 백엔드에서 온 응답을 포함
        }), 200

    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'failure', 'message': f'Failed to send data to backend server: {e}'}), 500

def run_ai_server():
    """AI 서버 실행"""
    app.run(host='0.0.0.0', port=5000)  # AI 서버는 5000 포트에서 실행

if __name__ == '__main__':
    # AI 서버 실행
    run_ai_server()
