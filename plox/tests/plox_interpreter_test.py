from plox_scanner import Scanner
from plox_parser import Parser
from plox_error import ErrorHandler, PloxError
from plox_interpreter import Interpreter
from plox_data import *

def test1():
    assert interpret_success('2 + 3') == 5.0
    assert interpret_success('2 - 3') == -1.0
    assert interpret_success('2 + 3 * 3') == 11.0
    assert interpret_success('(2 + 3) * 3') == 15.0
    assert interpret_success('1 / 4') == 0.25
    assert interpret_success('(2 + 3) * 3 + 15 - 25 == 5') == True
    assert interpret_success('(2 + 3) * 3 + 15 - 25 > 5') == False

def test2():
    assert interpret_error('2 -').category == 'ParserError'
    assert interpret_error('2 -"1"').category == 'InterpreterError'

    assert interpret_error("2 + 3").category == 'None' 

def interpret_error(source : str):
    error_handler = ErrorHandler()

    scanner = Scanner(source, error_handler)
    tokens = scanner.scan_tokens()
    if error_handler.have_error():
        return error_handler.pop_last_error()

    parser = Parser(tokens, error_handler)
    expr = parser.parse()
    if error_handler.have_error():
        return error_handler.pop_last_error()

    interpeter = Interpreter(error_handler)
    eval_res = interpeter.interpret_expr(expr)
    if error_handler.have_error():
        return error_handler.pop_last_error()

    return PloxError("-1", "None", "Success")

def interpret_success(source : str):
    error_handler = ErrorHandler()
    scanner = Scanner(source, error_handler)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens, error_handler)
    expr = parser.parse()
    interpeter = Interpreter(error_handler)
    return interpeter.interpret_expr(expr)
