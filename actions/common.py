import os
from typing import Any


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


def get_type(T: type) -> Any:
    while True:
        try:
            num = T(input())
            return num
        except ValueError:
            print(f"Enter a {T}")


def get_integer() -> int:
    return get_type(int)


def get_float() -> float:
    return get_type(float)


def get_file_path() -> str:
    while True:
        file = input("File path: ")
        if os.path.isfile(file):
            return file
        else:
            print("Couldn't find that file")

