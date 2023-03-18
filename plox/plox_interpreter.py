from __future__ import annotations
import time
from plox_error import ErrorHandler, InterpeterException, ReturnException
from plox_data import *

class Environment:
    pass

class Interpreter(ExprVisitor):
    def __init__(self, error_handler : ErrorHandler) -> None:
        self.error_handler = error_handler
        self.globals = Environment()
        self.locals : map[Expr, int] = {}
        self.environment = self.globals
        self.globals.define(Token(TokenType.IDENTIFIER, "clock", "clock", -1), PloxClockNF())

    def interpret_stmts(self, stmts):
        try:
            ctx = {}
            for stmt in stmts:
                self._execute(stmt, ctx)
        except InterpeterException as err:
            self.error_handler.exception(err)

    def interpret_expr(self, expr : Expr):
        try:
            eval_res = self._evaluate(expr, {})
            return eval_res
        except InterpeterException as err:
            self.error_handler.exception(err)
            return None
    
    def resolve(self, expr : Expr, depth : int, ctx):
        self.locals[expr] = depth

    def _evaluate(self, expr : Expr, ctx):
        return expr.accept(self, ctx)

    def _execute(self, stmt: Stmt, ctx):
        stmt.accept(self, ctx)

    def _check_number_operand(self, operator, operand):
        if type(operand) != float:
            raise InterpeterException("Operand must be a number.", operator)

    def _check_number_operands(self, operator, left, right):
        if type(left) != float or type(right) != float:
            raise InterpeterException("Operands must be numbers.", operator)

    def visit_stmt(self, stmt : Stmt, ctx):
        if type(stmt) == PrintStmt:
            eval_res = self._evaluate(stmt.expr, ctx)
            print(self.stringify(eval_res))
            return
        elif type(stmt) == ExpressionStmt:
            eval_res = self._evaluate(stmt.expr, ctx)
            return
        elif type(stmt) == VarDeclStmt:
            if stmt.initializer != None:
                value = self._evaluate(stmt.initializer, ctx)
            else:
                value = None
            self.environment.define(stmt.name, value)
        elif type(stmt) == BlockStmt:
            self._execute_block(stmt.stmts, Environment(self.environment), ctx)
        elif type(stmt) == IfStmt:
            if self._is_truth(self._evaluate(stmt.condition, ctx)):
                self._execute(stmt.then_branch, ctx)
            elif stmt.else_branch != None:
                self._execute(stmt.else_branch, ctx)
        elif type(stmt) == WhileStmt:
            while self._is_truth(self._evaluate(stmt.expr, ctx)):
                self._execute(stmt.body, ctx)
        elif type(stmt) == ForStmt:
            self._execute_for(stmt, Environment(self.environment), ctx)
        elif type(stmt) == FunDeclStmt:
            plox_fun = PloxFun(stmt, self.environment)
            self.environment.define(stmt.name, plox_fun)
        elif type(stmt) == ReturnStmt:
            value = None
            if stmt.value != None:
                value = self._evaluate(stmt.value, ctx)
            raise ReturnException(value)
        elif type(stmt) == ClassDeclStmt:
            self.environment.define(stmt.name, None)
            methods = {}
            supercl = None
            if stmt.superclass != None:
                supercl = self._evaluate(stmt.superclass, ctx)
                if type(supercl) != PloxClass:
                    raise InterpeterException(f"{stmt.name.lexeme} superclass, must be a class.", stmt)
                self.environment = Environment(self.environment)
                self.environment.define_str("super", supercl)
            for method in stmt.methods:
                func = PloxFun(method, self.environment, method.name.lexeme == "init")
                methods[method.name.lexeme] = func
            
            kl = PloxClass(stmt.name, supercl, methods)
            if stmt.superclass != None:
                self.environment = self.environment.parent
            self.environment.assign(stmt.name, kl)
        else:
            raise InterpeterException(f"Unknown statement [{type(stmt).__name__}].", stmt)

    def visit_expr(self, expr : Expr, ctx):
        if type(expr) == LiteralExpr:
            return expr.value
        elif type(expr) == GroupingExpr:
            return self._evaluate(expr.expr, ctx)
        elif type(expr) == UnaryExpr:
            eval_res = self._evaluate(expr.right, ctx)
            if expr.operator.type == TokenType.BANG:
                return not self._is_truth(eval_res)
            elif expr.operator.type == TokenType.MINUS:
                self._check_number_operand(expr.operator, eval_res)
                return -eval_res
        elif type(expr) == BinaryExpr:
            eval_left = self._evaluate(expr.left, ctx)
            eval_right = self._evaluate(expr.right, ctx)
            if expr.operator.type == TokenType.MINUS:
                self._check_number_operands(expr.operator, eval_left, eval_right)
                return eval_left - eval_right
            elif expr.operator.type == TokenType.PLUS:
                if (type(eval_left) == float and type(eval_right) == float) or \
                   (type(eval_left) == str and type(eval_right) == str):
                    return eval_left + eval_right
                elif (type(eval_left) == str and type(eval_right) == float):
                    return eval_left + str(int(eval_right) if eval_right.is_integer() else eval_right)
                elif (type(eval_left) == str):
                    return eval_left + self.stringify(eval_right)
                else:
                    raise InterpeterException("Unsupported operand types for PLUS operation.", expr.operator)
            elif expr.operator.type == TokenType.SLASH:
                self._check_number_operands(expr.operator, eval_left, eval_right)
                try:
                    return eval_left / eval_right
                except ZeroDivisionError:
                    raise InterpeterException("Division by zero.", expr.operator) 
            elif expr.operator.type == TokenType.STAR:
                self._check_number_operands(expr.operator, eval_left, eval_right)
                return eval_left * eval_right
            elif expr.operator.type == TokenType.GREATER:
                self._check_number_operands(expr.operator, eval_left, eval_right)
                return eval_left > eval_right
            elif expr.operator.type == TokenType.GREATER_EQUAL:
                self._check_number_operands(expr.operator, eval_left, eval_right)
                return eval_left >= eval_right
            elif expr.operator.type == TokenType.LESS:
                self._check_number_operands(expr.operator, eval_left, eval_right)
                return eval_left < eval_right
            elif expr.operator.type == TokenType.LESS_EQUAL:
                self._check_number_operands(expr.operator, eval_left, eval_right)
                return eval_left <= eval_right
            elif expr.operator.type == TokenType.EQUAL_EQUAL:
                return eval_left == eval_right
            elif expr.operator.type == TokenType.BANG_EQUAL:
                return eval_left != eval_right
        elif type(expr) == VarExpr:
            return self._lookup_variable(expr.name, expr)
        elif type(expr) == AssignExpr:
            value = self._evaluate(expr.value, ctx)
            if expr in self.locals:
                distance = self.locals[expr]
                self.environment.assign_at(distance, expr.name, value)
            else:
                self.globals.assign(expr.name, value)
            return value
        elif type(expr) == LogicalExpr:
            eval_left = self._evaluate(expr.left, ctx)
            if self._is_truth(eval_left): 
                if expr.op.type == TokenType.OR:
                    return eval_left
                elif expr.op.type == TokenType.AND:
                    return self._evaluate(expr.right, ctx)
            else:
                if expr.op.type == TokenType.OR:
                    return self._evaluate(expr.right, ctx)
                elif expr.op.type == TokenType.AND:
                    return eval_left
        elif type(expr) == CallExpr:
            callee = self._evaluate(expr.callee, ctx)
            if not isinstance(callee, PloxCallable):
                raise InterpeterException(f"Can only call functions and classes.", expr)
            arguments = [self._evaluate(arg, ctx) for arg in expr.arguments]
            if len(arguments) != callee.arity():
                raise InterpeterException(f"Expected {callee.arity()} arguments, but got {len(arguments)}.")
            return callee.call(self, arguments, ctx)
        elif type(expr) == GetExpr:
            obj = self._evaluate(expr.object, ctx)
            if type(obj) == PloxInstance:
                return obj.get(expr.name)
            raise InterpeterException(f"Only instances have properties.", expr)
        elif type(expr) == SetExpr:
            obj = self._evaluate(expr.object, ctx)
            if type(obj) == PloxInstance:
                value = self._evaluate(expr.value, ctx)
                return obj.set(expr.name, value)
            raise InterpeterException(f"Only instances have fields.", expr)
        elif type(expr) == ThisExpr:
            return self._lookup_variable(expr.keyword, expr)
        elif type(expr) == SuperExpr:
            distance = self.locals[expr]
            superclass = self.environment.get_at(distance, "super")
            obj = self.environment.get_at(distance - 1, "this")
            method = superclass.find_method(expr.method.lexeme)
            if method == None:
                raise InterpeterException(f"Undefined property {expr.method.lexeme}", expr)
            return method.bind(obj)
        else:
            raise InterpeterException(f"Unknown expression [{type(expr).__name__}].", expr)

    def _execute_for(self, for_stmt : ForStmt, environment : Environment, ctx):
        orig_env = self.environment
        try:
            self.environment = environment
            if for_stmt.initializer != None:
                self._execute(for_stmt.initializer, ctx)
            cond = for_stmt.condition if for_stmt.condition != None else LiteralExpr(True, for_stmt.line)
            while self._is_truth(self._evaluate(cond, ctx)):
                self._execute(for_stmt.body, ctx)
                if for_stmt.increment != None:
                    self._evaluate(for_stmt.increment, ctx)
        finally:
            self.environment = orig_env

    def _execute_block(self, stmts, environment: Environment, ctx):
        orig_env = self.environment
        try:
            self.environment = environment
            for stmt in stmts:
                self._execute(stmt, ctx)
        finally:
            self.environment = orig_env

    def _is_truth(self, obj):
        if obj == None:
            return False
        elif type(obj) == bool:
            return obj
        else:
            return True
    
    def _lookup_variable(self, name : Token, expr : Expr):
        if expr in self.locals:
            distance = self.locals[expr]
            return self.environment.get_at(distance, name)
        else:
            return self.globals.get(name)
    
    def stringify(self, obj) -> str:
        if obj == None:
            return "nil"
        elif type(obj) == float:
            return str(int(obj) if obj.is_integer() else obj)
        else:
            return str(obj)


