#!/usr/bin/env python3
"""
Activity 2: AI-Generated Trivia Night (STARTER)

Follow the numbered TODOs in order. Run the file often to test as you go:
    python code/trivia_starter.py
"""
# TODO 1: Build a list of at least 5 dictionaries, each with "question",
# "answer", and "category" keys. Ask AI to help generate content, then
# double-check the answers yourself. Example shape:
# {"question": "What is the capital of France?", "answer": "Paris", "category": "Geography"}
QUESTIONS = [
    {
        "question": "What is the largest planet in our solar system?",
        "answer": "Jupiter",
        "category": "Science",
    },
    {
        "question": "What country is famous for the Eiffel Tower?",
        "answer": "France",
        "category": "Geography",
    },
    {
        "question": "How many sides does a triangle have?",
        "answer": "Three",
        "category": "Mathematics",
    },
    {
        "question": "Who painted the Mona Lisa?",
        "answer": "Leonardo da Vinci",
        "category": "Art and History",
    },
    {
        "question": "What is the fastest land animal?",
        "answer": "Cheetah",
        "category": "Nature and Animals",
    },
]


def ask_question(question):
    """Ask one question, check the answer, and return True or False."""

    print(f"\n[{question['category']}] {question['question']}")
    # TODO 4: Wrap this input() call (and the comparison below) in a
    # try/except so a blank or unexpected answer doesn't crash the program.
    # If something goes wrong, print a friendly message and return False.
    
    answer = input("Your answer: ")
    try:
        answer = input("Your answer: ")
        if answer.strip() == "":
            print("Please enter an answer next time.")
            return False
    
    # TODO 2-3: Compare `answer` to question["answer"]. Use .strip() and
    # .lower() on both sides so extra spaces/capitalization don't count
    # as wrong. Return True if it matches, False otherwise.

        return answer.strip().lower() == question["answer"].strip().lower()
    except EOFError:
        print("No answer was entered.")
        return False


def main():
    print("=== Trivia Night ===\n")

    score = 0
    question_count = 0
    # TODO 5: Loop over QUESTIONS with a for loop. Call ask_question() for
    # each one, print "Correct!" or "Nope, the answer was ..." and keep a
    # running score.
    for question in QUESTIONS:
        question_count = question_count + 1
        if ask_question(question):
            print("Correct!")
            score = score + 1
        else:
            print(f"Nope, the answer was {question['answer']}.")

    print(f"\nFinal score: {score}/{question_count}")


if __name__ == "__main__":
    main()
