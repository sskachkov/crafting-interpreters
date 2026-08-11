package com.ss.jlox.compiler;

import com.ss.jlox.*;

import java.util.HashMap;
import java.util.Map;

public class Compiler {
    private Scanner scanner;
    private Parser parser;
    private Chunk chunk;

    public boolean compile(String source, Chunk chunk) {
        this.parser = new Parser();
        this.chunk = chunk;
        initScanner(source);
        advance();

        //expression();
        while (!match(TokenType.EOF)) {
            declaration();
        }

        endCompiler();
        return !parser.isHadError();
    }

    void expression() {
        parsePrecedence(Precedence.ASSIGNMENT);
        //consume(TokenType.SEMICOLON, "Expect semicolon");
    }

    private void declaration() {
        if (match(TokenType.VAR)) {
            varDeclaration();
        } else {
            statement();
        }

        if (parser.isPanicMode()) {
            synchronize();
        }
    }

    private void varDeclaration() {
        int global = parseVariable("Expect variable name.");
        if (match(TokenType.EQUAL)) {
            expression();
        } else {
            emitByte(OpCode.OP_NIL);
        }
        consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.");
        defineVariable(global);
    }

    private void defineVariable(int global) {
        emitBytes(OpCode.OP_DEFINE_GLOBAL, global);
    }

    int parseVariable(String errMsg) {
        consume(TokenType.IDENTIFIER, errMsg);
        return identifierConstant(parser.getPrevious());
    }

    int identifierConstant(Token name) {
        return makeConstant(new Value(new ObjString(name.getStr())));
    }

    void namedVariable(Token name, boolean canAssign) {
        int constant = identifierConstant(name);
        if (canAssign && match(TokenType.EQUAL)) {
            expression();
            emitBytes(OpCode.OP_SET_GLOBAL, constant);
        } else {
            emitBytes(OpCode.OP_GET_GLOBAL, constant);
        }
    }

    private void synchronize() {
        parser.setPanicMode(false);
        while (parser.getCurrent().getTokenType() != TokenType.EOF) {
            if (parser.getPrevious().getTokenType() == TokenType.SEMICOLON) {
                return;
            }
            switch (parser.getCurrent().getTokenType()) {
                case CLASS:
                case FUN:
                case VAR:
                case FOR:
                case IF:
                case WHILE:
                case PRINT:
                case RETURN:
                    return;
                default:
                    break;
            }
            advance();
        }
    }

    private void statement() {
        if (match(TokenType.PRINT)) {
            printStatement();
        } else {
            expressionStatement();
        }
    }

    private void printStatement() {
        expression();
        consume(TokenType.SEMICOLON, "Expect ';' after value.");
        emitByte(OpCode.OP_PRINT);
    }

    private void expressionStatement() {
        expression();
        consume(TokenType.SEMICOLON, "Expect ';' after expression.");
        emitByte(OpCode.OP_POP);
    }

    private boolean match(TokenType tt) {
        if (!check(tt)) {
            return false;
        }
        advance();
        return true;
    }

    private boolean check(TokenType tt) {
        return parser.getCurrent().getTokenType() == tt;
    }

    private void advance() {
        parser.setPrevious(parser.getCurrent());
        for (; ; ) {
            parser.setCurrent(scanner.scanToken());
            if (parser.getCurrent().getTokenType() != TokenType.ERROR) {
                break;
            }
            errorAtCurrent(parser.getCurrent().getStr());
        }
    }

    void consume(TokenType tokenType, String errorMsg) {
        if (parser.getCurrent().getTokenType() == tokenType) {
            advance();
            return;
        }
        errorAtCurrent(errorMsg);
    }

    void parsePrecedence(Precedence precedence) {
        advance();
        ParseFn prefixRule = getRule(parser.getPrevious().getTokenType()).prefix;
        if (prefixRule == null) {
            error("Expect expression.");
            return;
        }
        boolean canAssign = precedence.ordinal() <= Precedence.ASSIGNMENT.ordinal();
        prefixRule.apply(this, canAssign);
        while (precedence.ordinal() <= getRule(parser.getCurrent().getTokenType()).precedence.ordinal()) {
            advance();
            ParseFn infix = getRule(parser.getPrevious().getTokenType()).infix;
            infix.apply(this, canAssign);
        }
        if (canAssign && match(TokenType.EQUAL)) {
            error("Invalid assignment target");
        }
    }

    void emitConstant(Value v) {
        emitBytes(OpCode.OP_CONSTANT, makeConstant(v));
    }

    int makeConstant(Value v) {
        return chunk.addConstant(v);
    }

    void emitBytes(OpCode opCode, int byte2) {
        emitByte(opCode);
        emitByte(byte2);
    }
    void emitBytes(OpCode opCode1, OpCode opCode2) {
        emitByte(opCode1);
        emitByte(opCode2);
    }

