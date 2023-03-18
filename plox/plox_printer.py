from plox_data import *

class PrettyPrintExprVisitor(ExprVisitor):
    def parenthesize(self, name, *exprs):
        return f"({name} {' '.join(exprs)})"

    def visit(self, expr, ctx):
        if type(expr) == LiteralExpr:
            return str(expr.value)
        elif type(expr) == GroupingExpr:
            return self.parenthesize("grouping", expr.expr.accept(self, ctx))
        elif type(expr) == UnaryExpr:
            return self.parenthesize(expr.operator.lexeme, expr.right.accept(self, ctx))
        elif type(expr) == BinaryExpr:
            return self.parenthesize(expr.operator.lexeme, expr.left.accept(self, ctx), expr.right.accept(self, ctx))
        return ""

    def print(self, expr : Expr):
        return expr.accept(self, {})

class PrettyPrint2ExprVisitor(ExprVisitor):
    def visit(self, expr, ctx):
        if type(expr) == LiteralExpr:
            indent = ctx['indent']
            ctx['indent'] += 4
            str = f"Literal({expr.value})"
            ctx['indent'] -= 4
            return str
        elif type(expr) == GroupingExpr:
            indent = ctx['indent']
            ctx['indent'] += 4
            str = f"Grouping(\n{' ' * indent}{expr.expr.accept(self, ctx)}\n{' ' * (indent - 4)})"
            ctx['indent'] -= 4
            return str
        elif type(expr) == UnaryExpr:
            indent = ctx['indent']
            ctx['indent'] += 4
            str = f"Unary(\n{' ' * indent}{expr.operator.lexeme}\n{' ' * indent}{expr.right.accept(self, ctx)}\n{' ' * (indent - 4)})"
            ctx['indent'] -= 4
            return str
        elif type(expr) == BinaryExpr:
            indent = ctx['indent']
            ctx['indent'] += 4
            str = f"Binary(\n{' ' * indent}{expr.left.accept(self, ctx)}\n{' ' * indent}{expr.operator.lexeme}\n{' ' * indent}{expr.right.accept(self, ctx)}\n{' ' * (indent - 4)})"
            ctx['indent'] -= 4
            return str
        return ""

    def print(self, expr : Expr):
        return expr.accept(self, {'indent' : 4})
