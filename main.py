import json
import random
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_question_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base.get("tanya-jawab", []):
        questions_list = q.get('tanya', [])
        if question in questions_list:
            answers = q.get('jawab', [])
            return random.choice(answers) if answers else None
    return None


def chat_bot():
    knowledge_base: dict = load_knowledge_base('dataset/JSON/kusukabeTsumugi.json')

    while True:
        user_input: str = input('kamu:')

        if user_input.lower() == 'quit':
            break

        questions: list = [question for item in knowledge_base.get("tanya-jawab", []) for question in item.get("tanya", [])]
        best_match: str | None = find_question_match(user_input, questions)

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'nurse-t: {answer}')
        else:
            print('idk teach me')
            new_answer: str = input('type ans or skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base['tanya-jawab'].append({'tanya': user_input, 'jawab': new_answer})
                save_knowledge_base('dataset/JSON/kusukabeTsumugi.json', knowledge_base)
                print('tq')


if __name__ == '__main__':
    chat_bot()
