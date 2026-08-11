package com.ss.jlox.compiler;

import com.ss.jlox.TokenType;

public class GroupingParseFn implements ParseFn {
    @Override
    public void apply(Compiler compiler, boolean canAssign) {
        compiler.expression();
        compiler.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.");
    }
}
