import openai
from dotenv import load_dotenv
import os

# OpenAI API 키 설정
load_dotenv(dotenv_path='.env')  # .env 파일을 로드하여 환경 변수를 설정
openai.api_key = os.getenv('OPENAI_API_KEY')  # 환경 변수에서 OpenAI API 키 가져오기

def generate_adventure(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
    "role": "system",
    "content": "You are a helpful assistant that creates text adventure games in Korean. Your task is to provide the game content structured into specific sections."
},
{
    "role": "user",
    "content": f"{prompt}\n\nPlease write the result in Korean. Organize the output into the following sections: [스테이터스], [인벤토리] 아이템 : 숫자, [스토리], [선택지], [선택횟수] 숫자만. Exclude any phrases like 'What will you choose?' or similar prompts for selection.Please do not include the '-' character in the output."
}

            ],
        max_tokens=1000,
        temperature=0.7
    )
    # GPT-4 응답 텍스트 추출
    return response['choices'][0]['message']['content']
