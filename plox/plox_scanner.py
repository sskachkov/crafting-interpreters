from plox_data import *
# expression -> literal | unary | binary | grouping 
# literal -> NUMBER | STRING | "true" | "false" | "nil" 
# grouping -> "(" expression ")" 
# unary -> ( "-" | "!" ) expression
# binary -> expression operator expression
# operator -> "==" | "!=" | "<" | "<=" | ">" | ">=" | "+" | "-" | "*" | "/"
# 1 + / 3
class Scanner:
    def __init__(self, source : str, error_handler):
        self.source = source
        self.error_handler = error_handler

        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.keywords = {
            'and' : TokenType.AND, 
            'class' : TokenType.CLASS, 
            'else' : TokenType.ELSE, 
            'false' : TokenType.FALSE, 
            'for' : TokenType.FOR,
            'fun' : TokenType.FUN,
            'if' : TokenType.IF,
            'nil' : TokenType.NIL,
            'or' : TokenType.OR,
            'print' : TokenType.PRINT,
            'return' : TokenType.RETURN,
            'super' : TokenType.SUPER,
            'this' : TokenType.THIS,
            'true' : TokenType.TRUE, 
            'var' : TokenType.VAR,
            'while' : TokenType.WHILE}

    def __advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c

    def __add_token(self, token_type : TokenType, literal = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def __match(self, expected : str) -> bool:
        if self.__is_at_end():
            return False
        if self.source[self.current] == expected:
            self.current += 1
            return True
        return False

    def __peek(self) -> str:
        if self.__is_at_end():
            return '\0'
        else:
            return self.source[self.current]

    def __peekNext(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        else:
            return self.source[self.current + 1]

    def __scan_token(self):
        c = self.__advance()
        if c == '(':
            self.__add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.__add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.__add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.__add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.__add_token(TokenType.COMMA)
        elif c == '.':
            self.__add_token(TokenType.DOT)
        elif c == '-':
            self.__add_token(TokenType.MINUS)
        elif c == '+':
            self.__add_token(TokenType.PLUS)
        elif c == ';':
            self.__add_token(TokenType.SEMICOLON)
        elif c == '*':
            self.__add_token(TokenType.STAR)
        elif c == '!':
            if self.__match('='):
                self.__add_token(TokenType.BANG_EQUAL)
            else:
                self.__add_token(TokenType.BANG)
        elif c == '=':
            if self.__match('='):
                self.__add_token(TokenType.EQUAL_EQUAL)
            else:
                self.__add_token(TokenType.EQUAL)
        elif c == '>':
            if self.__match('='):
                self.__add_token(TokenType.GREATER_EQUAL)
            else:
                self.__add_token(TokenType.GREATER)
        elif c == '<':
            if self.__match('='):
                self.__add_token(TokenType.LESS_EQUAL)
            else:
                self.__add_token(TokenType.LESS)
        elif c == '/':
            if self.__match('/'):
                while not self.__is_at_end() and self.__peek() != '\n':
                    self.__advance()
            elif self.__match('*'):
                while self.__peek() != '*' or self.__peekNext() != '/':
                    if c == '\n':
                        self.line += 1
                    if not self.__is_at_end():
                        self.__advance()
                    else:
                        break
                if self.__is_at_end():
                    self.error_handler.error(self.line, "Scanner", "Unterminated multiline comment.")
                    return
                self.__advance()
                self.__advance()

            else:
                self.__add_token(TokenType.SLASH)
        elif c == ' ' or c == '\t' or c == '\r':
            pass
        elif c == '\n':
            self.line += 1
        elif c == '"':
            while not self.__is_at_end() and self.__peek() != '"':
                if self.__peek() == '\n':
                    self.line += 1
                self.__advance()
            if self.__is_at_end():
                self.error_handler.error(self.line, "Scanner", "Unterminated string.")
                return
            self.__advance() #closing quote

            val = self.source[self.start + 1: self.current - 1]
            self.__add_token(TokenType.STRING, val)
        elif c.isdigit():
            while self.__peek().isdigit():
                self.__advance()
            if self.__peek() == '.' and self.__peekNext().isdigit():
                self.__advance()
            while self.__peek().isdigit():
                self.__advance()
            self.__add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))
        elif c.isalpha():
            while self.__peek().isalnum():
                self.__advance()
            text = self.source[self.start:self.current]
            if text in self.keywords:
                self.__add_token(self.keywords[text])
            else:
                self.__add_token(TokenType.IDENTIFIER)
        else:
            self.error_handler.error(self.line, "Scanner", f"Unexpected character {c}.")
        

    
    def __is_at_end(self):
        return self.current >= len(self.source)

    def scan_tokens(self):
        while not self.__is_at_end():
            self.start = self.current
            self.__scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        #print(self.tokens)
        return self.tokens
