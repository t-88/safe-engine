from enum import Enum

TokenType = Enum("TokenType",[
    "Tag_Open",
    "Tag_Close",
    "Text"
])

class Token():
    def __init__(self,typ,value):
        self.typ = typ
        self.value = value
    
    def __str__(self):
        return f"<Token typ={self.typ} value={self.value.encode()}>"

    def __repr__(self):
        return self.__str__()
