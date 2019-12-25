import re
import sys
from typing import List

from newick import Node

from actions import create, update
from phylogenetic_trees.io import load_from_file
from phylogenetic_trees.trees import PhyTree
from phylogenetic_trees.visualization import visualize_tree


def menu():
    print("Script menu")
    print("-------------------")
    print("First argument is name file to read")
    print("Second argument is action, available actions: --show --create --update --help")
    print("Next arguments aren't read")
    print("Example call: python biola.py tree.newick --show")
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
    if action_name in ["--update", "-u"]:
        update(tree)
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
    argument1 = input("Give file name with extension: ")
    print("Give name action --show --help --create --update")
    argument2 = input()

    choose_action(argument1, argument2)


if __name__ == "__main__":
    arguments_count = len(sys.argv) - 1

    if arguments_count <= 1:
        read_from_user()
    else:
        read_from_commandline()
