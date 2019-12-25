def ask_if_finished():
    return ask("Have you finished?")


def ask(question: str) -> bool:
    while True:
        print(f"{question} (yes/no)")
        answer = input()
        if answer == "yes":
            return True
        elif answer == "no":
            return False


def get_number() -> int:
    while True:
        try:
            num = int(input())
            return num
        except ValueError:
            print("Enter a number")

