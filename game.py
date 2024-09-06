from gptapi import generate_adventure, translate_to_english, t2i
import json
import re


# 이미지 생성 프롬프트 작성 함수
def create_image_prompt(world_eng, char_traits_eng, img_story_eng):
    return f"""
    Based on the following inputs, create a **single, unified image** that depicts only one scene:

    - World setting: {world_eng}
    - Main character's traits: {char_traits_eng}
    - Scenario: {img_story_eng}

    The image must depict only one specific moment in time, with a single setting and character. Avoid creating multiple, disjointed, or collage-like images. The entire composition must focus on one scene, with no other visual distractions or separate events in the image.

    Ensure that the background and environment reflect the world’s setting and the time period accurately, including any natural or architectural elements relevant to the scenario. The main character should be depicted only from the back, facing the scenario as it unfolds.

    All elements in the image, including the character and the world, must fit naturally within the described scene. Do not include elements from other cultures or periods that are not directly relevant to the depicted world. 

    Do not include any text, labels, or unrelated visual elements in the image. The scene should visually convey the story, mood, and tension through the character's posture, the background, and the atmosphere of the moment.
    """

# 프롬프트 생성 함수 (최초 스토리, 선택지 및 이미지)
def get_main_story(world, char_traits, aim, count, playlog, choices, status, life, selectchoice, max_tokens=1000, min_tokens=700):
    # 입력된 내용을 영어로 번역
    world_eng = translate_to_english(world)
    char_traits_eng = translate_to_english(char_traits)
    aim_eng = translate_to_english(aim)

    # 선택한 선택지에 따른 이벤트 설명 (selectchoice가 있을 때만)
    event_description = ""
    if selectchoice:
        event_description = f"당신은 '{selectchoice}'를 선택했습니다. 이 선택에 따라 결과가 도출되었습니다. 그 결과는 다음과 같습니다."

    # 메인 스토리 생성 프롬프트
    story_prompt = f"""
    TRPG 게임을 만듭니다. 게임의 구성 요소는 캐릭터의 스테이터스, 인벤토리, 라이프, 그리고 엔딩입니다.

    {event_description}  # 선택한 행동의 결과에 대한 설명 추가

    이 결과를 바탕으로 상황을 설명하고, 스토리 전개를 도출합니다. 선택에 따른 결과는 상황 설명의 첫 번째 줄에 반영되며, 선택한 행동이 게임의 진행 상황에 어떤 영향을 미치는지 묘사해 주세요. 캐릭터의 행동이 스테이터스에 영향을 미치거나, 인벤토리 아이템을 획득하거나 손실하는 등의 변화를 묘사해 주세요.

    제가 제공하는 정보는 다음과 같습니다:
    1. 세계관: {world}
    2. 캐릭터: {char_traits}
    3. 목표: {aim}

    게임 진행 방식:
    1. 세계의 상황이나 이벤트를 묘사하고, 캐릭터가 선택할 수 있는 선택지를 3개 제시합니다.
    2. 선택한 행동에 따라 1~20 사이의 주사위를 돌려 결과를 결정합니다:
    - 1~3: 매우 나쁜 결과 (예: 체력 감소, 부정적 상태).
    - 4~8: 부정적인 결과 (예: 불리한 아이템 획득).
    - 9~13: 중립적인 결과.
    - 14~20: 긍정적인 결과 (예: 좋은 아이템 획득, 스테이터스 증가).
    3. 체력은 한 번에 최대 1만 감소할 수 있습니다.
    4. 스테이터스는 1 미만으로 떨어질 수 없습니다.

    캐릭터의 초기 스테이터스(스테이터스의 총 합은 15 입니다. {status}가 None 이 아니라면 {status}가 현재 플레이어의 스텟 입니다.):
    - life: 3 (게임 오버와 직결, 0이 되면 게임 오버, 최대 체력 3)
    - strength: 아이템을 들 수 있는 수량 결정
    - perception: 숨겨진 상황 감지
    - endurance: 지속적인 힘 사용 관련
    - charisma: NPC와의 상호작용
    - intelligence: 복잡한 아이템 사용 능력
    - luck: 주사위 판정에 보정
    - 인벤토리: 아이템 보유 및 사용

    엔딩 조건:
    - 10번의 선택지 선택 후 목표 달성 여부에 따라 엔딩을 생성합니다.
    - 목표가 달성되면 성취와 여정을 요약하고 한줄평을 남깁니다.
    - 현재 선택지 횟수는 {count}

    게임 진행 중:
    - '선택지 횟수', '스테이터스', '인벤토리'를 항상 먼저 출력한 후 상황 설명과 선택지를 제공합니다.
    - 선택지마다 상황에 따른 스테이터스 변화나 아이템 변화가 최소 1회 발생해야 합니다.
    - 아이템 사용 시 인벤토리에서 제거합니다.
    - 선택지에 따라 어떤 효과가 나오는지는 보여주지 말아줘

    진행 상황:
    - 현재까지의 대화 기록: {playlog} (None일 경우 첫 대화입니다).
    - 사용자의 선택: {selectchoice} (None일 경우 첫 선택입니다).
    - 첫 대화일 경우 선택횟수는 이야
    - 현재 status는 {status} (None일 경우 첫 선택입니다).
    - 마지막 대화의 선택지 목록은 {choices} (None일 경우 첫 선택입니다).
    - 현재 체력은 {life}

    중요: 다음 사용자 입력이 필요합니다. 추가 입력이 있을 때까지 다음 출력을 생성하지 마세요.
    스텟의 변화나 아이템의 획득을 선택지에 직접적인 수치로 표시하지는 말아줘
    스텟은 스탯이름:1, 스탯이름:2, 스탯이름:3 이런식으로 출력해줘
    위 내용을 바탕으로 상황을 묘사하고, 선택지를 제공해 주세요.
    마지막에 엔딩때는 요약을 [요약] 하고 요약을 출력해줘
    """
    
    # 메인 스토리 생성
    response_text = generate_adventure(story_prompt)
    
    # 이미지 프롬프트 생성 및 이미지 생성 API 호출
    img_story_eng = f"{world_eng}, {char_traits_eng}, {aim_eng}"
    image_prompt = create_image_prompt(world_eng, char_traits_eng, img_story_eng)
    image_url = t2i(image_prompt)

    return response_text, image_url

