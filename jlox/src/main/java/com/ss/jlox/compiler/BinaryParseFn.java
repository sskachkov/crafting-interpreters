package com.ss.jlox.compiler;

import com.ss.jlox.OpCode;
import com.ss.jlox.TokenType;

public class BinaryParseFn implements ParseFn {
    @Override
    public void apply(Compiler compiler, boolean canAssign) {
        Parser parser = compiler.getParser();
        TokenType operatorType = parser.getPrevious().getTokenType();
        ParseRule rule = compiler.getRule(operatorType);
        compiler.parsePrecedence(Precedence.next(rule.precedence));
        switch (operatorType) {
            case BANG_EQUAL:
                compiler.emitBytes(OpCode.OP_EQUAL, OpCode.OP_NOT);
                break;
            case EQUAL_EQUAL:
                compiler.emitByte(OpCode.OP_EQUAL);
                break;
            case GREATER:
                compiler.emitByte(OpCode.OP_GREATER);
                break;
            case GREATER_EQUAL:
                compiler.emitBytes(OpCode.OP_LESS, OpCode.OP_NOT);
                break;
            case LESS:
                compiler.emitByte(OpCode.OP_LESS);
                break;
            case LESS_EQUAL:
                compiler.emitBytes(OpCode.OP_GREATER, OpCode.OP_NOT);
                break;
            case PLUS:
                compiler.emitByte(OpCode.OP_ADD);
                break;
            case MINUS:
                compiler.emitByte(OpCode.OP_SUBTRACT);
                break;
            case STAR:
                compiler.emitByte(OpCode.OP_MULTIPLY);
                break;
            case SLASH:
                compiler.emitByte(OpCode.OP_DIVIDE);
                break;
            default:
                return;
        }
    }
}
