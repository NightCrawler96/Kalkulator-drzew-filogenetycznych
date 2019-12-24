import re
import sys
from typing import List

from newick import Node

from actions import create
from phylogenetic_trees.io import load_from_file
from phylogenetic_trees.trees import PhyTree
from phylogenetic_trees.visualization import visualize_tree


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


def load_tree(file_name) -> None or List[Node]:
    try:
        newick_tree = load_from_file(file_name)
        phy_tree = PhyTree(newick_tree)
        return phy_tree
    except IOError:
        print("File not accessible")
        exit()


def choose_action(tree: str, action_name: str):
    if action_name in ["--load", "-l"]:
        tree = load_tree(sys.argv[1])
        fun1()
    elif action_name in ["--save", "-s"]:
        fun2()
    elif action_name in ["--show", "-sh"]:
        phy_tree: PhyTree
        if re.match(r'[\S]*\.newick$', tree):
            phy_tree = load_tree(tree)
        elif re.match(r'\([\S ]+\}\;$', tree):
            phy_tree = PhyTree()
            try:
                phy_tree.parse_string(tree)
            except ValueError as e:
                print(e)
                exit()
        else:
            print("Post tree as a filename or string")
            exit()
        visualize_tree(phy_tree.get_newick()[0])
    elif action_name in ["--help", "-h"]:
        menu()
    elif action_name in ["--create", "-c"]:
        create(tree)
    else:
        print("Wrong name function")


def read_from_commandline():
    choose_action(sys.argv[1], sys.argv[2])


def read_from_user():
    print("Give file name with extension")
    argument1 = input()
    print("Give name action  --load  --save  --print --help --create --update")
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


if __name__ == "__main__":
    arguments_count = len(sys.argv) - 1

    if arguments_count <= 1:
        read_from_user()
    else:
        read_from_commandline()
