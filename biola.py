import re
import sys
from typing import List, Any

from newick import Node

from actions import create, update, random_tree, consensus_tree
from phylogenetic_trees.io import load_from_file
from phylogenetic_trees.trees import PhyTree
from phylogenetic_trees.visualization import visualize_tree


def menu():
    print("Script menu")
    print("-------------------")
    print("Available functions:\n"
          "[file] --create, --update, --random-tree, --show\n"
          "--help, --consensus")
    print("Example calls:\n"
          "python biola.py tree.newick --show\n"
          "python biola.py --help")
    print(" ")


def load_tree(file_name) -> None or List[Node]:
    try:
        newick_tree = load_from_file(file_name)
        phy_tree = PhyTree(newick_tree)
        return phy_tree
    except IOError:
        print("File not accessible")
        exit()


def choose_action(tree: str, action_name: str, optional: str = None):
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
    elif action_name in ["--create", "-c"]:
        create(tree)
    elif action_name in ["--random-tree", "-r"]:
        if optional is None:
            random_tree(tree)
        else:
            random_tree(tree, int(optional))
    else:
        print("Wrong name function")


def read_from_commandline():
    choose_action(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3] if len(sys.argv) > 3 else None,
    )


def no_file_action():
    print("actions available: --help --consensus")
    action = input("Choose action: ")

    if action in ["--help", "-h"]:
        menu()
    elif action in ["--consensus", "-cons"]:
        consensus_tree()
    else:
        print("Unknown action")


if __name__ == "__main__":
    arguments_count = len(sys.argv)

    if arguments_count == 1:
        no_file_action()
    else:
        read_from_commandline()
