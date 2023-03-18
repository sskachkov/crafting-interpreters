from os import error, truncate
from plox_engine import Engine
from plox_parser import Parser
import sys
from plox_data import *
from plox_scanner import Scanner
from plox_error import ErrorHandler
"""
TokenType = Enum('TokenType', 'LEFT_PAREN RIGHT_PAREN LEFT_BRACE RIGHT_BRACE ' +
'COMMA DOT MINUS PLUS SEMICOLON SLASH STAR ' +
'BANG BANG_EQUAL EQUAL EQUAL_EQUAL LESS LESS_EQUAL ' +
'IDENTIFIER STRING NUMBER ' +
'AND CLASS ELSE FALSE FUN FOR IF NIL OR PRINT RETURN SUPER THIS TRUE VAR WHILE ' +
'EOF') 
"""

class Plox:
    def main(self):
        plox_engine = Engine()
        if len(sys.argv) > 2:
            print("Usage : plox [script]")
            sys.exit(64)
        elif len(sys.argv) == 2:
            plox_engine.run_file(sys.argv[1])
        else:
            plox_engine.run_prompt()


if __name__ == "__main__":
    plox = Plox()
    plox.main()