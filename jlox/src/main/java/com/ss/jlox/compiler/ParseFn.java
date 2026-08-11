package com.ss.jlox.compiler;

public interface ParseFn {
    void apply(Compiler compiler, boolean canAssign);
}
