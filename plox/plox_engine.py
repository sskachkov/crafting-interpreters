from plox_interpreter import Interpreter
import sys
from plox_data import *
from plox_resolver import PloxResolver
from plox_scanner import Scanner
from plox_error import ErrorHandler, PloxException
from plox_parser import Parser

class Engine:
    def __init__(self):
        self.error_handler = ErrorHandler()
        pass

    def run_file(self, filename):
        with open(filename) as f: source = f.read()
        try:
            stmts = self._scan_and_parse(source)
            if self.error_handler.have_error():
                sys.exit(65)

            
            interpeter = Interpreter(self.error_handler)
            resolver = PloxResolver(self.error_handler, interpeter)
            resolver.resolve(stmts)
            if self.error_handler.have_error():
                sys.exit(65)

            interpeter.interpret_stmts(stmts)
        except PloxException as err:
            print (err)
            sys.exit(65)

    def run_prompt(self):
        interpeter = Interpreter(self.error_handler)
        while True:
            self.error_handler.clear_errors()
            print ('')
            line = input("> ")
            if line == '':
                break
            stmts = self._scan_and_parse(line)
            if self.error_handler.have_error():
                continue
            if len(stmts) == 1 and type(stmts[0]) == ExpressionStmt:
                expr = stmts[0].expr
                eval_res = interpeter.interpret_expr(expr)
                if self.error_handler.have_error():
                    continue
                print (interpeter.stringify(eval_res))
            else:
                interpeter.interpret_stmts(stmts)


    def _scan_and_parse(self, source : str) -> list [Stmt]:
            tokens = Scanner(source, self.error_handler).scan_tokens()
            return Parser(tokens, self.error_handler).parse()
        