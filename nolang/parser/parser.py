from nolang.parser.ast import *
from nolang.lexer.tokenz import *


def parse(tokens):
    global current
    current = 0

    def walk():
        global current

        token = tokens[current]

        # TODO write math expression parser
        if (token.type == TokenType.NUMBER) & (tokens[current + 1].type == TokenType.BINARY_OPERATOR):
            operation = tokens[current + 1]
            current += 2
            return BinaryOperation(operation.value, NumberLiteral(token.value), walk())

        if (token.type == TokenType.NUMBER) & (tokens[current + 1].type == TokenType.END_OF_STATEMENT):
            current += 1
            return NumberLiteral(token.value)


        if token.type == TokenType.STRING:
            current += 1
            return StringLiteral(token.value)

        if token.type == TokenType.VARIABLE:
            current += 1
            identifier = tokens[current]
            return Declaration(identifier.value)

        if (token.type == TokenType.BRACKET) & (token.value == '{'):
            body = StatementSequence()
            current += 1
            while tokens[current].value != '}':
                body.add(walk())
            return body

        if (token.type == TokenType.IDENTIFIER) & (tokens[current + 1].type == TokenType.ASSIGN):
            identifier = tokens[current]
            current += 2
            return Assignment(identifier.value, walk())

        if (token.type == TokenType.IDENTIFIER):
            identifier = tokens[current]
            current += 1
            return Variable(identifier.value)

        if (token.type == TokenType.END_OF_STATEMENT):
            current += 1
            return

    return walk()
