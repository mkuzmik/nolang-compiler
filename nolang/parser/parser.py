from nolang.parser.ast import *
from nolang.lexer.tokenz import *

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.current_token = self.tokens[self.current]

    def next_token(self):
        self.current += 1
        self.current_token = self.tokens[self.current]
        return self.current_token

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.next_token()
        else:
            self.error()

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return NumberLiteral(token.value)

        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return StringLiteral(token.value)

        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Variable(token.value)

        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.value in ('*', '/'):
            token = self.current_token
            self.eat(TokenType.BINARY_OPERATOR)

            node = BinaryOperation(token.value, node, self.factor())

        return node

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.value in ('+', '-'):
            token = self.current_token
            self.eat(TokenType.BINARY_OPERATOR)
            node = BinaryOperation(token.value, node, self.term())

        return node

    def parse(self):
        node = self.expr()
        if self.current_token.type != TokenType.END_OF_INPUT:
            self.error()
        return node

# def parse(tokens):
#     global current
#     current = 0
#
#     def walk():
#         global current
#
#         token = tokens[current]
#
#         # TODO write math expression parser
#         if (token.type == TokenType.NUMBER) & (tokens[current + 1].type == TokenType.BINARY_OPERATOR):
#             operation = tokens[current + 1]
#             current += 2
#             return BinaryOperation(operation.value, NumberLiteral(token.value), walk())
#
#         if (token.type == TokenType.NUMBER) & (tokens[current + 1].type == TokenType.END_OF_STATEMENT):
#             current += 1
#             return NumberLiteral(token.value)
#
#
#         if token.type == TokenType.STRING:
#             current += 1
#             return StringLiteral(token.value)
#
#         if token.type == TokenType.VARIABLE:
#             current += 1
#             identifier = tokens[current]
#             return Declaration(identifier.value)
#
#         if (token.type == TokenType.BRACKET) & (token.value == '{'):
#             body = StatementSequence()
#             current += 1
#             while tokens[current].value != '}':
#                 body.add(walk())
#             return body
#
#         if (token.type == TokenType.IDENTIFIER) & (tokens[current + 1].type == TokenType.ASSIGN):
#             identifier = tokens[current]
#             current += 2
#             return Assignment(identifier.value, walk())
#
#         if (token.type == TokenType.IDENTIFIER):
#             identifier = tokens[current]
#             current += 1
#             return Variable(identifier.value)
#
#         if (token.type == TokenType.END_OF_STATEMENT):
#             current += 1
#             return
#
#     return walk()
