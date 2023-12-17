from html_parser.html_token import TokenType, Token


class HtmlParser():
    def __init__(self):
        self.tokens = []
        self.src = ""
        self.index = 0

    def eos(self):
        # end of src
        return self.index >= len(self.src)
    def parse(self,src):
        self.index = 0
        self.src = src
        self.tokens = []
        
        while not self.eos():
            ch = self.src[self.index]
            self.index += 1


            if ch == "<":
                tag = ""
                token_typ = TokenType.Tag_Open

                # handle closing tags
                if not self.eos() and self.src[self.index] == "/":
                    token_typ = TokenType.Tag_Close
                    self.index += 1

                while not self.eos() and self.src[self.index] != ">":
                    tag += self.src[self.index]
                    self.index += 1
                
                # make sure u closed the tag
                assert self.src[self.index] == ">" and "[Assertion Failed] Tag Not Closed"
                
                # skip tag closing
                self.index += 1

                self.tokens.append(Token(token_typ,tag))
            elif ch in [" ","\n","\t"]: continue
            else:
                text = ch
                while not self.eos() and self.src[self.index] not in ["<"," ","\n","\t"] :
                    text += self.src[self.index]
                    self.index += 1
                
                self.tokens.append(Token(TokenType.Text,text))
        return self.tokens


