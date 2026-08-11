package com.ss;

import com.ss.jlox.*;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

public class BasicVMTest {

    @BeforeAll
    public static void setup() {
        System.setProperty("debug.traceExecution", "true");
        System.setProperty("debug.printCode", "true");
    }

    //@Test
    public void t1estSimpleAdd() {
        Chunk chunk = new Chunk();
        VM vm = new VM();
        chunk.addCode(OpCode.OP_CONSTANT, 1);
        chunk.addCode(chunk.addConstant(4), 1);
        chunk.addCode(OpCode.OP_CONSTANT, 2);
        chunk.addCode(chunk.addConstant(3), 2);
        chunk.addCode(OpCode.OP_ADD, 3);
        chunk.addCode(OpCode.OP_RETURN, 4);

        vm.interpret(chunk);
        Value result = vm.stackPeek();

        Assertions.assertSame(result.getValueType(), ValueType.NUMBER);
        Assertions.assertEquals(result.asNumber(), 7.0);
    }

    //@Test
    public void t1estMultiExpr1() {
        //1 * 2 + 3
        Chunk chunk = new Chunk();
        VM vm = new VM();
        chunk.addCode(OpCode.OP_CONSTANT, 1);
        chunk.addCode(chunk.addConstant(1), 1);

        chunk.addCode(OpCode.OP_CONSTANT, 2);
        chunk.addCode(chunk.addConstant(2), 2);

        chunk.addCode(OpCode.OP_MULTIPLY, 3);

        chunk.addCode(OpCode.OP_CONSTANT, 4);
        chunk.addCode(chunk.addConstant(3), 4);

        chunk.addCode(OpCode.OP_ADD, 5);

        chunk.addCode(OpCode.OP_RETURN, 6);
        vm.interpret(chunk);

        Value result = vm.stackPeek();
        Assertions.assertSame(result.getValueType(), ValueType.NUMBER);
        Assertions.assertEquals(result.asNumber(), 5.0);
    }

    //@Test
    public void t1estMultiExpr2() {
        //5 - 2 - 1
        Chunk chunk = new Chunk();
        VM vm = new VM();
        chunk.addCode(OpCode.OP_CONSTANT, 1);
        chunk.addCode(chunk.addConstant(5), 1);

        chunk.addCode(OpCode.OP_CONSTANT, 2);
        chunk.addCode(chunk.addConstant(2), 2);

        chunk.addCode(OpCode.OP_SUBTRACT, 3);

        chunk.addCode(OpCode.OP_CONSTANT, 4);
        chunk.addCode(chunk.addConstant(1), 4);

        chunk.addCode(OpCode.OP_SUBTRACT, 5);

        chunk.addCode(OpCode.OP_RETURN, 6);
        vm.interpret(chunk);

        Value result = vm.stackPeek();
        Assertions.assertSame(result.getValueType(), ValueType.NUMBER);
        Assertions.assertEquals(result.asNumber(), 2.0);
    }

}
