from plox_data import *

class PloxException(Exception):
    def __init__(self, message, line : int):
        self.message = message
        self.line = line

    def __repr__(self) -> str:
        return f"PloxError({self.message})"

    def _category(self):
        return "PloxError"

class ParserException(PloxException):
    def __init__(self, message, token : Token):
        super().__init__(message, token.line)

    def __repr__(self) -> str:
        return f"ParserError({self.message}, {self.token})"

    def _category(self):
        return "ParserError"

class InterpeterException(PloxException):
    def __init__(self, message, expr):
        super().__init__(message, expr.line)

    def __repr__(self) -> str:
        return f"InterpreterError({self.message}, {self.token})"

    def _category(self):
        return "InterpreterError"

class ResolverException(PloxException):
    def __init__(self, message, line: int):
        super().__init__(message, line)

class ReturnException(Exception):
    def __init__(self, value : object) -> None:
        self.value = value
    
    def __repr__(self) -> str:
        return f"ReturnException({self.object})"

class PloxError:
    def __init__(self, line, category, message):
        self.line = line
        self.category = category
        self.message = message

    def __repr__(self) -> str:
        return f"PloxError({self.line}, {self.category}, {self.message})"
    
class ErrorHandler:
    def __init__(self):
        self.errors = []

    def clear_errors(self):
        self.errors.clear()

    def pop_last_error(self):
        return self.errors.pop()
    
    def have_error(self):
        return len(self.errors) > 0

    def exception(self, exc: PloxException):
        self._error(exc.line, exc._category(), exc.message)

    def error(self, token : Token, category : str, message : str):
        self._error(token.line, category, message)
        
    def _error(self, line, category, message):
        self.errors.append(PloxError(line, category, message))
        self.__report(line, '', category, message)

    def __report(self, line_num, where, category, message):
        print(f"[line {line_num}]  Error {where}: [{category}] {message}")
