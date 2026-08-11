package com.ss.jlox;

public class Token {
    private final TokenType tokenType;
    private final String str;
    private final int line;

    public Token(TokenType tokenType, String str, int line) {
        this.tokenType = tokenType;
        this.str = str;
        this.line = line;
    }

    public TokenType getTokenType() {
        return tokenType;
    }

    public String getStr() {
        return str;
    }

    public int getLine() {
        return line;
    }

    @Override
    public String toString() {
        return "Token{" +
                "tokenType=" + tokenType +
                ", str='" + str + '\'' +
                ", line=" + line +
                '}';
    }
}
