from html_parser.html_token import TokenType, Token
from enum import Enum
import helper

TreeNodeType = Enum("TreeNodeType",[
    "Root",
    "Node",
    "Literal"
])

class TreeNode():
    def __init__(self,typ = TreeNodeType.Node, tag = "",value = "",props = []):
        self.value = value
        self.tag = tag
        self.props = props
        self.typ = typ

    def __str__(self):
        props = f"props={self.props} " if len(self.props) != 0 else ""
        tag = f"tag={self.tag} " if self.tag else ""
        value =  f"value={self.value}" if self.value else ""

        return f"<TreeNode {tag}{props}{value}>"

    def __repr__(self):
        return self.__str__()

class HtmlTreeBuilder():
    def __init__(self):
        self.tree = []
        self.index = 0
        self.tokens = []

        # data that is not shown in the website like title, doctype and links....
        self.html_metadata = {}

    def eot(self):
        return self.index >= len(self.tokens) or self.tokens[self.index].typ == TokenType.Eof  


    def build(self,tokens):
        self.tree = TreeNode(typ=TreeNodeType.Root,value=[])
        self.tokens = tokens
        self.index = 0

        while not self.eot():
            node = self.parse_tag()
            if node: self.tree.value.append(node)
            
        return self.tree

    def parse_tag(self):
        if self.eot(): return None

        if self.tokens[self.index].typ == TokenType.Tag_Open:
            node = TreeNode(
                tag=self.parse_basic(),
                props=self.parse_props(),
                value=[],
            )
            
            while not self.eot() and self.tokens[self.index].typ != TokenType.Tag_Close:
                node.value.append(self.parse_tag())
            
            # skip the Tag_Close Token
            self.index += 1
            return node
        
        return self.parse_basic()

    def parse_basic(self):
        if self.eot(): return None

        token = self.tokens[self.index]
        self.index += 1
        node = None
        
        if token.typ == TokenType.Tag_Open:
            node = token.value
        elif token.typ == TokenType.Text:
            value =  token.value
            while not self.eot() and self.tokens[self.index].typ == TokenType.Text:
                value += " " + self.tokens[self.index].value
                self.index += 1
            return TreeNode(typ=TreeNodeType.Literal, value=value) 
        elif token.typ == TokenType.Doctype:
            self.html_metadata["Doctype"] = self.parse_props()
            return
        else:
            print(f"[Unreachable] Unhandled Token Type in TreeBuilder token={token}")
            exit(-1)

        return node 

    def parse_props(self):
        props = []
        while not self.eot() and self.tokens[self.index].typ == TokenType.Tag_Prop:
            props.append(self.tokens[self.index].value)
            self.index += 1
        return props



    def print(self,elem = None,depth = 0):
        if elem == None: elem = self.tree

        if elem.typ == TreeNodeType.Root:
            # start of the doc
            for node in elem.value:
                self.print(node)
        elif elem.typ == TreeNodeType.Node:
            # print tag with its props
            print(f"{'    ' * depth}{elem.tag}",end=" ")
            print(elem.props if len(elem.props) else "")

            for node in elem.value:
                self.print(node,depth=depth + 1)
        elif elem.typ == TreeNodeType.Literal:
            # print the text
            print(f"{'    ' * depth}{elem.value}")
        else:
            print(f"[Unreachable] Unkown TreeNode {elem}")
            exit(-1)
