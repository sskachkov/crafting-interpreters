package com.ss.jlox.compiler;

import com.ss.jlox.ObjString;
import com.ss.jlox.Value;

public class StringParseFn implements ParseFn {
    @Override
    public void apply(Compiler compiler, boolean canAssign) {
        Parser parser = compiler.getParser();
        String tokenStr = parser.getPrevious().getStr();
        compiler.emitConstant(new Value(new ObjString(tokenStr.substring(1, tokenStr.length() - 1))));
    }
}
