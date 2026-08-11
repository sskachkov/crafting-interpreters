package com.ss.jlox;

import java.util.Objects;

public class ObjString extends Obj {
    public static ObjString copyString(String str) {
        return new ObjString(str);
    }
    private final String str;

    public ObjString(String str) {
        super(ObjType.OBJ_STRING);
        this.str = str;
    }

    public String getStr() {
        return str;
    }

    @Override
    public String toStr() {
        return str;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        if (!super.equals(o)) return false;
        ObjString objString = (ObjString) o;
        return Objects.equals(str, objString.str);
    }

    @Override
    public int hashCode() {
        return Objects.hash(str);
    }
}
