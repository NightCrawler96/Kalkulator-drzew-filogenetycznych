import sys


def fun1():
    print("Fun1")


def fun2():
    print("Fun2")


def fun3():
    print("Fun3")


def menu():
    print("Script menu")
    print("-------------------")
    print("First argument is name file to read")
    print("Second argument is action, available actions: --load, --save, --print, --help")
    print("Next arguments aren't read")
    print("Example call: biola.py file.txt --load")
    print(" ")


def read_from_commandline():
    try:
        f = open(sys.argv[1])
    except IOError:
        sys.argv[2] = "never mind"
        print("File not accessible")

    if sys.argv[2] == "--load" or sys.argv[2] == "load":
        fun1()
    elif sys.argv[2] == "--save" or sys.argv[2] == "save":
        fun2()
    elif sys.argv[2] == "--print" or sys.argv[2] == "print":
        fun3()
    elif sys.argv[2] == "--help" or sys.argv[2] == "help":
        menu()
    else:
        print("Wrong name function")


def read_from_user():
    print("Give file name with extension")
    argument1 = input()
    print("Give name action  --load  --save  --print --help ")
    argument2 = input()

    try:
        f = open(argument1)
    except IOError:
        print("File not accessible")
        argument2 = "never mind"

    if argument2 == "--load" or argument2 == "load":
        fun1()
    elif argument2 == "--save" or argument2 == "save":
        fun2()
    elif argument2 == "--print" or argument2 == "print":
        fun3()
    elif argument2 == "--help" or argument2 == "help":
        menu()
    else:
        print("Error - check argument 1 and 2")


menu()
arguments_count = len(sys.argv) - 1

if arguments_count <= 1:
    read_from_user()
else:
    read_from_commandline()
