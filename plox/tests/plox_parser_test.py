from plox_printer import PrettyPrint2ExprVisitor, PrettyPrintExprVisitor
from plox_error import ErrorHandler
from plox_parser import Parser
from plox_scanner import Scanner
from plox_data import *

def test1():
    error_handler = ErrorHandler()
    scanner = Scanner("1 + 2", error_handler)
    tokens = scanner.scan_tokens()
    #print (tokens)
    parser = Parser(tokens, error_handler)
    expr = parser.parse()

    assert type(expr) == BinaryExpr
    assert expr.operator.type == TokenType.PLUS

    assert type(expr.left) == LiteralExpr
    assert expr.left.value == 1.0

    assert type(expr.right) == LiteralExpr
    assert expr.right.value == 2.0
    
    pp = PrettyPrintExprVisitor()
    #print ("!!!! " + pp.print(expr))
    #print (expr)

def test2():
    error_handler = ErrorHandler()
    scanner = Scanner("1.2 + 2.3 / 12 > 23 - (117 / 0.5)", error_handler)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens, error_handler)
    expr = parser.parse()
    pp = PrettyPrint2ExprVisitor()
    #print (pp.print(expr))

    assert type(expr) == BinaryExpr
    assert expr.operator.type == TokenType.GREATER
    l1 = expr.left
    assert type (l1) == BinaryExpr
    assert l1.operator.type == TokenType.PLUS
    assert type(l1.left) == LiteralExpr
    assert l1.left.value == 1.2

    assert type(l1.right) == BinaryExpr
    assert type(l1.right.right) == LiteralExpr
    assert l1.right.right.value == 12.0
    assert type(l1.right.left) == LiteralExpr
    assert l1.right.left.value == 2.3

    r1 = expr.right
    assert type(r1) == BinaryExpr
    assert r1.operator.type == TokenType.MINUS
    assert type(r1.left) == LiteralExpr
    assert r1.left.value == 23.0
    assert type(r1.right) == GroupingExpr
    assert type(r1.right.expr) == BinaryExpr
    assert r1.right.expr.operator.type == TokenType.SLASH
    assert type(r1.right.expr.left) == LiteralExpr
    assert r1.right.expr.left.value == 117.0
    assert type(r1.right.expr.right) == LiteralExpr
    assert r1.right.expr.right.value == 0.5
    #print (expr)

