from flask import Flask, request, jsonify
from game import get_main_story, parse_output_to_json  # 필요한 함수 임포트

app = Flask(__name__)

count = -1

@app.route('/ai/process', methods=['POST'])
def process_request():
    global count
    """백엔드로부터 JSON 데이터를 받아 처리하고 게임 진행에 따라 적절한 함수를 호출하는 엔드포인트"""

    try:
        # JSON 데이터를 요청의 body에서 가져옴
        data = request.get_json()
        if data is None:
            return jsonify({'status': 'failure', 'message': 'Invalid or missing JSON data in the request'}), 400
    except Exception as e:
        return jsonify({'status': 'failure', 'message': 'Invalid JSON format in body', 'error': str(e)}), 400

    # 주요 게임 데이터 확인
    username = data.get('username')  # 기본 값 추가
    worldview = data.get('worldview')  # 기본 값 추가
    charsetting = data.get('charsetting')  # 기본 값 추가
    aim = data.get('aim')  # 기본 값 추가
    playlog = data.get('playlog', '')
    selectedchoice = data.get('selectedchoice', None)  # 기본 선택 값 추가
    choices = data.get('choices', None)
    status = data.get('status', None)
    life = data.get('life')

    # 데이터 검증: 필수 데이터 확인
    required_fields = [username, worldview, charsetting, aim]
    if any(field is None for field in required_fields):
        return jsonify({'status': 'failure', 'message': 'Missing required fields'}), 400
    
    count += 1

    # 게임 스토리 진행: 처음 입력이거나 이후 입력에 따라 다르게 처리
    story_response, image_url = get_main_story(worldview, charsetting, aim, count, playlog, choices, status, life, selectedchoice)

    # GPT 응답을 JSON 형식으로 변환
    processed_data = parse_output_to_json(story_response)

    # 적절한 JSON 형식으로 데이터 가공
    final_data = {
        "username": username,
        "worldview": worldview,
        "charsetting": charsetting,
        "aim": aim,
        "life": processed_data.get("life", {}),
        "status": {
            "strength": processed_data.get("status", {}).get("strength", 1),
            "perception": processed_data.get("status", {}).get("perception", 1),
            "endurance": processed_data.get("status", {}).get("endurance", 1),
            "charisma": processed_data.get("status", {}).get("charisma", 1),
            "intelligence": processed_data.get("status", {}).get("intelligence", 1),
            "luck": processed_data.get("status", {}).get("luck", 1),
        },
        "inventory": processed_data.get("inventory", {}),
        "playlog": processed_data.get("playlog", ""),
        "selectedchoice": selectedchoice,
        "gptsays": processed_data.get("gptsays", ""),
        "choices": processed_data.get("choices", {}),
        "imageurl": image_url if image_url else 'No image available',  # 이미지 URL 추가
    }

    # 처리된 데이터만 응답으로 전송
    return jsonify(final_data), 200

def run_ai_server():
    """AI 서버 실행"""
    app.run(host='0.0.0.0', port=5001, debug=True)  # AI 서버는 5000 포트에서 실행

if __name__ == '__main__':
    # AI 서버 실행
    run_ai_server()
