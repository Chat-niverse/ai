# 필요한 모듈과 함수 임포트
from gptapi import generate_adventure

def create_adventure_game(world, char, aim):
    prompt = f"""
    You are about to create a text-based adventure game. The setting, character, and goal are defined by the user as follows:

    **World Setting:** {world}
    - This is the world where the adventure takes place. It includes details such as the environment, time period, and any specific rules or magic systems.

    **Character Traits:** {char}
    - This describes the main character the player will embody. Include their backstory, abilities, and personality traits that will influence their decisions and actions within the game.

    **Objective:** {aim}
    - This is the goal or mission that the character is striving to achieve. It should drive the story forward and provide clear motivation for the player’s actions.

    Using these details, create a compelling and interactive text-based adventure game. The game should:
    - Introduce the setting and character in an engaging way.
    - Present challenges and decisions that align with the character’s traits and the game’s world.
    - Include branching narratives based on the player’s choices.
    - Aim to reach the goal specified by the user, with possible multiple endings depending on player actions.

    Start the game with an introductory scene that hooks the player and sets the tone for the adventure. Each segment should provide the player with choices, allowing them to guide the narrative towards their objective.
    """
    return prompt

def main():
    # 초기 설정을 위한 사용자 입력
    world = input("Enter the world setting: ")
    char = input("Enter the character traits: ")
    aim = input("Enter the objective: ")

    # 첫 번째 프롬프트 생성 및 게임 시작
    prompt = create_adventure_game(world, char, aim)
    story = generate_adventure(prompt)
    print(story)

    # 게임 루프: 사용자의 선택에 따라 이야기를 계속 생성
    while True:
        user_choice = input("\n당신의 선택은? (게임을 종료하려면 'exit' 입력): ")
        if user_choice.lower() == 'exit':
            print("게임을 종료합니다.")
            break
        
        # 이전 이야기와 사용자의 선택을 기반으로 새로운 프롬프트 생성
        prompt += f"\n\n사용자의 선택: {user_choice}\n이에 따라 이야기를 계속 이어가 주세요."
        story = generate_adventure(prompt)
        print(story)

if __name__ == "__main__":
    main()
