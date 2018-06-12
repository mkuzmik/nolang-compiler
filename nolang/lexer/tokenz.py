from enum import Enum


class Token:

    def __init__(self, token_type, value, line, column):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return self.value + " (" + str(self.token_type) + ") "

    def __repr__(self):
        return self.value + " (" + str(self.token_type) + ") "


class TokenType(Enum):
    IDENTIFIER = 'identifier'

    NUMBER = 'number'
    STRING = 'string'

    PLUS = 'plus'
    MINUS = 'minus'
    TIMES = 'times'
    DIV = 'div'

    GREATER = 'greater than'
    GREATER_EQUAL = 'greater than or equal'
    LESS = 'less than'
    LESS_EQUAL = 'less than or equal'
    EQUAL = 'equal'

    ASSIGN = 'assign'

    LEFT_PAR = 'left parenthesis'
    RIGHT_PAR = 'right parenthesis'

    END_OF_INPUT = 'end of input'

    UNKNOWN = 'unknown token'

    LEFT_BRAC = 'left bracket'
    RIGHT_BRAC = 'right bracket'

    FUNCTION = 'function'
    PRINT = 'print'
    VARIABLE = 'variable'
    WHILE = 'while loop'

    END_OF_STATEMENT = 'end of statement'