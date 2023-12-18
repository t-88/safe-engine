from html_parser.html_token import TokenType, Token
import helper


class HtmlParser():
    def __init__(self):
        self.tokens = []
        self.src = ""
        self.index = 0

    def eos(self,offset = 0):
        # end of src
        return self.index + offset >= len(self.src)
    

    def parse(self,src):
        self.index = 0
        self.src = src
        self.tokens = []
        
        while not self.eos():
            ch = self.src[self.index]
            self.index += 1



            if ch == "<":
                text = ""
                token_typ = TokenType.Tag_Open
                tokenzied_tag = False


                string_char = '"'

                # handle closing tags
                if not self.eos() and self.src[self.index] == "/":
                    token_typ = TokenType.Tag_Close
                    self.index += 1
                elif not self.eos() and self.src[self.index] == "!":
                    if not self.eos(1) and self.src[self.index + 1] != "-":
                        # deal with doctype
                        token_typ = TokenType.Doctype
                        self.index += 1
                    else:
                        if not self.eos(2) and self.src[self.index + 2] == "-": 
                            # this is a comment better skip it
                            self.index += 2
                            while not self.eos() and self.src[self.index] != ">":
                                self.index += 1
        
                            self.index += 1
        
                            # exit the tag parsing
                            continue

                while not self.eos() and self.src[self.index] != ">":
                    
                    while not self.eos() and self.src[self.index] not in [" ",">"]:
                        # handling string literals
                        if self.src[self.index] == '"' or self.src[self.index] == "'":
                            string_char = self.src[self.index]
                            self.index += 1
                            
                            text += string_char
                            while not self.eos() and self.src[self.index] != string_char:
                                text += self.src[self.index]
                                self.index += 1
                            # skip the '"' or "'"                            
                            self.index += 1
                            text += string_char

                            # skip the rest of the loop
                            continue
                        
                        text += self.src[self.index]
                        self.index += 1

                    # this is a prop
                    if not self.eos() and self.src[self.index] == " "  and tokenzied_tag:
                        self.tokens.append(Token(TokenType.Tag_Prop,text))
                        text = ""
                        self.index += 1

                    # save tag token and parse the props 
                    if not self.eos() and self.src[self.index] == " ":
                        if not tokenzied_tag:
                            self.tokens.append(Token(token_typ,text))
                            tokenzied_tag = True
                            self.index += 1
                            text = ""

                # there still a prop not saved, heppens when there is a '>'
                if text != "" and tokenzied_tag:
                    self.tokens.append(Token(TokenType.Tag_Prop,text))
                    text = ""

                # make sure u closed the tag
                assert self.src[self.index] == ">" and "[Assertion Failed] Tag Not Closed"
                self.index += 1
                
                # skip tag closing
                if not tokenzied_tag: self.tokens.append(Token(token_typ,text))
                                    
            elif ch in [" ","\n","\t"]: continue
            else:
                text = ch
                while not self.eos() and self.src[self.index] not in ["<"," ","\n","\t"] :
                    text += self.src[self.index]
                    self.index += 1
                
                self.tokens.append(Token(TokenType.Text,text))

        self.tokens.append(Token(TokenType.Eof))
        return self.tokens


