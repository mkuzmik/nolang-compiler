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
        node = self.factor()

        while self.current_token.value in ('*', '/'):
            token = self.current_token
            self.eat(TokenType.BINARY_OPERATOR)

            node = BinaryOperation(token.value, node, self.factor())

        return node

    def expr(self):
        node = self.term()

        while self.current_token.value in ('+', '-'):
            token = self.current_token
            self.eat(TokenType.BINARY_OPERATOR)
            node = BinaryOperation(token.value, node, self.term())

        return node

    def program(self):
        node = self.compound()
        return node

    def compound(self):
        self.eat(TokenType.LBRACKET)
        nodes = self.statement_seq()
        self.eat(TokenType.RBRACKET)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_seq(self):
        node = self.statement()
        res = [node]
        while self.current_token.type != TokenType.RBRACKET:
            if (self.current_token.type == TokenType.END_OF_STATEMENT):
                self.eat(TokenType.END_OF_STATEMENT)
            res.append(self.statement())

        if self.current_token.type == TokenType.IDENTIFIER:
            self.error()

        return res

    def statement(self):
        if self.current_token.type == TokenType.LBRACKET:
            node = self.compound()
        elif self.current_token.type == TokenType.IDENTIFIER:
            node = self.assignment_statement()
        elif self.current_token.type == TokenType.VARIABLE:
            node = self.declaration_statement()
        elif self.current_token.type == TokenType.PRINT:
            node = self.print_statement()
        elif self.current_token.type == TokenType.WHILE:
            node = self.while_loop()
        else:
            node = self.empty()
        return node

    def while_loop(self):
        self.eat(TokenType.WHILE)
        condition_exp = self.condition()
        body = self.compound()
        node = WhileLoop(condition_exp, body)
        return node

    def condition(self):
        self.eat(TokenType.LPAREN)
        left = self.expr()
        condition = self.current_token.value
        self.eat(TokenType.BINARY_OPERATOR)
        right = self.expr()
        self.eat(TokenType.RPAREN)
        node = Condition(condition, left, right)
        return node

    def print_statement(self):
        self.eat(TokenType.PRINT)
        expression = self.expr()
        node = PrintStatement(expression)
        return node

    def assignment_statement(self):
        variable = self.variable()
        self.eat(TokenType.ASSIGN)
        expression = self.expr()
        node = Assignment(variable, expression)
        return node

    def declaration_statement(self):
        self.eat(TokenType.VARIABLE)
        variable = self.variable()
        self.eat(TokenType.ASSIGN)
        expression = self.expr()
        node = Declaration(variable, expression)
        return node

    def variable(self):
        node = Variable(self.current_token.value)
        self.eat(TokenType.IDENTIFIER)
        return node

    def empty(self):
        return Empty()

    def parse(self):
        node = self.program()
        if self.current_token.type != TokenType.END_OF_INPUT:
            self.error()
        return node

