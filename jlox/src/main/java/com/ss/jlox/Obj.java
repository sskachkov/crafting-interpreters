package com.ss.jlox;


public class Obj {
    private final ObjType type;

    public Obj(ObjType type) {
        this.type = type;
    }

    public ObjType getType() {
        return type;
    }

    public String toStr() {
        return type.name();
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Obj obj = (Obj) o;
        return type == obj.type;
    }

}

