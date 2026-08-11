package com.ss.jlox.compiler;

import com.ss.jlox.OpCode;
import com.ss.jlox.TokenType;

public class UnaryParseFn implements ParseFn {

    @Override
    public void apply(Compiler compiler, boolean canAssign) {
        Parser parser = compiler.getParser();
        TokenType operatorType = parser.getPrevious().getTokenType();
        compiler.parsePrecedence(Precedence.UNARY);
        switch (operatorType) {
            case BANG:
                compiler.emitByte(OpCode.OP_NOT);
                break;
            case MINUS:
                compiler.emitByte(OpCode.OP_NEGATE);
                break;
            default:
                break;
        }
    }
}
