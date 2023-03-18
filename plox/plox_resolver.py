from os import error
from plox_error import ErrorHandler, InterpeterException, ResolverException, ReturnException
from plox_data import *

class FuncType(Enum):
    NONE, FUNC, INITIALIZER, METHOD = range(4)

class ClassType(Enum):
    NONE, CLASS, SUBCLASS = range(3)

class PloxResolver(ExprVisitor):
    def __init__(self, error_handler: ErrorHandler, interpreter) -> None:
        self.error_handler = error_handler
        self.interpreter = interpreter
        self.curr_func = FuncType.NONE
        self.curr_class = ClassType.NONE
        self.scopes = []

    def __repr__(self) -> str:
        return f"PloxResolver()"

    def resolve(self, stmts : list [Stmt]):
        ctx = {}
        for stmt in stmts:
            stmt.accept(self, ctx)

    def visit_stmt(self, stmt : Stmt, ctx):
        st = type(stmt)
        if st == BlockStmt:
            self._begin_scope(ctx)
            self._resolve(stmt.stmts, ctx)
            self._end_scope(ctx)
        elif st == VarDeclStmt:
            self._declare(stmt.name, ctx)
            if stmt.initializer != None:
                self._resolve(stmt.initializer, ctx)
            self._define(stmt.name, ctx)
        elif st == FunDeclStmt:
            self._define(stmt.name, ctx)
            self._declare(stmt.name, ctx)
            self._resolve_func(stmt, FuncType.FUNC, ctx)
        elif st == ExpressionStmt:
            self._resolve(stmt.expr, ctx)
        elif st == IfStmt:
            self._resolve(stmt.condition, ctx)
            self._resolve(stmt.then_branch, ctx)
            if stmt.else_branch != None:
                self._resolve(stmt.else_branch, ctx)
        elif st == PrintStmt:
            self._resolve(stmt.expr, ctx)
        elif st == WhileStmt:
            self._resolve(stmt.expr, ctx)
            self._resolve(stmt.body, ctx)
        elif st == ForStmt:
            self._begin_scope(ctx)
            self._resolve(stmt.initializer, ctx)
            self._resolve(stmt.condition, ctx)
            self._resolve(stmt.increment, ctx)
            self._resolve(stmt.body, ctx)
            self._end_scope(ctx)
        elif st == ReturnStmt:
            if self.curr_func == FuncType.NONE:
                self._error(stmt, "Can't return from top level code.")
            if stmt.value != None:
                if self.curr_func == FuncType.INITIALIZER:
                    self._error(stmt, "Can't return a value from an initializer.")
                self._resolve(stmt.value, ctx)
        elif st == ClassDeclStmt:
            encl_class = self.curr_class
            self.curr_class = ClassType.CLASS
            self._declare(stmt.name, ctx)
            self._define(stmt.name, ctx)
            if stmt.superclass != None:
                if stmt.name.lexeme == stmt.superclass.name.lexeme:
                    self._error(stmt, "A class can't inherit from itself.")
                self.curr_class = ClassType.SUBCLASS
                self._resolve(stmt.superclass, ctx)
                self._begin_scope(ctx)
                self.scopes[-1]["super"] = True
            self._begin_scope(ctx)
            self.scopes[-1]['this'] = True
            for method in stmt.methods:
                func_type = FuncType.METHOD
                if method.name.lexeme == "init":
                    func_type = FuncType.INITIALIZER
                self._resolve_func(method, func_type, ctx)

            if stmt.superclass != None:
                self._end_scope(ctx)
            self._end_scope(ctx)
            self.curr_class = encl_class

    def visit_expr(self, expr : Expr, ctx):
        et = type(expr)
        if et == VarExpr:
            if len(self.scopes) > 0 and self.scopes[-1].get(expr.name.lexeme) == False:
                self._error(expr, "Can't read local variable in its own initializer.")
            self._resolve_local(expr, expr.name, ctx)
        elif et == AssignExpr:
            self._resolve(expr.value, ctx)
            self._resolve_local(expr, expr.name, ctx)
        elif et == BinaryExpr:
            self._resolve(expr.left, ctx)
            self._resolve(expr.right, ctx)
        elif et == CallExpr:
            self._resolve(expr.callee, ctx)
            for arg in expr.arguments:
                self._resolve(arg, ctx)
        elif et == GroupingExpr:
            self._resolve(expr.expr, ctx)
        elif et == LiteralExpr:
            pass # do nothing
        elif et == LogicalExpr:
            self._resolve(expr.left, ctx)
            self._resolve(expr.right, ctx)
        elif et == UnaryExpr:
            self._resolve(expr.right, ctx)
        elif et == GetExpr:
            self._resolve(expr.object, ctx)
        elif et == SetExpr:
            self._resolve(expr.object, ctx)
            self._resolve(expr.value, ctx)
        elif et == ThisExpr:
            if self.curr_class == ClassType.NONE:
                self._error(expr, "Can't use 'this' outside of a class.")
            self._resolve_local(expr, expr.keyword, ctx)
        elif et == SuperExpr:
            if self.curr_class == ClassType.NONE:
                self._error(expr.keyword, "Can't use 'super' outside of a class.")
            elif self.curr_class != ClassType.SUBCLASS:
                self._error(expr.keyword, "Can't use 'super' in a class without superclass.")
            self._resolve_local(expr, expr.keyword, ctx)

        

    def _resolve_func(self, func : FunDeclStmt, func_type : FuncType, ctx):
        encl_func = self.curr_func
        self.curr_func = func_type
        self._begin_scope(ctx)
        for param in func.params:
            self._declare(param, ctx)
            self._define(param, ctx)
        self._resolve(func.body, ctx)
        self._end_scope(ctx)
        self.curr_func = encl_func

    def _resolve_local(self, expr: Expr, name : Token, ctx):
        for i in range(len(self.scopes) -1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i, ctx)
                return
            
    def _error(self, token, message):
        self.error_handler.error(token, "Resolver", message)

    def _begin_scope(self, ctx):
        self.scopes.append({})

    def _end_scope(self, ctx):
        self.scopes.pop()

    def _declare(self, name: Token, ctx):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        if name.lexeme in scope:
            self._error(name, "Already a variable with this name in this scope.")    
        scope[name.lexeme] = False

    def _define(self, name: Token, ctx):
        if len(self.scopes) == 0:
            return
        self.scopes[-1][name.lexeme] = True

    def _resolve(self, obj, ctx):
        if isinstance(obj, Stmt) or isinstance(obj, Expr):
            obj.accept(self, ctx)
        elif type(obj) == list:
            for e in obj:
                self._resolve(e, ctx)
        else:
            line = obj.line if hasattr(obj, 'line') else -1
            print (obj)
            raise ResolverException(f"Internal Error: tried to resolve unsupported type: {type(obj)}", line)


def a() -> tuple[int, int]:
    pass