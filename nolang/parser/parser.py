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

    def error(self, expected_token_type):
        line = self.current_token.line
        column = self.current_token.line
        raise Exception("PARSER ERROR: Expected: " + str(expected_token_type) + ", but found: " + str(self.current_token.value) + " at line " + str(line) + " column " + str(column))

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.next_token()
        else:
            self.error(token_type)

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

        elif token.type == TokenType.BOOLEAN:
            self.eat(TokenType.BOOLEAN)
            return BooleanLiteral(token.value)

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
        '''
        Program -> Compound
        '''
        node = self.compound()
        return node

    def compound(self):
        '''
        Compound -> '{' Statement '}'
        '''
        self.eat(TokenType.LBRACKET)
        nodes = self.statement_seq()
        self.eat(TokenType.RBRACKET)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_seq(self):
        '''
        StatementSeq -> Statement Statement | Epsilon
        '''
        node = self.statement()
        res = [node]
        while self.current_token.type == TokenType.END_OF_STATEMENT:
            self.eat(TokenType.END_OF_STATEMENT)
            res.append(self.statement())

        if self.current_token.type == TokenType.IDENTIFIER:
            self.error()

        return res

    def statement(self):
        '''
        Statement -> Assignment | VarDeclaration | PrintStatement | WhileLoop | IfStatement
        '''
        if self.current_token.type == TokenType.IDENTIFIER:
            node = self.assignment()
        elif self.current_token.type == TokenType.VARIABLE:
            node = self.var_declaration()
        elif self.current_token.type == TokenType.PRINT:
            node = self.print_statement()
        elif self.current_token.type == TokenType.WHILE:
            node = self.while_loop()
        elif self.current_token.type == TokenType.IF:
            node = self.if_statement()
        else:
            node = self.empty()
        return node

    def assignment(self):
        '''
        Assignment -> identifier '=' Expression ';'
        '''
        variable = self.variable()
        self.eat(TokenType.ASSIGN)
        expression = self.expr()
        node = Assignment(variable, expression)
        return node

    def var_declaration(self):
        '''
        VarDeclaration -> 'var' identifier = ';'
        '''
        self.eat(TokenType.VARIABLE)
        variable = self.variable()
        self.eat(TokenType.ASSIGN)
        expression = self.expr()
        node = Declaration(variable, expression)
        return node

    def print_statement(self):
        '''
        PrintStatement -> 'print' Expression ';'
        '''
        self.eat(TokenType.PRINT)
        expression = self.expr()
        node = PrintStatement(expression)
        return node

    def if_statement(self):
        '''
        IfStatement -> 'if' Condition Compound ';'
        '''
        self.eat(TokenType.IF)
        condition_exp = self.condition()
        body = self.compound()
        node = IfStatement(condition_exp, body)
        return node

    def while_loop(self):
        '''
        WhileLoop -> 'while' Condition Compound ';'
        '''
        self.eat(TokenType.WHILE)
        condition_exp = self.condition()
        body = self.compound()
        node = WhileLoop(condition_exp, body)
        return node

    def condition(self):
        '''
        TODO grammar for condition
        '''
        self.eat(TokenType.LPAREN)
        left = self.expr()
        condition = self.current_token.value
        self.eat(TokenType.BINARY_OPERATOR)
        right = self.expr()
        self.eat(TokenType.RPAREN)
        node = Condition(condition, left, right)
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

