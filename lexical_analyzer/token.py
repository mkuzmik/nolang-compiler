from enum import Enum


class Token:

    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return self.value + " (" + str(self.token_type) + ") "

    def __repr__(self):
        return self.value + " (" + str(self.token_type) + ") "


class TokenType(Enum):
    KEYWORD = 1
    OPERATOR = 2
    IDENTIFIER = 3
    CONSTANT = 4
    SYMBOL = 5
    UNKNOWN = 6
