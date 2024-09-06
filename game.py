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
    4. 스테이터스는 1 미만으로 떨어질 수 없습니다.

    캐릭터의 초기 스테이터스(스테이터스의 총 합은 15 입니다.):
    - life: 3 (게임 오버와 직결, 0이 되면 게임 오버, 최대 체력 3)
    - strength: 아이템을 들 수 있는 수량 결정
    - perception: 숨겨진 상황 감지
    - endurance: 지속적인 힘 사용 관련
    - charisma: NPC와의 상호작용
    - intelligence: 복잡한 아이템 사용 능력
    - luck: 주사위 판정에 보정
    - 인벤토리: 아이템 보유 및 사용

    엔딩 조건:
    - 15번 이상 30번 이하의 선택지 후 목표 달성 여부에 따라 엔딩을 생성합니다.
    - 목표가 달성되면 성취와 여정을 요약하고 한줄평을 남깁니다.

    게임 진행 중:
    - '선택지 횟수', '스테이터스', '인벤토리'를 항상 먼저 출력한 후 상황 설명과 선택지를 제공합니다.
    - 선택지마다 상황에 따른 스테이터스 변화나 아이템 변화가 최소 1회 발생해야 합니다.
    - 아이템 사용 시 인벤토리에서 제거합니다.
    - 선택지에 따라 어떤 효과가 나오는지는 보여주지 말아줘

    진행 상황:
    - 현재까지의 대화 기록: {playlog} (None일 경우 첫 대화입니다).
    - 사용자의 선택: {selectchoice} (None일 경우 첫 선택입니다).

    중요: 다음 사용자 입력이 필요합니다. 추가 입력이 있을 때까지 다음 출력을 생성하지 마세요.
    스텟의 변화나 아이템의 획득을 선택지에 직접적인 수치로 표시하지는 말아줘
    스텟은 스탯이름:1, 스탯이름:2, 스탯이름:3 이런식으로 출력해줘
    위 내용을 바탕으로 상황을 묘사하고, 선택지를 제공해 주세요.

    마지막에 엔딩때는 요약을 [요약] 하고 요약을 출력해줘
    """
    
    # 메인 스토리 생성
    response_text = generate_adventure(story_prompt)
    
    return response_text

def parse_output_to_json(output_text):
    # 스테이터스 추출
    status_match = re.search(r'\[스테이터스\]\n(.+?)\n\n', output_text, re.DOTALL)
    status_text = status_match.group(1) if status_match else ''
    
    # 스테이터스를 콤마로 분리하고 각 항목을 ':'로 나누어 딕셔너리로 변환
    status = {}
    if status_text:
        # 콤마를 기준으로 나눈 후 공백을 처리하지 않고 ':'로 나눈다.
        status_items = status_text.split(',')
        for item in status_items:
            if ':' in item:
                key, value = item.split(':', 1)
                try:
                    # 문자열에서 정확하게 숫자만 추출
                    number = re.findall(r'\d+', value.strip())
                    status[key.strip()] = int(number[0]) if number else 1
                except ValueError:
                    # 디버그 출력 추가
                    print(f"Failed to parse status value for {key.strip()}: {value.strip()}")
                    status[key.strip()] = 1  # 변환 실패 시 기본값 설정

    # 인벤토리 추출
    inventory_match = re.search(r'\[인벤토리\]\n아이템 : (.+)', output_text)
    inventory_items = inventory_match.group(1).split(', ') if inventory_match else ['']
    inventory = {inventory_items}

    # 스토리 추출
    playlog_match = re.search(r'\[스토리\]\n(.+?)\n\n', output_text, re.DOTALL)
    playlog = playlog_match.group(1) if playlog_match else ''

    # 선택지 추출
    choices_match = re.search(r'\[선택지\]\n(.+?)\n\n', output_text, re.DOTALL)
    choices_text = choices_match.group(1) if choices_match else ''
    choices_lines = choices_text.split('\n')
    choice_keys = ['first', 'second', 'third', 'fourth']
    # 선택지를 키 이름에 맞게 할당
    choices = {choice_keys[i]: line.strip() for i, line in enumerate(choices_lines) if line.strip() and i < len(choice_keys)}

    # 선택 횟수 추출
    count_match = re.search(r'\[선택횟수\]\n(\d+)', output_text)
    count = int(count_match.group(1)) if count_match else 0

    gptsays_match = re.search(r'\[요약\]\n(.+?)\n\n', output_text, re.DOTALL)
    gptsays = gptsays_match.group(1) if gptsays_match else ''

    # 새로운 JSON 형식으로 변환
    parsed_data = {
        "status": status,
        "life": status.get('체력', 3),  # 체력 가져오기, 기본값 3
        "inventory": inventory,
        "playlog": playlog,
        "choices": choices,
        "count": count,
        "gptsays": gptsays
    }

    return parsed_data

