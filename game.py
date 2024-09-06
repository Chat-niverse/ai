from gptapi import generate_adventure
import openai

# 메인 스토리 리스트 초기화
story_list = []

# 프롬프트 생성 함수 (최초 스토리, 선택지 및 이미지)
def get_main_story(world, char_traits, aim, max_tokens=1000, min_tokens=700):
    # 메인 스토리 생성 프롬프트
    story_prompt = f"""
    World Setting: {world}
    - This is the world where the adventure takes place. It includes details such as the environment, time period, and any specific rules or magic systems.

    Character Name:
    - Generate a suitable character name for the main character based on the world setting.

    Character Traits: {char_traits}
    - This describes the main character the player will embody.

    Objective: {aim}
    - This is the goal or mission that the character is striving to achieve. It should drive the story forward and provide clear motivation for the player’s actions.

    Requirements:
    - Respond in Korean and ensure the text follows proper spelling and grammar rules.
    - Write a main story based on these details.
    - The story should introduce a character name that suits the setting and genre.
    - The story should be written in a continuous, narrative style like a novel, without using lists or bullet points.
    - The story should be between {min_tokens} and {max_tokens} tokens.
    """
    
    # 메인 스토리 생성
    story = generate_adventure(story_prompt)
    
    # 선택지 생성 프롬프트 (생성된 메인 스토리에 적합한 선택지)
    choices_prompt = f"""
    Main Story: {story}

    - Based on the main story, generate 4 different choices the character can make to influence the next step of the story.
    - The choices should be relevant to the current situation and challenges presented in the story.
    - The choices should be written in Korean and follow proper spelling and grammar rules.
    """
    
    # 선택지 생성
    choices = generate_adventure(choices_prompt)
    
    # 선택지를 리스트로 분리
    choices_list = choices.strip().split('\n')

    # 생성된 스토리를 리스트에 저장
    story_list.append(story)

    '''# 이미지 생성 프롬프트 (캐릭터 얼굴에 초점을 맞춘 이미지 생성)
    image_prompt = f"""
    Create a detailed portrait of the main character based on the following traits:
    - Main character: {char_traits}.
    - The environment and situation described in the story: {world}.
    
    Focus on creating a realistic depiction of the character's face and emotions.
    """'''

    '''# 이미지 생성 요청
    try:
        response = openai.Image.create(
            prompt=image_prompt[:1000],  # 프롬프트 길이를 1000자로 제한
            n=1,
            size="1024x1024"  # 이미지 크기
        )
        # 이미지 URL 추출
        image_url = response['data'][0]['url']
    except Exception as e:
        # 예외 발생 시 오류 처리
        image_url = f"이미지 생성 실패: {e}"'''
    image_url = None
    return story, choices_list

# 다음 스토리 생성 함수 (사용자의 선택 반영)
def generate_next_story(user_choice, max_tokens=1000, min_tokens=700):
    previous_story = "\n".join(story_list)
    
    # 사용자 선택에 따라 다음 스토리 요청
    prompt = f"""
    Previous Story: {previous_story}
    
    User Choice: {user_choice}

    - Based on the user's choice, continue the story logically. Ensure the new story is consistent with previous events and decisions.
    - Provide 4 new choices the 'user' can make to influence the direction of the story.
    - In the choices, use "나" to represent the main character and ensure other characters are referred to by their names.
    - The choices should be relevant to the events and challenges presented in the story.
    - The choices should be written in Korean and follow proper spelling and grammar rules.
    """
    
    # 새로운 스토리 생성
    next_story = generate_adventure(prompt)
    
    # 선택지 생성 프롬프트 (플레이어 이름 제외, "나" 사용)
    choices_prompt = f"""
    Main Story: {next_story}

    - Based on the current situation in the story, generate 4 relevant choices that the player can make without mentioning the player's name but using "나".
    - The choices should be related to the events and challenges in the story, and other characters should be referred to by their names if necessary.
    - The choices should be written in Korean and follow proper spelling and grammar rules.
    """
    
    # 선택지 생성
    choices = generate_adventure(choices_prompt)
    
    # 선택지를 리스트로 분리
    choices_list = choices.strip().split('\n')
    
    # 새로운 스토리 리스트에 저장
    story_list.append(next_story)
    
    # 스토리와 선택지를 반환하고 선택지 리스트 삭제
    full_story = f"{next_story.strip()}\n\n" + "\n".join(choices_list) + "\n\n어떤 행동을 선택하시겠습니까?"

    # 선택지 리스트 삭제
    del choices_list
    
    return full_story

# 엔딩 처리 함수 (게임 종료 후 리스트 초기화)
def handle_ending(is_good_ending, user_responses, minimum_responses):
    if user_responses < minimum_responses:
        print(f"\n아직 {minimum_responses}번 이상의 선택이 이루어지지 않았습니다. 게임을 계속 진행하세요.")
        return False  # 엔딩을 보여주지 않고 계속 진행

    if is_good_ending:
        print("\n축하합니다! 당신은 목표를 달성했습니다! 게임이 끝났습니다.")
    else:
        print("\n유감입니다. 당신은 죽었습니다. 게임이 끝났습니다.")
    
    # 게임 종료 후 스토리 리스트 초기화
    story_list.clear()
    return True  # 게임 종료

# main 게임
def main():
    # 초기 설정을 위한 사용자 입력
    world = '중세시대 유럽'
    char_background = '가정적인 농부'
    goal = '마왕처치'
    a, b= get_main_story(world, char_background, goal)

    print('story', a)
    print('choices', b)
if __name__ == "__main__":
    main()