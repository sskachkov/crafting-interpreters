package com.ss.jlox;

import com.ss.jlox.compiler.Compiler;

import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

public class VM {
    public enum InterpretResult {
        OK, COMPILE_ERROR, RUNTIME_ERROR
    }
    private Compiler compiler;
    private Chunk chunk;
    private Stack<Value> stack;
    private int ip;
    private Map<ObjString, Value> globals;

    public VM() {
        this.init();
    }
    public InterpretResult interpret(String source) {
        this.chunk = new Chunk();
        this.ip = 0;
        if (!compiler.compile(source, this.chunk)) {
            return InterpretResult.COMPILE_ERROR;
        }
        try {
            return run();
        } catch (RuntimeException r) {
            r.printStackTrace();
            System.out.println(r.getMessage());
            return InterpretResult.RUNTIME_ERROR;
        }
    }


    public InterpretResult interpret(Chunk chunk) {
        this.chunk = chunk;
        this.ip = 0;
        return run();
    }

    public void stackPush(Value value) {
        this.stack.push(value);
    }

    public Value stackPop() {
        return this.stack.pop();
    }

    public Value stackPeek() {
        return stackPeek(0);
    }

    public Value stackPeek(int depth) {
        int idx = this.stack.size() - 1 + depth;
        if (idx < 0) {
            throw new IllegalStateException("Stack is not deep enough to peek for " + depth + "th element.");
        }
        return this.stack.get(idx);
    }

    InterpretResult run() {
        for (;;) {
            int instruction = readByte();
            OpCode opCode = OpCode.byOrdinal(instruction);
            if (SystemPropertyUtils.getValueBool("debug.traceExecution")) {
                //System.out.print("            ");
                if (this.stack.size() > 0) {
                    for (Value value : this.stack) {
                        System.out.printf("[ %6.6s ] ", value.toStr());
                    }
                    System.out.println();
                }
                Debug.disassembleInstruction(this.chunk, this.ip - 1);
            }
            switch (opCode) {
                case OP_PRINT: {
                    System.out.println(stackPop().toStr());
                    break;
                }
                case OP_RETURN: {
                    return InterpretResult.OK;
                }
                case OP_NOT: {
                    stackPush(new Value(isFalsey(stackPop())));
                    break;
                }
                case OP_NEGATE: {
                    ensureStackHasNumberAt(0, "Negate operand must be a number");
                    Value neg = new Value(-stackPop().asNumber());
                    stackPush(neg);
                    break;
                }
                case OP_CONSTANT: {
                    Value constant = readConstant();
                    stackPush(constant);
                    break;
                }
                case OP_NIL:
                    stackPush(Value.NIL);
                    break;
                case OP_TRUE:
                    stackPush(Value.TRUE);
                    break;
                case OP_FALSE:
                    stackPush(Value.FALSE);
                    break;
                case OP_POP: {
                    stackPop();
                    break;
                }
                case OP_GET_GLOBAL: {
                    ObjString name = readString();
                    Value value = globals.get(name);
                    if (value == null) {
                        runtimeError("Undefined variable '%s'", name.getStr());
                        return InterpretResult.RUNTIME_ERROR;
                    }
                    stackPush(value);
                    break;
                }
                case OP_DEFINE_GLOBAL: {
                    ObjString name = readString();
                    Value value = stackPeek();
                    globals.put(name, value);
                    stackPop();
                    break;
                }
                case OP_SET_GLOBAL: {
                    ObjString name = readString();
                    if (globals.put(name, stackPeek()) == null) {
                        globals.remove(name);
                        runtimeError("Undefined variable '%s'.", name.toStr());
                        return InterpretResult.RUNTIME_ERROR;
                    }
                    break;
                }
                case OP_EQUAL: {
                    Value v1 = stackPop();
                    Value v2 = stackPop();
                    stackPush(new Value(v1.equals(v2)));
                    break;
                }
                case OP_GREATER: {
                    ensureStackHasNumberAt(0, "'Greater' operands must be numbers");
                    ensureStackHasNumberAt(-1, "'Greater' operands must be numbers");
                    double v2 = stackPop().asNumber();
                    double v1 = stackPop().asNumber();
                    stackPush(new Value(Double.compare(v1, v2) > 0));
                    break;
                } case OP_LESS: {
                    ensureStackHasNumberAt(0, "'Less' operands must be numbers");
                    ensureStackHasNumberAt(-1, "'Less' operands must be numbers");
                    double v2 = stackPop().asNumber();
                    double v1 = stackPop().asNumber();
                    stackPush(new Value(Double.compare(v1, v2) < 0));
                    break;
                }
                case OP_ADD: {
                    Value v2 = stackPeek(-1);
                    Value v1 = stackPeek(0);
                    if (v1.isObjType(ObjType.OBJ_STRING) && v2.isObjType(ObjType.OBJ_STRING)) {
                        String s2 = stackPop().asObject().toStr();
                        String s1 = stackPop().asObject().toStr();
                        stackPush(new Value(new ObjString(s1 + s2)));
                    } else if (v1.getValueType() == ValueType.NUMBER && v2.getValueType() == ValueType.NUMBER) {
                        double op2 = stackPop().asNumber();
                        double op1 = stackPop().asNumber();
                        stackPush(new Value(op1 + op2));
                    }
                    break;
                }
                case OP_SUBTRACT: {
                    ensureStackHasNumberAt(0, "Subtract operands must be numbers");
                    ensureStackHasNumberAt(-1, "Subtract operands must be numbers");
                    double op2 = stackPop().asNumber();
                    double op1 = stackPop().asNumber();
                    stackPush(new Value(op1 - op2));
                    break;
                }
                case OP_MULTIPLY: {
                    ensureStackHasNumberAt(0, "Multiply operands must be numbers");
                    ensureStackHasNumberAt(-1, "Multiply operands must be numbers");
                    double op2 = stackPop().asNumber();
                    double op1 = stackPop().asNumber();
                    stackPush(new Value(op1 * op2));
                    break;
                }
                case OP_DIVIDE: {
                    ensureStackHasNumberAt(0, "Divide operands must be numbers");
                    ensureStackHasNumberAt(-1, "Divide operands must be numbers");
                    double op2 = stackPop().asNumber();
                    double op1 = stackPop().asNumber();
                    stackPush(new Value(op1 / op2));
                    break;
                }
            }
        }
    }

    private boolean isFalsey(Value value) {
        return value.getValueType() == ValueType.NIL || (value.getValueType() == ValueType.BOOL && value.asBool());
    }

    private void ensureStackHasNumberAt(int index, String errorMessage) {
        Value value = stackPeek(index);
        if (value.getValueType() != ValueType.NUMBER) {
            runtimeError(errorMessage);
        }
    }

    private void runtimeError(String format, Object... args) {
        int offset = this.ip - 1;
        int lineNum = chunk.getLine(offset);
        System.err.print("[line " +  lineNum + "] in script: ");
        System.err.printf(format, args);
        System.err.println();
        resetStack();
        throw new RuntimeException();
    }

    private ObjString readString() {
        return (ObjString) readConstant().asObject();
    }
    private Value readConstant() {
        return chunk.getConstant(readByte());
    }
    private int readByte() {
        return chunk.getCode(this.ip++);
    }

    public void init() {
        resetStack();
        this.compiler = new Compiler();
        this.globals = new HashMap<>();
    }

    private void resetStack() {
        this.stack = new Stack<>();
    }

    public void free() {
        this.compiler = null;
        this.stack = null;
        this.globals = null;
        init();
    }

}
