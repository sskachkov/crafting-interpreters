package com.ss.jlox;

import java.io.PrintStream;
import java.util.List;

public class Debug {
    private static PrintStream out = System.out;
    public static void disassembleChunk(Chunk chunk, String name) {
        out.printf("== %s ==%n", name);
        List<Integer> code = chunk.getCodeList();
        for (int offset = 0; offset < code.size(); ) {
            offset = disassembleInstruction(chunk, offset);
        }
    }

    public static int disassembleInstruction(Chunk chunk, int offset) {
        out.printf("%04d ", offset);
        if (offset > 0 && chunk.getLine(offset) == chunk.getLine(offset - 1)) {
            out.print("    | ");
        } else {
            out.printf("%4d ", chunk.getLine(offset));
        }

        int instruction = chunk.getCode(offset);
        OpCode opCode = OpCode.byOrdinal(instruction);
        String opcodeLabel = opCode.name();
        switch (opCode) {
            case OP_RETURN:
            case OP_ADD:
            case OP_SUBTRACT:
            case OP_MULTIPLY:
            case OP_DIVIDE:
            case OP_NOT:
            case OP_NEGATE:
            case OP_NIL:
            case OP_TRUE:
            case OP_FALSE:
            case OP_LESS:
            case OP_GREATER:
            case OP_EQUAL:
            case OP_PRINT:
            case OP_POP:
                return simpleInstruction(opcodeLabel, offset);
            case OP_CONSTANT:
            case OP_GET_GLOBAL:
            case OP_DEFINE_GLOBAL:
            case OP_SET_GLOBAL:
                return constantInstruction(opcodeLabel, chunk, offset);
            default:
                out.println("Unknown opcode " + instruction);
                return offset + 1;
        }
    }

    private static int constantInstruction(String name, Chunk chunk, int offset) {
        int constant = chunk.getCode(offset + 1);
        Value value = chunk.getConstant(constant);
        out.printf(" %-16s %4d %s\n", name, constant, value.toStr());
        return offset + 2;
    }

    private static int simpleInstruction(String name, int offset) {
        out.println(" " + name);
        return offset + 1;
    }
}
