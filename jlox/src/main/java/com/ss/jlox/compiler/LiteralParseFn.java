package com.ss.jlox.compiler;

import com.ss.jlox.OpCode;

public class LiteralParseFn implements ParseFn {
    @Override
    public void apply(Compiler compiler, boolean canAssign) {
        Parser parser = compiler.getParser();
        switch (parser.getPrevious().getTokenType()) {
            case FALSE:
                compiler.emitByte(OpCode.OP_FALSE);
                break;
            case TRUE:
                compiler.emitByte(OpCode.OP_TRUE);
                break;
            case NIL:
                compiler.emitByte(OpCode.OP_NIL);
                break;
            default:
                return;
        }
    }
}
