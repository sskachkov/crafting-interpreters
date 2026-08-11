package com.ss.jlox;

import java.util.ArrayList;
import java.util.List;

public class Chunk {
    private List<Integer> code;
    private List<Value> values;
    private List<Integer> lines;

    public Chunk() {
        init();
    }

    public void addCode(OpCode opCode, int line) {
        addCode(opCode.ordinal(), line);
    }

    public void addCode(int data, int line) {
        this.code.add(data);
        this.lines.add(line);
    }

    public int getCode(int offset) {
        return this.code.get(offset);
    }

    public int getLine(int offset) {
        return this.lines.get(offset);
    }

    public int addConstant(double number) {
        return addConstant(new Value(number));
    }

    public int addConstant(Value value) {
        this.values.add(value);
        return this.values.size() - 1;
    }

    public Value getConstant(int constantIndex) {
        return this.values.get(constantIndex);
    }


    public void clear() {
        this.code = null;
        this.values = null;
        this.lines = null;
        init();
    }

    private void init() {
        this.code = new ArrayList<>();
        this.values = new ArrayList<>();
        this.lines = new ArrayList<>();
    }

    public List<Integer> getCodeList() {
        return code;
    }
}
