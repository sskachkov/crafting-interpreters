package com.ss.jlox.compiler;

public class ParseRule {
    public ParseRule(ParseFn prefix, ParseFn infix, Precedence precedence) {
        this.prefix = prefix;
        this.infix = infix;
        this.precedence = precedence;
    }

    ParseFn prefix;
    ParseFn infix;
    Precedence precedence;
}
