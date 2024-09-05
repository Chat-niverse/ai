import openai
import time
from dotenv import load_dotenv
import os

# OpenAI API 키 설정
load_dotenv(dotenv_path='./env')  # .env 파일을 로드하여 환경 변수를 설정
openai.api_key = os.getenv('OPENAI_API_KEY')  # 환경 변수에서 OpenAI API 키 가져오기

def generate_adventure(prompt):
    try:
        # GPT-3.5-turbo 모델을 사용하여 텍스트 어드벤처 게임 생성
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 모델 설정
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates text adventure games in Korean."},
                {"role": "user", "content": f"{prompt}\n\n결과를 한국어로 작성해 주세요."}
            ],
            max_tokens=1000,  # 응답의 최대 토큰 수 (필요에 따라 조정 가능)
            n=1,  # 응답 개수
            stop=None,  # 응답 종료를 위한 문구 (없으면 전체 생성)
            temperature=0.7  # 텍스트 다양성 조절 (0~1 사이 값)
        )
        
        # 생성된 텍스트 추출
        adventure_text = response.choices[0].message['content'].strip()
        return adventure_text

    except Exception as e:
        # 예외 발생 시 오류 메시지 출력
        return f"An error occurred: {e}"