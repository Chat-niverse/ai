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
    username = data.get('username', 'PlayerOne')  # 기본 값 추가
    worldview = data.get('worldview', 'Fantasy')  # 기본 값 추가
    charsetting = data.get('charsetting', 'Warrior')  # 기본 값 추가
    aim = data.get('aim', 'Defeat the Dragon')  # 기본 값 추가
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
        "status": {
            "strength": processed_data.get("status", {}).get("힘", 1),
            "perception": processed_data.get("status", {}).get("인지력", 1),
            "endurance": processed_data.get("status", {}).get("지구력", 1),
            "charisma": processed_data.get("status", {}).get("카리스마", 1),
            "intelligence": processed_data.get("status", {}).get("지능", 1),
            "luck": processed_data.get("status", {}).get("운", 1),
            "life": processed_data.get("status", {}).get("체력", 3)
        },
        "life": processed_data.get("life", 3),
        "inventory": processed_data.get("inventory", {}),
        "playlog": processed_data.get("playlog", ""),
        "selectedchoice": selectedchoice or "first",  # 기본 선택 값
        "gptsays": processed_data.get("gptsays", ""),
        "choices": {
            "first": processed_data.get("choices", {}).get("choice_1", ""),
            "second": processed_data.get("choices", {}).get("choice_2", ""),
            "third": processed_data.get("choices", {}).get("choice_3", ""),
            "fourth": processed_data.get("choices", {}).get("choice_4", "")
        },
        "imageurl": processed_data.get("imageurl", "http://example.com/images/dragon.jpg")
    }

    # 처리된 데이터만 응답으로 전송
    return jsonify(final_data), 200  # final_data만 전송

def run_ai_server():
    """AI 서버 실행"""
    app.run(host='0.0.0.0', port=5000)  # AI 서버는 5000 포트에서 실행

if __name__ == '__main__':
    # AI 서버 실행
    run_ai_server()
