package com.ss.jlox.compiler;

import com.ss.jlox.Value;

public class NumberParseFn implements ParseFn {

    @Override
    public void apply(Compiler compiler, boolean canAssign) {
        Parser parser = compiler.getParser();
        double v = Double.parseDouble(parser.getPrevious().getStr());
        compiler.emitConstant(new Value(v));
    }

}
