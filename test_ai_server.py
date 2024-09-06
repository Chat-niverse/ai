import json
import requests

def load_request_data(file_path):
    """JSON 파일에서 요청 데이터를 로드합니다."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def save_response_data(file_path, data):
    """응답 데이터를 JSON 파일로 저장합니다."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    # 요청 데이터를 파일에서 로드
    request_data = load_request_data('request_data.json')
    
    # 서버에 요청 전송
    try:
        response = requests.post('http://127.0.0.1:5000/ai/process', json=request_data)
        response.raise_for_status()  # 오류가 있는 경우 예외 발생
        
        # 응답 데이터 JSON 파일로 저장
        save_response_data('response_data.json', response.json())
        
        print("응답이 response_data.json 파일에 저장되었습니다.")
    
    except requests.exceptions.RequestException as e:
        print(f"요청 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
