from enum import Enum

TokenType = Enum("TokenType",[
    "Tag_Open",
    "Tag_Close",
    "Tag_Prop",
    "Doctype",
    "Eof",
    "Text"
])

class Token():
    def __init__(self,typ,value = ""):
        self.typ = typ
        self.value = value
    
    def __str__(self):
        if self.value:
            return f"<Token typ={self.typ} value={self.value.encode()}>"
        return f"<Token typ={self.typ}>"
    def __repr__(self):
        return self.__str__()
