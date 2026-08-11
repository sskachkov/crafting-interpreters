package com.ss.jlox;

import java.util.HashMap;
import java.util.Map;

public enum OpCode {
    //public final static byte OP_CONSTANT = 1, OP_RETURN = 2;
    OP_UNKNOWN, OP_POP, OP_GET_GLOBAL, OP_DEFINE_GLOBAL, OP_SET_GLOBAL, OP_CONSTANT, OP_NIL, OP_TRUE, OP_FALSE, OP_EQUAL, OP_GREATER, OP_LESS, OP_ADD, OP_SUBTRACT, OP_MULTIPLY, OP_DIVIDE, OP_NOT, OP_NEGATE, OP_PRINT, OP_RETURN;

    private static final Map<Integer,OpCode> opCodeByOrdinal;
    static {
        opCodeByOrdinal = new HashMap<>();
        for (OpCode opCode : OpCode.values()) {
            opCodeByOrdinal.put(opCode.ordinal(), opCode);
        }
    }
    public static OpCode byOrdinal(int ordinal) {
        OpCode opCode = opCodeByOrdinal.get(ordinal);
        return opCode != null ? opCode : OP_UNKNOWN;
    }
}
