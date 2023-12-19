from enum import Enum

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