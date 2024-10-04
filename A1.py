import os
from typing import Union, List, Optional

alphabet_chars = list("abcdefghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
numeric_chars = list("0123456789")
var_chars = alphabet_chars + numeric_chars
all_valid_chars = var_chars + ["(", ")", ".", "\\"]
valid_examples_fp = "./valid_examples.txt"
invalid_examples_fp = "./invalid_examples.txt"


def read_lines_from_txt(fp: [str, os.PathLike]) -> List[str]:
    """
    :param fp: File path of the .txt file.
    :return: The lines of the file path removing trailing whitespaces
    and newline characters.
    """
    # TODO
    with open(fp) as file:
        lines = [line.rstrip() for line in file]
    return lines


def is_valid_var_name(s: str) -> bool:
    """
    :param s: Candidate input variable name
    :return: True if the variable name starts with a character,
    and contains only characters and digits. Returns False otherwise.
    """
    # TODO
    for char in s:
        if char not in var_chars:
            return False
    if s[0] in numeric_chars:
        return False
    elif s[0] in alphabet_chars:
        return True
    return False


class Node:
    """
    Nodes in a parse tree
    Attributes:
        elem: a list of strings
        children: a list of child nodes
    """
    def __init__(self, elem: List[str] = None):
        self.elem = elem
        self.children = []


    def add_child_node(self, node: 'Node') -> None:
        self.children.append(node)


class ParseTree:
    """
    A full parse tree, with nodes
    Attributes:
        root: the root of the tree
    """
    def __init__(self, root):
        self.root = root

    def print_tree(self, node: Optional[Node] = None, level: int = 0) -> None:
        # TODO
        print("") # ---- per level
        print('_'.join(self.root.elem))
        children = self.root.children
        for child in children:
            print('----'+"_".join(child.elem))
            for grandkid in child.children:
                print('--------'+"_".join(grandkid.elem))
                for greatgrandkid in grandkid.children:
                    print('------------'+"_".join(greatgrandkid.elem))
                    for greatgreatgrandkid in greatgrandkid.children:
                        print('----------------'+"_".join(greatgreatgrandkid.elem))
                        for greatgreatgrandkid2 in greatgreatgrandkid.children:
                           print('--------------------'+"_".join(greatgreatgrandkid2.elem))



def parse_tokens(s_: str, association_type: Optional[str] = None) -> Union[List[str], bool]:
    """
    Gets the final tokens for valid strings as a list of strings, only for valid syntax,
    where tokens are (no whitespace included)
    \\ values for lambdas
    valid variable names
    opening and closing parenthesis
    Note that dots are replaced with corresponding parenthesis
    :param s_: the input string
    :param association_type: If not None, add brackets to make expressions non-ambiguous
    :return: A List of tokens (strings) if a valid input, otherwise False
    """

    s = s_[:]  #  Don't modify the original input string
    # TODO
    if s == "":
        print("Token Empty")
        return False
    else:
        finalStrList = []
        i = 0
        dotCount = 0
        openBrackets = []
        closedBrackets = []
        for i in range(len(s)):
            if s[i] in var_chars:
                j = i
                if i < len(s)-1:
                    if s[i+1] not in var_chars:
                        if is_valid_var_name(s[j:i+1]):
                            finalStrList.append(s[j:i+1])
                        else:
                            print("invalid variable name at index "+str(i))
                            return False
                else:
                    if is_valid_var_name(s[j:]):
                            finalStrList.append(s[j:])
                    else:
                        print("invalid variable name at index " + str(i))
                        return False
            elif s[i] == ' ':
                i = i + 1
            elif s[i] not in all_valid_chars:
                            print('Invalid Character '+s[j]+' encountered at index '+str(j))
                            return False 
            elif s[i] == '\\':
                if s[i+1] in alphabet_chars:
                    finalStrList.append('\\')
                elif s[i+1] == ' ':
                    print('Invalid space inserted after \\ at index '+str(i))
                    return False
                else:
                    print('Backslashes not followed by a variable name at '+str(i))
                    return False
            elif s[i] == '.':
                if s[i-1] in alphabet_chars:
                    count = 1
                    while s[i+count] == ' ':
                        count = count + 1
                    if s[i+count] in alphabet_chars or s[i+1] =='(' or s[i+1] =='\\':
                        finalStrList.append('(')
                        dotCount = dotCount + 1
                    else:
                        print('Invalid Character following dot at index '+str(i))
                        return False
                else:
                    print("Must have a variable name before character '.' at index "+str(i))
                    return False
            elif s[i] == '(':
                finalStrList.append('(')
                openBrackets.append(i)
            elif s[i] == ')':
                finalStrList.append(')')
                closedBrackets.append(i)
        if len(openBrackets) < len(closedBrackets):
            print("Bracket ) at index: "+str(closedBrackets[-1])+" not matched with a opening bracket '('")
            return False
        elif len(openBrackets) > len(closedBrackets):
            print("Bracket ( at index: "+str(openBrackets[-1])+" not matched with a closing bracket ')'")
            return False
        if dotCount > 0:
            for i in range(dotCount):
                finalStrList.append(')')
    return finalStrList


def read_lines_from_txt_check_validity(fp: [str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then
    parses each string  to yield a tokenized list of strings for printing, joined by _ characters
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens function).
    :param lines: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    valid_lines = []
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            valid_lines.append(l)
            print(f"The tokenized string for input string {l} is {'_'.join(tokens)}")
    if len(valid_lines) == len(lines):
        print(f"All lines are valid")



def read_lines_from_txt_output_parse_tree(fp: [str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then
    parses each string to yield a tokenized output string, to be used in constructing a parse tree. The
    parse tree should call print_tree() to print its content to the console.
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens function).
    :param fp: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            print("\n")
            parse_tree2 = build_parse_tree(tokens)
            parse_tree2.print_tree()


def add_associativity(s_: List[str], association_type: str = "left") -> List[str]:
    """
    :param s_: A list of string tokens
    :param association_type: a string in [`left`, `right`]
    :return: List of strings, with added parenthesis that disambiguates the original expression
    """

    # TODO Optional
    s = s_[:]  # Don't modify original string
    return []




def build_parse_tree_rec(tokens: List[str], node: Optional[Node] = None) -> Node:
    """
    An inner recursive inner function to build a parse tree
    :param tokens: A list of token strings
    :param node: A Node object
    :return: a node with children whose tokens are variables, parenthesis, slashes, or the inner part of an expression
    """

    #TODO
    if node == None:
        root = Node(tokens)
    else:
        root = node
    i = 0
    while i < len(tokens):
        if tokens[i] == '(':
                j = i+1
                closeCount = 1
                while closeCount > 0 and j < len(tokens):
                    if tokens[j] == '(':
                        closeCount = closeCount + 1
                    elif tokens[j] == ')':
                        closeCount = closeCount - 1
                    j = j + 1
                new_node = Node(tokens[i:j])
                new_node1 = Node(tokens[i])
                new_node2 = Node(tokens[j-1])
                new_node.add_child_node(new_node1)
                if len(tokens[i+1:j-1]) > 1:
                    new_node.add_child_node(build_parse_tree_rec(tokens[i+1:j-1]))
                else:
                    build_parse_tree_rec(tokens[i+1:j-1], new_node)
                new_node.add_child_node(new_node2)
                root.add_child_node(new_node)
                
                i = j-1
        elif tokens[i] == '\\':
            root.add_child_node(Node([tokens[i]]))
            i = i + 1
        elif tokens[i] == ')':
            i = i+1
        else:
            root.add_child_node(Node([tokens[i]]))
            i = i + 1
    return root


def build_parse_tree(tokens: List[str]) -> ParseTree:
    """
    Build a parse tree from a list of tokens
    :param tokens: List of tokens
    :return: parse tree
    """
    pt = ParseTree(build_parse_tree_rec(tokens))
    return pt


if __name__ == "__main__":
    
    print("\n\nChecking valid examples...")
    read_lines_from_txt_check_validity(valid_examples_fp)
    read_lines_from_txt_output_parse_tree(valid_examples_fp)

    print("Checking invalid examples...")
    #read_lines_from_txt_check_validity(invalid_examples_fp)

    # Optional
    #print("\n\nAssociation Examples:")
    #sample = ["a", "b", "c"]
    #print("Right association")
    #associated_sample_r = add_associativity(sample, association_type="right")
    #print(associated_sample_r)
    #print("Left association")
    #associated_sample_l = add_associativity(sample, association_type="left")
    #print(associated_sample_l)
