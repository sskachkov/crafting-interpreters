package com.ss.jlox.compiler;

import com.ss.jlox.Token;

public class Parser {
    private Token current;
    private Token previous;
    private boolean panicMode;
    private boolean hadError;

    public Token getCurrent() {
        return current;
    }

    public void setCurrent(Token current) {
        this.current = current;
    }

    public Token getPrevious() {
        return previous;
    }

    public void setPrevious(Token previous) {
        this.previous = previous;
    }

    public boolean isPanicMode() {
        return panicMode;
    }

    public void setPanicMode(boolean panicMode) {
        this.panicMode = panicMode;
    }

    public boolean isHadError() {
        return hadError;
    }

    public void setHadError(boolean hadError) {
        this.hadError = hadError;
    }
}
