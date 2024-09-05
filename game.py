from gptapi import generate_adventure

# 메인 스토리 리스트 초기화
story_list = []

# 프롬프트 생성 함수 (최초 스토리 및 선택지)
def get_main_story(world, char, aim, max_tokens=1000, min_tokens=700):
    prompt = f"""
    **World Setting:** {world}
    - This is the world where the adventure takes place. It includes details such as the environment, time period, and any specific rules or magic systems.

    **Character Traits:** {char}
    - This describes the main character the player will embody. Include their backstory, abilities, and personality traits that will influence their decisions and actions within the game.

    **Objective:** {aim}
    - This is the goal or mission that the character is striving to achieve. It should drive the story forward and provide clear motivation for the player’s actions.

    Requirements:
    - Respond in Korean.
    - Write a main story based on these details and provide 4 different choices the 'user' can make.
    - The story should be between {min_tokens} and {max_tokens} tokens.
    """
    # 첫 번째 스토리 생성
    story = generate_adventure(prompt)
    # 생성된 스토리를 리스트에 저장
    story_list.append(story)
    return story

# 다음 스토리 생성 함수 (사용자의 선택 반영)
def generate_next_story(user_choice, max_tokens=1000, min_tokens=700):
    previous_story = "\n".join(story_list)
    
    # 사용자 선택에 따라 다음 스토리 요청
    prompt = f"""
    **Previous Story:** {previous_story}
    
    **User Choice:** {user_choice}

    - Based on the user's choice, continue the story logically. Ensure the new story is consistent with previous events and decisions.
    - Provide 4 new choices the 'user' can make to influence the direction of the story.
    - The story should be between {min_tokens} and {max_tokens} tokens.
    """
    
    # 새로운 스토리 생성
    next_story = generate_adventure(prompt)
    
    # 생성된 스토리를 리스트에 저장
    story_list.append(next_story)
    
    return next_story

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

# 메인 게임 루프
def main():
    # 초기 설정을 위한 사용자 입력
    world = input("Enter the world setting: ")
    char = input("Enter the character traits: ")
    aim = input("Enter the objective: ")

    # 첫 번째 스토리 출력
    print("\n첫 번째 스토리:\n")
    print(get_main_story(world, char, aim))

    # 사용자 입력을 기다리는 루프
    user_responses = 1
    minimum_responses = 5  # 최소 5번의 선택이 이루어지도록 설정
    while True:
        user_choice = input("\n어떤 행동을 선택하시겠습니까? (1, 2, 3, 4 중 숫자로 선택, 게임 종료: 'exit'): ")
        if user_choice.lower() == 'exit':
            print("게임이 종료되었습니다. 언제든지 다시 시작할 수 있습니다.")
            break
        
        # 유효한 선택인지 확인
        if user_choice not in ['1', '2', '3', '4']:
            print("유효한 선택을 입력하세요 (1, 2, 3, 4 중 선택).")
            continue

        # 선택에 따른 새로운 스토리 생성
        print("\n다음 스토리:\n")
        print(generate_next_story(user_choice))

        # 사용자 선택 횟수 업데이트
        user_responses += 1

        # 최소 5번 선택이 완료된 후 엔딩 가능성
        if user_responses >= minimum_responses:
            # 최소 5번 선택을 완료한 경우 엔딩이 나올 수 있음
            print(f"\n{minimum_responses}번 이상의 선택이 이루어졌습니다. 적절한 시점에서 엔딩을 볼 수 있습니다.")

if __name__ == "__main__":
    main()