    void emitBytes(int byte1, int byte2) {
        emitByte(byte1);
        emitByte(byte2);
    }

    void emitByte(OpCode opcode) {
        emitByte(opcode.ordinal());
    }

    void emitByte(int data) {
        chunk.addCode(data, parser.getPrevious().getLine());
    }

    void emitReturn() {
        emitByte(OpCode.OP_RETURN);
    }

    void endCompiler() {
        emitReturn();
        if (SystemPropertyUtils.getValueBool("debug.printCode")) {
            if (!parser.isHadError()) {
                Debug.disassembleChunk(chunk, "code");
                System.out.println("Compilation finished.");
            }
        }
    }

    private void errorAtCurrent(String errorMsg) {
        errorAt(parser.getCurrent(), errorMsg);
    }

    private void error(String errorMsg) {
        errorAt(parser.getPrevious(), errorMsg);
    }

    private void errorAt(Token token, String errorMsg) {
        if (parser.isPanicMode()) {
            return;
        } else {
            parser.setPanicMode(true);
        }

        System.err.print("[Line " + token.getLine() + "] Compiler error");
        if (token.getTokenType() == TokenType.EOF) {
            System.err.print(" at end");
        } else if (token.getTokenType() == TokenType.ERROR) {
            //nothing
        } else {
            System.err.print(" at '" + token.getStr() + "'");
        }
        System.err.println(": " + errorMsg);
    }

    void initScanner(String source) {
        scanner = new Scanner(source, 0, 1);
    }
    public ParseRule getRule(TokenType tokenType) {
        return parseRules.get(tokenType);
    }

    public Parser getParser() {
        return parser;
    }

    private static Map<TokenType, ParseRule> parseRules = new HashMap<>();
    static {
        parseRules.put(TokenType.LEFT_PAREN,    new ParseRule(new GroupingParseFn(),    null,                   Precedence.NONE));
        parseRules.put(TokenType.RIGHT_PAREN,   new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.LEFT_BRACE,    new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.RIGHT_BRACE,   new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.COMMA,         new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.DOT,           new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.MINUS,         new ParseRule(new UnaryParseFn(),       new BinaryParseFn(),    Precedence.TERM));
        parseRules.put(TokenType.PLUS,          new ParseRule(null,                     new BinaryParseFn(),    Precedence.TERM));
        parseRules.put(TokenType.SEMICOLON,     new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.SLASH,         new ParseRule(null,                     new BinaryParseFn(),    Precedence.FACTOR));
        parseRules.put(TokenType.STAR,          new ParseRule(null,                     new BinaryParseFn(),    Precedence.FACTOR));
        parseRules.put(TokenType.BANG,          new ParseRule(new UnaryParseFn(),       null,                   Precedence.NONE));
        parseRules.put(TokenType.BANG_EQUAL,    new ParseRule(null,                     new BinaryParseFn(),    Precedence.EQUALITY));
        parseRules.put(TokenType.EQUAL,         new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.EQUAL_EQUAL,   new ParseRule(null,                     new BinaryParseFn(),    Precedence.EQUALITY));
        parseRules.put(TokenType.GREATER,       new ParseRule(null,                     new BinaryParseFn(),    Precedence.COMPARISON));
        parseRules.put(TokenType.GREATER_EQUAL, new ParseRule(null,                     new BinaryParseFn(),    Precedence.COMPARISON));
        parseRules.put(TokenType.LESS,          new ParseRule(null,                     new BinaryParseFn(),    Precedence.COMPARISON));
        parseRules.put(TokenType.LESS_EQUAL,    new ParseRule(null,                     new BinaryParseFn(),    Precedence.COMPARISON));
        parseRules.put(TokenType.IDENTIFIER,    new ParseRule(new VariableParseFn(),    null,                   Precedence.NONE));
        parseRules.put(TokenType.STRING,        new ParseRule(new StringParseFn(),      null,                   Precedence.NONE));
        parseRules.put(TokenType.NUMBER,        new ParseRule(new NumberParseFn(),      null,                   Precedence.NONE));
        parseRules.put(TokenType.AND,           new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.CLASS,         new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.ELSE,          new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.FALSE,         new ParseRule(new LiteralParseFn(),     null,                   Precedence.NONE));
        parseRules.put(TokenType.FOR,           new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.FUN,           new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.IF,            new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.NIL,           new ParseRule(new LiteralParseFn(),     null,                   Precedence.NONE));
        parseRules.put(TokenType.OR,            new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.PRINT,         new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.RETURN,        new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.SUPER,         new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.THIS,          new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.TRUE,          new ParseRule(new LiteralParseFn(),     null,                   Precedence.NONE));
        parseRules.put(TokenType.VAR,           new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.WHILE,         new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.ERROR,         new ParseRule(null,                     null,                   Precedence.NONE));
        parseRules.put(TokenType.EOF,           new ParseRule(null,                     null,                   Precedence.NONE));


    }
}
