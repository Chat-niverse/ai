import openai
from dotenv import load_dotenv
import os

# OpenAI API 키 설정
load_dotenv(dotenv_path='GitH/env')  # .env 파일을 로드하여 환경 변수를 설정
openai.api_key = os.getenv('OPENAI_API_KEY')  # 환경 변수에서 OpenAI API 키 가져오기

def set_character_stats(charsetting):
    """
    GPT API를 사용하여 캐릭터 설정을 기반으로 스탯을 설정하는 함수.
    각 스탯의 총합이 15가 되도록 요청하며, 각 스탯의 최소값은 1입니다.
    """
    prompt = f"""
    Create character stats for a {charsetting} in a fantasy setting.
    The stats should include the following categories:
    - Strength
    - Perception
    - Endurance
    - Charisma
    - Intelligence
    - Luck

    The sum of all stat values should be exactly 15.
    Each stat value should be between 1 and 10.
    Please provide the stats in the format:
    Strength: <value>
    Perception: <value>
    Endurance: <value>
    Charisma: <value>
    Intelligence: <value>
    Luck: <value>
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # GPT-3.5 또는 GPT-4 사용
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates character stats."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.7,
    )

    # GPT로부터 받은 응답을 파싱하여 스탯 생성
    stats = parse_gpt_response(response.choices[0].message['content'])
    # 스탯 총합이 15가 되도록 조정
    stats = adjust_stats_to_sum_15(stats)
    return stats

def parse_gpt_response(response_text):
    """
    GPT 응답 텍스트를 파싱하여 캐릭터 스탯 딕셔너리로 변환하는 함수.
    """
    # 각 스탯의 이름을 예상한 대로 파싱합니다.
    lines = response_text.strip().split('\n')
    stats = {
        "strength": 1,      # 기본값 설정
        "perception": 1,
        "endurance": 1,
        "charisma": 1,
        "intelligence": 1,
        "luck": 1
    }

    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lower()
            if value.strip().isdigit():
                value = int(value.strip())
                # 예상하는 키 목록에 있는지 확인하고, 있다면 값 할당
                if key in stats:
                    # 최소값은 1로 설정, 최대값은 10으로 설정
                    stats[key] = max(1, min(value, 10))

    return stats

def adjust_stats_to_sum_15(stats):
    """
    스탯의 총합이 15가 되도록 조정하는 함수.
    """
    total = sum(stats.values())
    keys = list(stats.keys())
    
    while total != 15:
        if total > 15:
            # 스탯 총합이 15보다 클 경우, 랜덤으로 값을 1씩 줄입니다.
            for key in keys:
                if stats[key] > 1:
                    stats[key] -= 1
                    total -= 1
                    if total == 15:
                        break
        elif total < 15:
            # 스탯 총합이 15보다 작을 경우, 랜덤으로 값을 1씩 늘립니다.
            for key in keys:
                if stats[key] < 10:
                    stats[key] += 1
                    total += 1
                    if total == 15:
                        break

    return stats

