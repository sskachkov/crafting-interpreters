package com.ss.jlox.compiler;

import com.ss.jlox.Token;

public class VariableParseFn implements ParseFn {
    @Override
    public void apply(Compiler compiler, boolean canAssign) {
        Parser parser = compiler.getParser();
        Token name = parser.getPrevious();
        compiler.namedVariable(name, canAssign);
    }
}
