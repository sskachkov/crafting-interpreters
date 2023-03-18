from enum import Enum

class TokenType(Enum):
    LEFT_PAREN, RIGHT_PAREN, LEFT_BRACE, RIGHT_BRACE, COMMA, DOT, MINUS, PLUS, \
    SEMICOLON, SLASH, STAR, BANG, BANG_EQUAL, EQUAL, EQUAL_EQUAL, GREATER, \
    GREATER_EQUAL, LESS, LESS_EQUAL, IDENTIFIER, STRING, NUMBER, AND, CLASS, \
    ELSE, FALSE, FUN, FOR, IF, NIL, OR, PRINT, RETURN, SUPER, THIS, TRUE, VAR,\
    WHILE, EOF= range(39)

class Token:
    def __init__(self, token_type : TokenType, lexeme, literal, line):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    def __repr__(self):
        return f"Token({self.type.name}, '{self.lexeme}', {self.literal})"

class Expr:
    pass

class Stmt:
    pass

class ExprVisitor:
    def visit_expr(self, expr : Expr, ctx):
        pass

class StmtVisitor:
    def visit_stmt(self, stmt : Stmt, ctx):
        pass

class Expr:
    def __init__(self, line : int) -> None:
        self.line = line

    def accept(self, visitor: ExprVisitor, ctx):
        return visitor.visit_expr(self, ctx)

class LiteralExpr(Expr):
    def __init__(self, value, line : int):
        super().__init__(line)
        self.value = value

    def __repr__(self) -> str:
        return f"Literal({self.value}, {self.line})"

class GroupingExpr(Expr):
    def __init__(self, expr, line : int):
        super().__init__(line)
        self.expr = expr

    def __repr__(self) -> str:
        return f"GroupingExpr({self.expr}, {self.line})"

class UnaryExpr(Expr):
    def __init__(self, operator, right, line : int):
        super().__init__(line)
        self.operator = operator
        self.right = right

    def __repr__(self) -> str:
        return f'Unary({self.operator}, {self.right}, {self.line})'

class AssignExpr(Expr):
    def __init__(self, name : Token, value : Expr, line : int):
        super().__init__(line)
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f'Assign({self.name}, {self.value}, {self.line})'

class BinaryExpr(Expr):
    def __init__(self, left, operator, right, line : int):
        super().__init__(line)
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self) -> str:
        return f'Binary({self.left}, {self.operator}, {self.right}, {self.line})'

class LogicalExpr(Expr):
    def __init__(self, left: Expr, op : Token, right : Expr, line: int) -> None:
        super().__init__(line)
        self.left = left
        self.op  = op
        self.right = right

    def __repr__(self) -> str:
        return f"LogicalExpr({self.left}, {self.op}, {self.right}, {self.line})"

class VarExpr(Expr):
    def __init__(self, name : Token, line : int) -> None:
        super().__init__(line)
        self.name = name

    def __repr__(self) -> str:
        return f"VarExpr({self.name}, {self.line})"

class CallExpr(Expr):
    def __init__(self, callee : Expr, arguments : list [Expr], line: int) -> None:
        super().__init__(line)
        self.callee = callee
        self.arguments = arguments
    
    def __repr__(self) -> str:
        return f"CallExpr({self.callee}, {self.arguments})"
    
class GetExpr(Expr):
    def __init__(self, object : Expr, name : Token, line: int) -> None:
        super().__init__(line)
        self.object = object
        self.name = name
    
    def __repr__(self) -> str:
        return f"GetExpr({self.object}, {self.name})"

class SetExpr(Expr):
    def __init__(self, object : Expr, name : Token, value : Expr, line: int) -> None:
        super().__init__(line)
        self.object = object
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f"SetExpr({self.object}, {self.name}, {self.value})"

class SuperExpr(Expr):
    def __init__(self, keyword : Token, method : Token, line: int) -> None:
        super().__init__(line)
        self.keyword = keyword
        self.method = method

    def __repr__(self) -> str:
        return f"SuperExpr({self.keyword}, {self.method})"

class ThisExpr(Expr):
    def __init__(self, keyword : Expr, line: int) -> None:
        super().__init__(line)
        self.keyword = keyword

    def __repr__(self) -> str:
        return f"ThisExpr({self.keyword})"


class Stmt:
    def __init__(self, line : int) -> None:
        self.line = line

    def accept(self, visitor: StmtVisitor, ctx):
        return visitor.visit_stmt(self, ctx)

class ReturnStmt(Stmt):
    def __init__(self, value : Expr, line: int) -> None:
        super().__init__(line)
        self.value = value
    
    def __repr__(self) -> str:
        return f"ReturnStmt({self.value})"

class ExpressionStmt(Stmt):
    def __init__(self, expr : Expr, line : int) -> None:
        super().__init__(line)
        self.expr = expr

    def __repr__(self) -> str:
        return f"ExpressionStmt({self.expr}, {self.line})"

class IfStmt(Stmt):
    def __init__(self, condition, then_branch, else_branch, line : int) -> None:
        super().__init__(line)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self) -> str:
        return f"IfStmt({self.condition}, {self.then_branch}, {self.else_branch}, {self.line})"


class PrintStmt(Stmt):
    def __init__(self, expr : Expr, line : int) -> None:
        super().__init__(line)
        self.expr = expr

    def __repr__(self) -> str:
        return f"PrintStmt({self.expr}, {self.line})"

class VarDeclStmt(Stmt):
    def __init__(self, name : Token, initializer : Expr, line : int) -> None:
        super().__init__(line)
        self.name = name
        self.initializer = initializer

    def __repr__(self) -> str:
        return f"VarDeclStmt({self.name}, {self.initializer}, {self.line})"

class WhileStmt(Stmt):
    def __init__(self, expr : Expr, body : Stmt, line: int) -> None:
        super().__init__(line)
        self.expr = expr
        self.body = body

    def __repr__(self) -> str:
        return f"WhileStmt({self.expr}, {self.body})"

class ForStmt(Stmt):
    def __init__(self, initializer : Stmt, condition : Expr, increment : Expr, body : Stmt, line: int) -> None:
        super().__init__(line)
        self.initializer = initializer
        self.condition = condition
        self.increment = increment
        self.body = body
    
    def __repr__(self) -> str:
        return f"ForStmt({self.initializer}, {self.condition}, {self.increment}, {self.body})"

class BlockStmt(Stmt):
    def __init__(self, stmts, line : int) -> None:
        super().__init__(line)
        self.stmts = stmts

    def __repr__(self) -> str:
        return f"BlockStmt({self.stmts}, {self.line})"

class FunDeclStmt(Stmt):
    def __init__(self, name : Token, params : list [Token], body : list [Stmt], line: int) -> None:
        super().__init__(line)
        self.name = name
        self.params = params
        self.body = body
    def __repr__(self) -> str:
        return f"FunDeclStmt({self.name}, {self.params}, {self.body})"

class ClassDeclStmt(Stmt):
    def __init__(self, name : Token, superclass : VarExpr, methods : list [FunDeclStmt], line: int) -> None:
        super().__init__(line)
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def __repr__(self) -> str:
        return f"ClassDeclStmt({self.name} {self.superclass}, {self.methods})"



