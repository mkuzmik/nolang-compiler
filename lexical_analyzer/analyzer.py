from lexical_analyzer.token import *


class Analyzer:

    def __init__(self, input):
        self.input = input
        self.position = 0
        self.line = 0
        self.column = 0

    def next_token(self):
        if self.position >= len(self.input):
            return Token(TokenType.END_OF_INPUT, '', self.line, self.column)

        char = self.input[self.position]

        if char.isalpha():
            return self.recognize_identifier()

        if char.isdigit():
            return self.recognize_number()

        if is_operator(char):
            return self.recognize_operator()

        if is_parenthesis(char):
            return self.recognize_parenthesis()

        if char == '\n':
            self.position += 1
            self.line += 1
            self.column = 0
            return self.next_token()

        return Token(TokenType.UNKNOWN, '', self.line, self.position)

    def recognize_identifier(self):
        pass


    def recognize_number(self):
        pass

    def recognize_operator(self):
        pass

    def recognize_parenthesis(self):
        position = self.position
        line = self.line
        column = self.column
        character = self.input[position]

        self.position += 1
        self.column += 1

        if character == '(':
            return Token(TokenType.LEFT_PAR, character, line, column)
        else:
            return Token(TokenType.RIGHT_PAR, character, line, column)


def is_operator(character):
    return character in "=+-<>*/"

def is_parenthesis(character):
    return character in "()"