from gptapi import generate_adventure
import json
import re
# 프롬프트 생성 함수 (최초 스토리, 선택지 및 이미지)
def get_main_story(world, char_traits, aim, playlog, selectchoice, max_tokens=1000, min_tokens=700):
    # 메인 스토리 생성 프롬프트
    story_prompt = f"""
    TRPG 게임을 만듭니다. 게임의 구성 요소는 캐릭터의 스테이터스, 인벤토리, 라이프, 그리고 엔딩입니다.

    제가 제공하는 정보는 다음과 같습니다:
    1. 세계관: {world}
    2. 캐릭터: {char_traits}
    3. 목표: {aim}

    게임 진행 방식:
    1. 세계의 상황이나 이벤트를 묘사하고, 캐릭터가 선택할 수 있는 선택지를 2~4개 제시합니다.
    2. 선택한 행동에 따라 1~20 사이의 주사위를 돌려 결과를 결정합니다:
    - 1~3: 매우 나쁜 결과 (예: 체력 감소, 부정적 상태).
    - 4~8: 부정적인 결과 (예: 불리한 아이템 획득).
    - 9~13: 중립적인 결과.
    - 14~20: 긍정적인 결과 (예: 좋은 아이템 획득, 스테이터스 증가).
    3. 체력은 한 번에 최대 1만 감소할 수 있습니다.

    캐릭터의 초기 스테이터스:
    - 체력: 3 (게임 오버와 직결, 0이 되면 게임 오버, 최대 체력 3)
    - 힘: 아이템을 들 수 있는 수량 결정
    - 인지력: 숨겨진 상황 감지
    - 지구력: 지속적인 힘 사용 관련
    - 카리스마: NPC와의 상호작용
    - 지능: 복잡한 아이템 사용 능력
    - 운: 주사위 판정에 보정
    - 인벤토리: 아이템 보유 및 사용

    엔딩 조건:
    - 10번의 선택지 후 목표 달성 여부에 따라 엔딩을 생성합니다.
    - 목표가 달성되면 성취와 여정을 요약하고 한줄평을 남깁니다.

    게임 진행 중:
    - '선택지 횟수', '스테이터스', '인벤토리'를 항상 먼저 출력한 후 상황 설명과 선택지를 제공합니다.
    - 선택지마다 상황에 따른 스테이터스 변화나 아이템 변화가 최소 1회 발생해야 합니다.
    - 아이템 사용 시 인벤토리에서 제거합니다.

    진행 상황:
    - 현재까지의 대화 기록: {playlog} (None일 경우 첫 대화입니다).
    - 사용자의 선택: {selectchoice} (None일 경우 첫 선택입니다).

    중요: 다음 사용자 입력이 필요합니다. 추가 입력이 있을 때까지 다음 출력을 생성하지 마세요.

    위 내용을 바탕으로 상황을 묘사하고, 선택지를 제공해 주세요.
    """
    
    # 메인 스토리 생성
    response_text = generate_adventure(story_prompt)
    
    return response_text

def parse_gpt_response(response_text):
    # 정규 표현식을 사용하여 섹션별로 데이터를 추출
    status_match = re.search(r'\[스테이터스\](.*?)\[인벤토리\]', response_text, re.DOTALL)
    inventory_match = re.search(r'\[인벤토리\](.*?)\[스토리\]', response_text, re.DOTALL)
    story_match = re.search(r'\[스토리\](.*?)\[선택지\]', response_text, re.DOTALL)
    choices_match = re.search(r'\[선택지\](.*?)\[선택횟수\]', response_text, re.DOTALL)
    count_match = re.search(r'\[선택횟수\](.*)', response_text, re.DOTALL)

    # 각 섹션을 텍스트에서 추출하고, 필요 시 변환
    status = parse_status(status_match.group(1).strip()) if status_match else {}
    inventory = parse_inventory(inventory_match.group(1).strip()) if inventory_match else {}
    story = story_match.group(1).strip() if story_match else ""
    choices = parse_choices(choices_match.group(1).strip()) if choices_match else {}
    count = int(count_match.group(1).strip()) if count_match else 0

    # 예시 JSON 데이터 생성
    json_data = {
        "username": "PlayerOne",
        "worldview": "Fantasy",
        "charsetting": "Warrior",
        "aim": "Defeat the Dragon",
        "status": status,
        "life": 3,  # 기본 설정
        "inventory": inventory,
        "playlog": "Entered the dragon's lair.",
        "selectedchoice": "first",
        "gptsays": "You are on the right path to defeat the dragon!",
        "choices": choices,
        "count": 0,
        "imageurl": "http://example.com/images/dragon.jpg"  # 예시 값
    }

    return json.dumps(json_data, indent=4, ensure_ascii=False)

