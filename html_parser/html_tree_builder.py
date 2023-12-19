from html_parser.html_token import TokenType, Token
from html_parser.tree_node import TreeNode,TreeNodeType
import helper


class HtmlTreeBuilder():
    def __init__(self):
        self.tree = []
        self.index = 0
        self.tokens = []

        # data that is not shown in the website like title, doctype and links....
        self.metadata_tags = ["meta","title"]
        self.html_metadata = {}

        # tags i dont want to handle yet
        self.skippable_tags = ["style","head"] 
        self.skipped_nodes = []

        #TODO: add token in parser for this type of tags
        # self closing tags
        self.self_closing = ["meta"]


    def eot(self):
        return self.index >= len(self.tokens) or self.tokens[self.index].typ == TokenType.Eof  


    def build(self,tokens):
        self.tree = TreeNode(typ=TreeNodeType.Root,value=[])
        self.tokens = tokens
        self.index = 0

        while not self.eot():
            node = self.parse_self_closing_tags()
            if node: self.tree.value.append(node)
            
        return self.tree
    
    def parse_self_closing_tags(self):
        if self.eot(): return None

        if self.tokens[self.index].typ == TokenType.Tag_Open and self.tokens[self.index].value in self.self_closing:
            node = TreeNode(
                tag=self.parse_basic(),
                props=self.parse_props(),
                value=[],
            )
            
            if node.tag in self.metadata_tags:
                self.html_metadata[node.tag] = [node.props,node.value]
                return  
            
            if node.tag in self.skippable_tags:
                self.skipped_nodes.append(node)
                return              

            return node
        
        return self.parse_tag()
    
    def parse_tag(self):
        if self.eot(): return None

        if self.tokens[self.index].typ == TokenType.Tag_Open:
            node = TreeNode(
                tag=self.parse_basic(),
                props=self.parse_props(),
                value=[],
            )
            
            while not self.eot() and self.tokens[self.index].typ != TokenType.Tag_Close:
                elem = self.parse_self_closing_tags()
                if elem != None: node.value.append(elem)


            # skip the Tag_Close Token
            self.index += 1


            if node.tag in self.metadata_tags:
                self.html_metadata[node.tag] = [node.props,node.value]
                return  
            
            if node.tag in self.skippable_tags:
                self.skipped_nodes.append(node)
                return              

            print(node.tag)
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
            out_str = ""
            # start of the doc
            for node in elem.value:
                out_str += self.print(node)
            return out_str
        elif elem.typ == TreeNodeType.Node:
            # print tag with its props
            out_str = f"{'    ' * depth}{elem.tag} {elem.props if len(elem.props) else ''}\n"
            
            print(f"{'    ' * depth}{elem.tag}",end=" ")
            print(elem.props if len(elem.props) else "")

            for node in elem.value:
                out_str += self.print(node,depth=depth + 1)
            return out_str
        elif elem.typ == TreeNodeType.Literal:
            # print the text
            print(f"{'    ' * depth}{elem.value}")
            return f"{'    ' * depth}{elem.value}\n"
        else:
            print(f"[Unreachable] Unkown TreeNode {elem}")
            exit(-1)
