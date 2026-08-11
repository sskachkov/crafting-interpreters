package com.ss.jlox;

public class Value {
    public static Value NIL = new Value(ValueType.NIL, false, 0, null);
    public static Value TRUE = new Value(true);
    public static Value FALSE = new Value(false);
    private final ValueType valueType;
    private boolean bool;
    private double number;
    private Obj obj;

    Value(ValueType valueType, boolean bool, double number, Obj obj) {
        this.valueType = valueType;
        this.bool = bool;
        this.number = number;
        this.obj = obj;
    }

    public Value(boolean bool) {
        this.bool = bool;
        this.valueType = ValueType.BOOL;
    }

    public Value(double number) {
        this.number = number;
        this.valueType = ValueType.NUMBER;
    }

    public Value(Obj obj) {
        this.obj = obj;
        this.valueType = ValueType.OBJ;
    }

    public ValueType getValueType() {
        return valueType;
    }
    public boolean isObjType(ObjType type) {
        return valueType == ValueType.OBJ && obj.getType() == type;
    }

    public boolean asBool() {
        if (valueType != ValueType.BOOL) {
            throw new IllegalStateException("asBool called on " + valueType + " Value.");
        }
        return bool;
    }

    public double asNumber() {
        if (valueType != ValueType.NUMBER) {
            throw new IllegalStateException("asNumber called on " + valueType + " Value.");
        }
        return number;
    }

    public Obj asObject() {
        if (valueType != ValueType.OBJ) {
            throw new IllegalStateException("asObject called on " + valueType + " Value.");
        }
        return obj;
    }

    public String toStr() {
        switch (this.valueType) {
            case BOOL:
                return String.valueOf(this.asBool());
            case OBJ:
                return String.valueOf(this.asObject().toStr());
            case NUMBER:
                return String.valueOf(round(this.asNumber(), 3));
            case NIL:
                return "NIL";
            default:
                throw new IllegalStateException("Unexpected value type");
        }
    }

    public boolean equals(Object o2) {
        if (!(o2 instanceof Value)) {
            return false;
        }
        Value v2 = (Value) o2;

        if (this.getValueType() != v2.getValueType()) {
            return false;
        }
        switch (getValueType()) {
            case NIL:
                return true;
            case OBJ:
                return this.asObject().equals(v2.asObject());
            case BOOL:
                return this.asBool() == v2.asBool();
            case NUMBER:
                return this.asNumber() == v2.asNumber();
            default:
                return false;
        }
    }

    private double round(double number, int digits) {
        double pow = Math.pow(10, digits);
        return Math.round(number * pow) / pow;
    }
}
