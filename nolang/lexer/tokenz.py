from enum import Enum


class Token:

    def __init__(self, token_type, value, line, column):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return self.value + " (" + str(self.type) + ") "

    def __repr__(self):
        return self.value + " (" + str(self.type) + ") "


class TokenType(Enum):
    IDENTIFIER = 'identifier'

    NUMBER = 'number'
    STRING = 'string'

    BINARY_OPERATOR = 'binary operator'

    ASSIGN = 'assign'

    PAREN = 'parenthesis'
    BRACKET = 'bracket'

    END_OF_INPUT = 'end of input'

    UNKNOWN = 'unknown token'

    FUNCTION = 'function'
    PRINT = 'print'
    VARIABLE = 'variable'
    WHILE = 'while loop'

    END_OF_STATEMENT = 'end of statement'