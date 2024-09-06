import openai
from dotenv import load_dotenv
import requests
import os

# OpenAI API 키 설정
load_dotenv(dotenv_path='GitH/.env')  # .env 파일을 로드하여 환경 변수를 설정
openai.api_key = os.getenv('OPENAI_API_KEY')  # 환경 변수에서 OpenAI API 키 가져오기

KAKAO_API_KEY = os.getenv('KAKAO_API_KEY')

# TRPG 프롬프트 실행
def generate_adventure(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
    "role": "system",
    "content": "You are a helpful assistant that creates text adventure games in Korean. Your task is to provide the game content structured into specific sections."
},
{
    "role": "user",
    "content": f"{prompt}\n\nPlease write the result in Korean. Organize the output into the following sections: [스테이터스], [인벤토리] 아이템 : 숫자, [스토리], [선택지], [선택횟수] 숫자만, [요약](요약이 없다면 [요약]만 출력하고 아래는 빈칸으로 출력해줘). Exclude any phrases like 'What will you choose?' or similar prompts for selection.Please do not include the '-' character in the output."
}

            ],
        max_tokens=1000,
        temperature=0.7
    )
    # GPT-4 응답 텍스트 추출
    return response['choices'][0]['message']['content']

# OpenAI를 사용하여 텍스트를 영어로 번역하는 함수
def translate_to_english(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 최신 모델로 변경
            messages=[{
                "role": "system",
                "content": "Translate the following text to English:"
            },
            {
                "role": "user",
                "content": prompt
            }],
            max_tokens=100
        )
        translation = response['choices'][0]['message']['content'].strip()
        return translation
    except Exception as e:
        print(f"Error translating text: {e}")
        return None

# 이미지 생성하기 요청 함수
def t2i(prompt):
    try:
        r = requests.post(
            'https://api.kakaobrain.com/v2/inference/karlo/t2i',
            json={
                "version": "v2.1", 
                "prompt": prompt,
                "height": 1024,
                "width": 1024,
                "samples": 1
            },
            headers={
                'Authorization': f'KakaoAK {KAKAO_API_KEY}',
                'Content-Type': 'application/json'
            }
        )
        
        if r.status_code == 200:
            response = r.json()
            return response['images'][0]['image'] if 'images' in response else None
        else:
            print(f"Error: {r.status_code}, {r.text}")
            return None
    except Exception as e:
        print(f"Error in image generation: {e}")
        return None