#json 형식 파싱
def parse_output_to_json(output_text):
    # 스테이터스 추출
    status_match = re.search(r'\[스테이터스\]\n(.+?)\n\n', output_text, re.DOTALL)
    status_text = status_match.group(1) if status_match else ''
    
    # 스테이터스를 콤마로 분리하고 각 항목을 ':'로 나누어 딕셔너리로 변환
    status = {}
    if status_text:
        status_items = status_text.split(',')
        for item in status_items:
            if ':' in item:
                key, value = item.split(':', 1)
                try:
                    # 문자열에서 숫자만 추출
                    number = re.findall(r'\d+', value.strip())
                    status[key.strip()] = int(number[0]) if number else 1
                except ValueError:
                    print(f"Failed to parse status value for {key.strip()}: {value.strip()}")
                    status[key.strip()] = 1  # 기본값 1로 설정

    # 인벤토리 추출
    inventory_match = re.search(r'\[인벤토리\]\n(.+)', output_text)  # [인벤토리] 섹션 아래 텍스트 추출
    inventory_text = inventory_match.group(1).strip() if inventory_match else ''

    # 빈 딕셔너리 초기화
    inventory = {}

    # 인벤토리 내용이 "없음"인 경우 처리
    if "없음" in inventory_text:
        inventory = {}  # 빈 딕셔너리 유지
    else:
        # 아이템들을 쉼표로 분리하여 리스트로 만듦
        inventory_items = inventory_text.split(', ')

        # 각 아이템을 파싱하여 딕셔너리에 추가, 불필요한 항목 필터링
        for item in inventory_items:
            if ':' in item:
                key, value = item.split(':', 1)  # 첫 번째 ':'로만 분리
                key = key.strip()
                value = value.strip()

                # "수량" 또는 "아이템" 키는 제외
                if key not in ["수량", "아이템"]:
                    try:
                        inventory[key] = int(value) if value.isdigit() else 0  # 숫자일 때만 변환, 아니면 0
                    except ValueError:
                        print(f"Failed to parse inventory item for {key.strip()}: {value.strip()}")
                        inventory[key] = 1  # 변환 실패 시 기본값 설정

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

    # 요약 추출
    gptsays_match = re.search(r'\[요약\]\n(.+?)\n\n', output_text, re.DOTALL)
    gptsays = gptsays_match.group(1) if gptsays_match else ''

    # 최종 JSON 형식으로 변환
    parsed_data = {
        "status": status,
        "life": status.get('체력', 3),  # 체력 가져오기, 기본값 3
        "inventory": inventory,  # 필터링된 인벤토리
        "playlog": playlog,
        "choices": choices,
        "gptsays": gptsays
    }

    return parsed_data