class Environment:
    def __init__(self, parent : Environment = None) -> None:
        self.values = {}
        self.parent = parent

    def get_at(self, distance: int, name : Token):
        if type(name) == Token:
            name = name.lexeme
        return self._ancestor(distance).values[name]
    
    def assign_at(self, distance : int, name : Token, value : object):
        self._ancestor(distance).values[name.lexeme] = value

    def _ancestor(self, distance : int) -> Environment:
        res = self
        for i in range(distance):
            res = res.parent
        return res

    def define_str(self, name : str, value : object):
        self.values[name] = value


    def define(self, name : Token, value : object):
        name_s = name.lexeme
        if type(name) != Token:
            raise InterpeterException(f"Cannot use objects of type {type(name).__name__} as names.", name)
        self.values[name_s] = value


    def assign(self, name : Token, value):
        if type(name) != Token:
            raise InterpeterException(f"Cannot use objects of type {type(name).__name__} as names.", name)
        
        name_s = name.lexeme

        if name_s in self.values:
            self.values[name_s] = value
        elif self.parent != None:
            self.parent.assign(name, value)
        else:
            raise InterpeterException(f"Undefined variable {name_s}", name)

    def get(self, name : Token) -> object:
        if type(name) != Token:
            raise InterpeterException(f"Cannot use objects of type {type(name).__name__} as names.", name)
        name_s = name.lexeme

        if name_s in self.values:
            return self.values[name_s]
        if self.parent != None:
            return self.parent.get(name_s)
        else:
            raise InterpeterException(f"Undefined variable {name_s}", name)

