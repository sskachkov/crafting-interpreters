from plox_error import ErrorHandler, ParserException, PloxError, PloxException
from plox_data import *

# program -> declaration* EOF;
# declaration -> classDecl | funDecl | varDecl | statement
# classDecl -> "class" IDENTIFIER "{" function* "}"
# funDecl -> "fun" function
# function -> IDENTIFIER "(" parameters? ")" block
# parameters -> IDENTIFIER ("," IDENTIFIER)*
# varDecl -> "var" IDENTIFIER ("=" expression)? ";"
# statement -> exprStmt | ifStmt | forStmt | printStmt | returnStmt | whileStmt | blockStmt
# exprStmt -> expression ";"
# ifStmt -> "if" "(" expression ")" statement ("else" statement)?
# forStmt -> "for" "(" (varDecl | exprStmt | ";") expression? ";" expression? ")" statement
# printStmt -> "print" expression ";"
# returnStmt -> "return" expression? ";"
# whileStmt -> "while" "(" expression ")" statement
# blockStmt -> "{" declaration* "}"
#
# expression -> assignment
# assignment -> (call ".")? IDENTIFIER "=" assignment | logic_or
# logic_or -> logic_and ("or" logic_and)*
# logic_and -> equality ("and" equality)*
# equality -> comparison ( ("!=" | "==") comparison )*
# comparison -> term ( (">" | ">=" | "<" | "<=") term)*
# term -> factor ( ("-" | "+") factor )*
# factor -> unary ( ("/" | "*") unary)*
# unary -> ( ("!"| "-") unary) | call
# call -> primary ("(" arguments? ")" | "." IDENTIFIER)*
# arguments -> expression ("," expression)*
# primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" | IDENTIFIER | "super" "." IDENTIFIER
class Parser:
    def __init__(self, tokens, error_handler: ErrorHandler) -> None:
        self.error_handler = error_handler
        self.tokens = tokens
        self.current = 0
    
    def parse(self) -> list [Stmt]:
        stmts = []
        while not self._is_at_end():
            decl = self._declaration()
            if decl != None:
                stmts.append(decl)
        #print(stmts)
        return stmts

    def _declaration(self) -> Stmt:
        try:
            if self._match(TokenType.CLASS):
                return self._class_decl()
            if self._match(TokenType.VAR):
                return self._var_decl()
            elif self._match(TokenType.FUN):
                return self._fun_decl("function")
            else:
                return self._statement()
        except PloxException as err:
            self.error_handler.exception(err)
            self._advance()
            return None
    
    def _class_decl(self) :
        name = self._consume(TokenType.IDENTIFIER, "Expect class name.")
        supercl = None
        if self._match(TokenType.LESS):
            supercl = VarExpr(self._consume(TokenType.IDENTIFIER, "Expect superclass name."), name.line)
        self._consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")
        methods = []
        while not self._check(TokenType.RIGHT_BRACE):
            methods.append(self._fun_decl("method"))
        self._consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")
        return ClassDeclStmt(name, supercl, methods, name.line)
        
    def _fun_decl(self, kind : str):
        name = self._consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self._consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters = []
        if not self._check(TokenType.RIGHT_PAREN):
            parameters.append(self._consume(TokenType.IDENTIFIER, "Expect parameter name."))
        while self._match(TokenType.COMMA):
            if len(parameters) > 255:
                self._error(self._peek(), "Can't have more than 255 parameters.")
            parameters.append(self._consume(TokenType.IDENTIFIER, "Expect parameter name."))
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        self._consume(TokenType.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        body = self._block()
        return FunDeclStmt(name, parameters, body, name.line)

    def _var_decl(self):
        name = self._consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if (self._match(TokenType.EQUAL)):
            initializer = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return VarDeclStmt(name, initializer, name.line)

    def _statement(self):
        if self._match(TokenType.PRINT):
            return self._print_statement()
        elif self._match(TokenType.RETURN):
            return self._return_statement()
        elif self._match(TokenType.LEFT_BRACE):
            return self._block_statement()
        elif self._match(TokenType.IF):
            return self._if_statement()
        elif self._match(TokenType.WHILE):
            return self._while_statement()
        elif self._match(TokenType.FOR):
            return self._for_statement()
        else:
            return self._expr_statement()

    def _return_statement(self):
        keyword = self._previous()
        value = None
        if not self._check(TokenType.SEMICOLON):
            value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return ReturnStmt(value, keyword.line)
    
    def _for_statement(self):
        line = self._previous().line
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        initializer = None
        if self._match(TokenType.SEMICOLON):
            initializer = None
        elif self._match(TokenType.VAR):
            initializer = self._var_decl()
        else:
            initializer = self._expr_statement()
        
        condition = None
        if not self._check(TokenType.SEMICOLON):
            condition = self._expression()

        self._consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self._check(TokenType.RIGHT_PAREN):
            increment = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after for clause.")
        body = self._statement()

        return ForStmt(initializer, condition, increment, body, line)


    def _if_statement(self):
        line = self._previous().line
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after if.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
        then_branch = self._statement()
        else_branch = None
        if self._match(TokenType.ELSE):
            else_branch = self._statement()
        return IfStmt(condition, then_branch, else_branch, line)

    def _print_statement(self):
        line = self._previous().line
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return PrintStmt(expr, line)

    def _while_statement(self):
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after while.")
        expr = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after while condition.")
        body = self._statement()
        return WhileStmt(expr, body, expr.line)
    
    def _block_statement(self) -> BlockStmt:
        line = self._previous().line
        return BlockStmt(self._block(), line)

    def _block(self) -> list [Stmt]:
        stmts = []
        while not self._is_at_end() and not self._check(TokenType.RIGHT_BRACE):
            stmts.append(self._declaration())
        self._consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return stmts

    def _expr_statement(self):
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return ExpressionStmt(expr, expr.line)

    def _expression(self) -> Expr:
        return self._assignment()
    
    def _assignment(self) -> Expr:
        expr = self._or()
        if self._match(TokenType.EQUAL):
            value = self._assignment()
            if type(expr) == VarExpr:
                return AssignExpr(expr.name, value, expr.line)
            elif type(expr) == GetExpr:
                return SetExpr(expr.object, expr.name, value, expr.line)
            else:
                raise ParserException(f"Invalid assignment target [{type(expr).__name__}].", expr)
        else:
            return expr
    
    def _or(self) -> Expr: 
        expr = self._and()
        while self._match(TokenType.OR):
            op = self._previous()
            right = self._and()
            expr = LogicalExpr(expr, op, right, expr.line)
        return expr
    
    def _and(self) -> Expr:
        expr = self._equality()
        while self._match(TokenType.AND):
            op = self._previous()
            right = self._equality()
            expr = LogicalExpr(expr, op, right, expr.line)
        return expr
    
    def _equality(self) -> Expr:
        expr = self._comparison()
        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            op = self._previous()
            right = self._comparison()
            expr = BinaryExpr(expr, op, right, expr.line)
        return expr

    def _comparison(self):
        expr = self._term()
        while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            op = self._previous()
            right = self._term()
            expr = BinaryExpr(expr, op, right, expr.line)
        return expr

    def _term(self):
        expr = self._factor()
        while self._match(TokenType.MINUS, TokenType.PLUS):
            op = self._previous()
            right = self._factor()
            expr = BinaryExpr(expr, op, right, expr.line)
        return expr
        
    def _factor(self):
        expr = self._unary()
        while self._match(TokenType.SLASH, TokenType.STAR):
            op = self._previous()
            right = self._unary()
            expr = BinaryExpr(expr, op, right, expr.line)
        return expr

    def _unary(self):
        if self._match(TokenType.BANG, TokenType.MINUS):
            op = self._previous()
            right = self._unary()
            return UnaryExpr(op, right, op.line)
        return self._call()
    
    def _call(self):
        expr = self._primary()
        while True:
            if self._match(TokenType.LEFT_PAREN):
                expr = self._finish_call(expr)
            elif self._match(TokenType.DOT):
                name = self._consume(TokenType.IDENTIFIER, "Expect property name after '.'.")
                expr = GetExpr(expr, name, expr.line)
            else:
                break
        return expr

    def _finish_call(self, callee : Expr):
        arguments = []
        if not self._check(TokenType.RIGHT_PAREN):
            arguments.append(self._expression())
        error_reported = False
        while self._match(TokenType.COMMA):
            arguments.append(self._expression())
            if not error_reported and len(arguments) >= 255:
                self._error(self._peek(), "Can't have more than 255 arguments.")
                error_reported = True

        line = self._consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.").line
        return CallExpr(callee, arguments, line)


    def _primary(self):
        if self._match(TokenType.FALSE):
            return LiteralExpr(False, self._previous().line)
        elif self._match(TokenType.TRUE):
            return LiteralExpr(True, self._previous().line)
        elif self._match(TokenType.NIL):
            return LiteralExpr(None, self._previous().line)
        elif self._match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self._previous().literal, self._previous().line)
        elif self._match(TokenType.IDENTIFIER):
            return VarExpr(self._previous(), self._previous().line)
        elif self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return GroupingExpr(expr, expr.line)
        elif self._match(TokenType.THIS):
            keyword = self._previous()
            return ThisExpr(keyword, keyword.line)
        elif self._match(TokenType.SUPER):
            keyword = self._previous()
            self._consume(TokenType.DOT, "Expect '.' after 'super'.")
            method = self._consume(TokenType.IDENTIFIER, "Expect superclass method name.")
            return SuperExpr(keyword, method, keyword.line)
        else:
            token = self._peek()
            if token.type == TokenType.EOF:
                raise ParserException(f"Unexpected end of file.", token)
            else:                
                raise ParserException(f"Unexpected token [{token}]", token)
    
    def _consume(self, token_type, message) -> Token:
        if self._check(token_type):
            return self._advance()
        raise ParserException(message, self._peek())

    def _match(self, *token_types) -> bool:
        for token_type in token_types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _peek(self) -> Token:
        return self.tokens[self.current]
    
    def _previous(self) -> Token: 
        return self.tokens[self.current - 1]

    def _is_at_end(self) -> bool :
        return self._peek().type == TokenType.EOF
    
    def _check(self, token_type) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == token_type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _synchronize(self):
        self._advance()
        while not self._is_at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return
            if self._peek().type in {TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.FOR, TokenType.IF, \
                TokenType.WHILE, TokenType.PRINT, TokenType.RETURN}:
                return
            self._advance()

    def _error(self, token, message):
        self.error_handler.error(token, "Parser", message)