def parse_gpt_response(response_text):
    # 정규 표현식을 사용하여 섹션별로 데이터를 추출
    status_match = re.search(r'\[스테이터스\](.*?)\[인벤토리\]', response_text, re.DOTALL)
    inventory_match = re.search(r'\[인벤토리\](.*?)\[스토리\]', response_text, re.DOTALL)
    story_match = re.search(r'\[스토리\](.*?)\[선택지\]', response_text, re.DOTALL)
    choices_match = re.search(r'\[선택지\](.*?)\[선택횟수\]', response_text, re.DOTALL)
    count_match = re.search(r'\[선택횟수\](.*)', response_text, re.DOTALL)

    # 각 섹션을 텍스트에서 추출하고, 필요 시 변환
    status = parse_status(status_match.group(1).strip()) if status_match else {}
    inventory = parse_inventory(inventory_match.group(1).strip()) if inventory_match else {}
    story = parse_story(story_match.group(1).strip()) if story_match else ""
    choices = parse_choices(choices_match.group(1).strip()) if choices_match else {}
    count = parse_count(count_match.group(1).strip()) if count_match else 0

    # 예시 JSON 데이터 생성
    json_data = {
        "username": "PlayerOne",
        "worldview": "Fantasy",
        "charsetting": "Warrior",
        "aim": "Defeat the Dragon",
        "status": status,
        "life": 3,  # 기본 설정
        "inventory": inventory,
        "playlog": story,  # 스토리를 playlog에 저장
        "selectedchoice": "first",
        "gptsays": "You are on the right path to defeat the dragon!",
        "choices": choices,
        "count": count,  # 선택 횟수 추가
        "imageurl": "http://example.com/images/dragon.jpg"  # 예시 값
    }

    return json.dumps(json_data, indent=4, ensure_ascii=False)

# 스테이터스 파싱
def parse_status(status_text):
    status_lines = status_text.split('\n')
    status = {}
    for line in status_lines:
        key, value = line.split(':')
        status[key.strip()] = int(value.strip())
    return status

# 인벤토리 파싱
def parse_inventory(inventory_text):
    inventory_lines = inventory_text.split('\n')
    inventory = {}
    for line in inventory_lines:
        key, value = line.split(':')
        inventory[key.strip()] = int(value.strip())
    return inventory

# 선택지 파싱
def parse_choices(choices_text):
    choices_lines = choices_text.split('\n')
    choices = {}
    for i, line in enumerate(choices_lines, 1):
        choices[f"choice_{i}"] = line.strip()
    return choices

# 스토리 파싱
def parse_story(story_text):
    # 스토리 텍스트를 필요한 형식으로 가공
    return story_text.strip()

# 선택 횟수 파싱
def parse_count(count_text):
    # 선택 횟수를 정수로 변환하여 반환
    return int(count_text.strip())

# 예시 사용
response_text = get_main_story('중세시대 유럽', '가정적인 농부', '마왕 처치', None, None)
json_output = parse_gpt_response(response_text)
print(json_output)