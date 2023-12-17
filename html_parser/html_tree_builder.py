from html_parser.html_token import TokenType, Token

class TreeNode():
    def __init__(self,tag = "",value = ""):
        self.value = value
        self.tag = tag

    def __str__(self):
        if self.tag:
            return f"<TreeNode tag={self.tag} value={self.value}>"
        return f"<TreeNode value={self.value}>"

    def __repr__(self):
        return self.__str__()

class HtmlTreeBuilder():
    def __init__(self):
        self.tree = []
        self.index = 0
        self.tokens = []

    def eot(self):
        return self.index >= len(self.tokens) 


    def build(self,tokens):
        self.tree = []
        self.tokens = tokens
        self.index = 0

        while not self.eot():
            self.tree.append(self.parse_tag())
            self.index += 1
        return self.tree

    def parse_tag(self):
        if self.eot(): return None

        if self.tokens[self.index].typ == TokenType.Tag_Open:
            node = TreeNode(
                tag=self.parse_basic(),
                value=[]
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
            value = token.value
            while not self.eot() and self.tokens[self.index].typ == TokenType.Text:
                value += " " + self.tokens[self.index].value
                self.index += 1
            return value
        else:
            print(f"[Unreachable] Unhandled Token Type in TreeBuilder token={token}")
            exit(-1)

        return node 


    def print(self,elem = None,depth = 0):
        if elem == None: elem = self.tree

        if type(elem) == list:
            tree = elem
            for node in tree:
                self.print(node)
        else:
            if type(elem) == TreeNode:
                print(f"{'    ' * depth}{elem.tag}")
                for child in elem.value:
                    self.print(elem= child,depth= depth + 1)
            else:
                print(f"{'    ' * depth}{elem}")