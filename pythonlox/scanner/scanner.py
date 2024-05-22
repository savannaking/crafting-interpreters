from scanner.tokentype import TokenType
from scanner.token import Token


class Scanner:
    def __init__(self, source: str):
        self.src = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []
        self.keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }

    def scanTokens(self):
        while self.current < len(self.src):
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scanToken(self):
        c = self.src[self.current]
        match c:
            case "(":
                self.addToken(TokenType.LEFT_PAREN)
                return
            case ")":
                self.addToken(TokenType.RIGHT_PAREN)
                return
            case "{":
                self.addToken(TokenType.LEFT_BRACE)
                return
            case "}":
                self.addToken(TokenType.RIGHT_BRACE)
                return
            case ",":
                self.addToken(TokenType.COMMA)
                return
            case ".":
                self.addToken(TokenType.DOT)
                return
            case "-":
                self.addToken(TokenType.MINUS)
                return
            case "+":
                self.addToken(TokenType.PLUS)
                return
            case ";":
                self.addToken(TokenType.SEMICOLON)
                return
            case "*":
                self.addToken(TokenType.STAR)
                return
            case "!":
                self.addToken(
                    TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                )
                return
            case "=":
                self.addToken(
                    TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                )
                return
            case "<":
                self.addToken(
                    TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                )
                return
            case ">":
                self.addToken(
                    TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                )
                return
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and self.isAtEnd() is False:
                        self.advance()
                else:
                    self.addToken(TokenType.SLASH)
                return
            case " ":
                return
            case "\r":
                return
            case "\t":
                return
            case "\n":
                self.line = self.line + 1
                return
            case '"':
                self.string()
                return

            case _:
                if c.isnumeric():
                    self.number()
                elif c.isalpha():
                    self.identifier()
                else:
                    raise Exception(f"Unexpected character on line ${self.line}")

    def identifier(self):
        while self.peek().isalpha() or self.peek().isnumeric():
            self.advance()

        text = self.src[self.start : self.current + 1]
        type = self.keywords.get(text)
        if type is None:
            type = TokenType.IDENTIFIER

        self.addToken(type)

    def number(self):
        while self.peek().isnumeric():
            self.advance()

        if self.peek() == "." and self.peekNext().isdigit():
            self.advance()

            while self.peek().isdigit():
                self.advance()

        self.addToken(TokenType.NUMBER, float(self.src[self.start : self.current + 1]))

    def string(self):
        while self.peek() != '"' and self.isAtEnd() is False:
            if self.peek() == "\n":
                self.line = self.line + 1
            self.advance()
        if self.isAtEnd():
            raise Exception(f"Unterminated string on line ${self.line}")

        self.advance()

        value = self.src[self.start + 1 : self.current - 1]
        self.addToken(TokenType.STRING, value)

    def match(self, expected):
        if self.current + 1 >= len(self.src):
            return False
        if self.src[self.current] != expected:
            return False

        self.advance()
        return True

    def addToken(self, type, literal=None):
        text = self.src[self.start : self.current + 1]
        self.tokens.append(Token(type, text, literal, self.line))
        self.current = self.current + 1

    def advance(self):
        self.current = self.current + 1
        return self.src[self.current]

    def peek(self):
        if self.isAtEnd() == True:
            return "\0"
        else:
            return self.src[self.current + 1]

    def peekNext(self):
        if (self.current + 1) >= len(self.src):
            return "\0"
        return self.src[self.current]

    def isAtEnd(self):
        return self.current + 1 >= len(self.src)
