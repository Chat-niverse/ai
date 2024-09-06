from flask import Flask, request, jsonify
import json
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
        processed_data = json.loads(parse_gpt_response(story_response))  # 여기서 JSON 파싱

    else:
        # 이후 입력: 다음 스토리 진행
        story_response = get_main_story(worldview, charsetting, aim, playlog, selectedchoice)
        processed_data = json.loads(parse_gpt_response(story_response))  # 여기서도 JSON 파싱

    # 적절한 JSON 형식으로 데이터 가공
    final_data = {
        "username": username,
        "worldview": worldview,
        "charsetting": charsetting,
        "aim": aim,
        "status": processed_data.get("status", {}),
        "life": processed_data.get("life", 3),
        "inventory": processed_data.get("inventory", {}),
        "playlog": processed_data.get("playlog", ""),
        "selectedchoice": selectedchoice,
        "gptsays": processed_data.get("gptsays", ""),
        "choices": processed_data.get("choices", {}),
        "imageurl": processed_data.get("imageurl", "")
    }

    # 처리된 데이터를 클라이언트에 직접 응답으로 전송
    return jsonify({
        'status': 'success',
        'message': 'Game data processed successfully',
        'processed_data': final_data  # 처리된 데이터를 응답에 포함
    }), 200

def run_ai_server():
    """AI 서버 실행"""
    app.run(host='0.0.0.0', port=5000)  # AI 서버는 5000 포트에서 실행

if __name__ == '__main__':
    # AI 서버 실행
    run_ai_server()
