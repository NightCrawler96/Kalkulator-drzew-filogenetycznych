def ask_if_finished():
    while True:
        print("Have you finished? (yes/no)")
        answer = input()
        if answer == "yes":
            return True
        elif answer == "no":
            return False
