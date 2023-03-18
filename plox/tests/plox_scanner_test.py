from plox_scanner import Scanner
from plox_error import ErrorHandler
from plox_data import *

def test1():
    error_handler = ErrorHandler()
    scanner = Scanner("1 + 2", error_handler)
    tokens = scanner.scan_tokens()
    assert len(tokens) == 4

    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].literal == 1.0
    assert tokens[1].type == TokenType.PLUS
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].literal == 2.0

    assert tokens[-1].type == TokenType.EOF

def test2():
    error_handler = ErrorHandler()
    scanner = Scanner("1.2 + 2.3 / 12 > 23 - (117 / 0.5)", error_handler)
    tokens = scanner.scan_tokens()
    assert len(tokens) == 14

    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].literal == 1.2
    assert tokens[1].type == TokenType.PLUS
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].literal == 2.3
    assert tokens[3].type == TokenType.SLASH
    assert tokens[4].type == TokenType.NUMBER
    assert tokens[4].literal == 12
    assert tokens[5].type == TokenType.GREATER
    assert tokens[6].type == TokenType.NUMBER
    assert tokens[6].literal == 23
    assert tokens[7].type == TokenType.MINUS
    assert tokens[8].type == TokenType.LEFT_PAREN
    assert tokens[9].type == TokenType.NUMBER
    assert tokens[9].literal == 117
    assert tokens[10].type == TokenType.SLASH
    assert tokens[11].type == TokenType.NUMBER
    assert tokens[11].literal == 0.5
    assert tokens[12].type == TokenType.RIGHT_PAREN

    assert tokens[-1].type == TokenType.EOF
