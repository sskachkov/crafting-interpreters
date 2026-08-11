package com.ss.jlox;

public class Scanner {
    private String source;
    private int start;
    private int current;
    private int lineNum;

    public Scanner(String source, int current, int lineNum) {
        this.source = source;
        this.current = current;
        this.lineNum = lineNum;
    }
    public Token scanToken() {
        skipWhitespace();
        this.start = this.current;
        if (isAtTheEnd()) {
           return makeToken(TokenType.EOF);
        }
        char c = advance();
        if (isAlpha(c)) {
            return identifier();
        }
        if (isDigit(c)) {
            return number();
        }
        switch (c) {
            case '(':
                return makeToken(TokenType.LEFT_PAREN);
            case ')':
                return makeToken(TokenType.RIGHT_PAREN);
            case '{':
                return makeToken(TokenType.LEFT_BRACE);
            case '}':
                return makeToken(TokenType.RIGHT_BRACE);
            case ';':
                return makeToken(TokenType.SEMICOLON);
            case ',':
                return makeToken(TokenType.COMMA);
            case '.':
                return makeToken(TokenType.DOT);
            case '-':
                return makeToken(TokenType.MINUS);
            case '+':
                return makeToken(TokenType.PLUS);
            case '/':
                return makeToken(TokenType.SLASH);
            case '*':
                return makeToken(TokenType.STAR);
            case '!':
                return (match('=') ? makeToken(TokenType.BANG_EQUAL) : makeToken(TokenType.BANG));
            case '=':
                return (match('=') ? makeToken(TokenType.EQUAL_EQUAL) : makeToken(TokenType.EQUAL));
            case '<':
                return (match('=') ? makeToken(TokenType.LESS_EQUAL) : makeToken(TokenType.LESS));
            case '>':
                return (match('=') ? makeToken(TokenType.GREATER_EQUAL) : makeToken(TokenType.GREATER));
            case '"':
                return string();

        }
        return errorToken("Unexpected character.");
    }
    private Token string() {
        while (peek() != '"' && !isAtTheEnd()) {
            if (peek() == '\n') {
                this.lineNum++;
            }
            advance();
        }
        if (isAtTheEnd()) {
            return errorToken("Unterminated string.");
        }
        advance();//consume closing quote
        return makeToken(TokenType.STRING);
    }

    private Token number() {
        while (isDigit(peek())) {
            advance();
        }
        if (peek() == '.' && isDigit(peekNext())) {
            advance();
            while(isDigit(peek())) {
                advance();
            }
        }

        return makeToken(TokenType.NUMBER);
    }

    private Token identifier() {
        while (isAlpha(peek()) || isDigit(peek())) {
            advance();
        }
        return makeToken(identifierType());
    }

    private TokenType identifierType() {
        switch (this.source.charAt(this.start)) {
            case 'a':
                return checkKeyword(1, "nd", TokenType.AND);
            case 'c':
                return checkKeyword(1, "lass", TokenType.CLASS);
            case 'e':
                return checkKeyword(1, "lse", TokenType.ELSE);
            case 'f':
                if (this.current - this.start > 1) {
                    switch (this.source.charAt(this.start + 1)) {
                        case 'a':
                            return checkKeyword(2, "lse", TokenType.FALSE);
                        case 'o':
                            return checkKeyword(2, "r", TokenType.FOR);
                        case 'u':
                            return checkKeyword(2, "n", TokenType.FUN);
                    }
                }
                break;
            case 'i':
                return checkKeyword(1, "f", TokenType.IF);
            case 'n':
                return checkKeyword(1, "il", TokenType.NIL);
            case 'o':
                return checkKeyword(1, "r", TokenType.OR);
            case 'p':
                return checkKeyword(1, "rint", TokenType.PRINT);
            case 'r':
                return checkKeyword(1, "eturn", TokenType.RETURN);
            case 's':
                return checkKeyword(1, "uper", TokenType.SUPER);
            case 't':
                if (this.current - this.start > 1) {
                    switch (this.source.charAt(this.start + 1)) {
                        case 'h':
                            return checkKeyword(2, "is", TokenType.THIS);
                        case 'r':
                            return checkKeyword(2, "ue", TokenType.TRUE);
                    }
                }
                break;
            case 'v':
                return checkKeyword(1, "ar", TokenType.VAR);
            case 'w':
                return checkKeyword(1, "hile", TokenType.WHILE);

        }
        return TokenType.IDENTIFIER;
    }

    private TokenType checkKeyword(int start, String rest, TokenType type) {
        int length = rest.length();
        if (this.current - this.start == start + length) {
            for (int i = start; i < start + length; i++) {
                if (this.source.charAt(i + this.start) != rest.charAt(i - start)) {
                    return TokenType.IDENTIFIER;
                }
            }
        } else {
            return TokenType.IDENTIFIER;
        }
        return type;
    }

    private boolean isDigit(char c) {
        return c >= '0' && c <= '9';
    }

    private boolean isAlpha(char c) {
        return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
    }

    private Token makeToken(TokenType tokenType) {
        return new Token(tokenType, source.substring(this.start, this.current), this.lineNum);
    }

    private Token errorToken(String errorMsg) {
        return new Token(TokenType.ERROR, errorMsg, this.lineNum);
    }


    private void skipWhitespace() {
        for(;;) {
            char c = peek();
            switch (c) {
                case ' ':
                case '\t':
                case '\r':
                    advance();
                    break;
                case '\n':
                    advance();
                    this.lineNum++;
                    break;
                case '/':
                    if (peekNext() == '/') {
                        while (peek() != '\n' && !isAtTheEnd()) {
                            advance();
                        }
                    } else {
                        return;
                    }
                    break;
                default:
                    return;
            }
        }
    }

    private char peek() {
        return isAtTheEnd() ? '\0' : this.source.charAt(this.current);
    }
    private char peekNext() {
        if (isAtTheEnd()) {
            return '\0';
        }
        return this.source.charAt(this.current + 1);
    }
    private char advance() {
        this.current++;
        return this.source.charAt(current - 1);
    }

    private boolean match(char expected) {
        if (isAtTheEnd()) {
            return false;
        }
        boolean result = this.source.charAt(this.current) == expected;
        if (result) {
            this.current++;
        }
        return result;

    }

    private boolean isAtTheEnd() {
        return this.current >= this.source.length();
    }
}