class PloxCallable:
    def arity(self) -> int:
        raise NotImplemented("Implement me")
    def call(self, interpreter : Interpreter, arguments : list [Expr], ctx):
        raise NotImplemented("Implement me")

class PloxClockNF(PloxCallable):
    def arity(self) -> int:
        return 0
    
    def call(self, interpreter: Interpreter, arguments: list[Expr], ctx):
        return time.time()
    
    def __repr__(self) -> str:
        return "<PloxClock native fn>"

class PloxClass(PloxCallable):
    def __init__(self, name : str, superclass : PloxClass, methods : dict [str, PloxFun]) -> None:
        self.name = name
        self.superclass = superclass
        self.methods = methods
    
    def call(self, interpreter: Interpreter, arguments: list[Expr], ctx):
        instance = PloxInstance(self)
        initializer = self.find_method("init")
        if initializer != None:
            initializer.bind(instance).call(interpreter, arguments, ctx)
        return instance


    def arity(self) -> int:
        initializer = self.find_method("init")
        if initializer != None:
            return initializer.arity()
        return 0

    def find_method(self, name : str):
        if name in self.methods:
            return self.methods[name]
        if self.superclass != None:
            return self.superclass.find_method(name)
        return None

    def __repr__(self) -> str:
        return f"<PloxClass {self.name.lexeme}{' (' + self.superclass.name.lexeme + ')' if self.superclass != None else ''}>"

class PloxInstance:
    def __init__(self, plox_class : PloxClass) -> None:
        self.plox_class = plox_class
        self.fields = {}

    def get(self, name : Token):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]
        
        method = self.plox_class.find_method(name.lexeme)
        if method != None:
            return method.bind(self)
        raise InterpeterException(f"Undefined property {name.lexeme}.", name)

    def set(self, name : Token, value : object):
        self.fields[name.lexeme] = value

    def __repr__(self) -> str:
        return f"PloxInstance({self.plox_class.name.lexeme})"
        
        
class PloxFun(PloxCallable):
    def __init__(self, fun_decl : FunDeclStmt, closure : Environment, is_initializer = False) -> None:
        self.fun_decl = fun_decl
        self.closure = closure
        self.is_initializer = is_initializer

    def arity(self) -> int:
        return len(self.fun_decl.params)

    def call(self, interpreter: Interpreter, arguments: list[Expr], ctx):
        env = Environment(self.closure)
        ret_val = None
        for i in range(0, len(self.fun_decl.params)):
            env.define(self.fun_decl.params[i], arguments[i])
        try:
            interpreter._execute_block(self.fun_decl.body, env, ctx)
        except ReturnException as re:
            ret_val = re.value
        if self.is_initializer:
            ret_val = self.closure.get_at(0, "this")
        return ret_val
     
    def bind(self, instance : PloxInstance) -> PloxFun:
         env = Environment(self.closure)
         env.define_str("this", instance)
         return PloxFun(self.fun_decl, env, self.is_initializer)


    def __repr__(self) -> str:
        return f"<PloxFun {self.fun_decl.name} fn>"
