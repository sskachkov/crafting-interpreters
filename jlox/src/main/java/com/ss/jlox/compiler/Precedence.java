package com.ss.jlox.compiler;

public enum Precedence {
    NONE,
    ASSIGNMENT, // =
    OR, // or
    AND, // and
    EQUALITY, // == !=
    COMPARISON, // < > <= >=
    TERM, // + -
    FACTOR, // * /
    UNARY, // ! -
    CALL, // . ()
    PRIMARY;

    private static final Precedence[] ARR = Precedence.values();

    public static Precedence next(Precedence precedence) {
        return ARR[precedence.ordinal() + 1];
    }
}
