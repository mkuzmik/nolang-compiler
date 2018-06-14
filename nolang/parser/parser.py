from nolang.parser.ast import *
from nolang.lexer.tokenz import *


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.current_token = self.tokens[self.current]

    def parse(self):
        node = self.program()
        if self.current_token.type != TokenType.END_OF_INPUT:
            self.error(TokenType.END_OF_INPUT)
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
            node = self.epsilon()
        return node

    def assignment(self):
        '''
        Assignment -> identifier '=' Expression ';'
        '''
        variable = self.identifier()
        self.eat(TokenType.ASSIGN)
        assignable = self.assignable()
        node = Assignment(variable, assignable)
        return node

    def var_declaration(self):
        '''
        VarDeclaration -> 'var' identifier = ';'
        '''
        self.eat(TokenType.VARIABLE)
        variable = self.identifier()
        self.eat(TokenType.ASSIGN)
        assignable = self.assignable()
        node = Declaration(variable, assignable)
        return node

    def print_statement(self):
        '''
        PrintStatement -> 'print' Expression ';'
        '''
        self.eat(TokenType.PRINT)
        expression = self.expression()
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
        Condition -> '(' Expression BooleanOperator Expression ')'
        '''
        self.eat(TokenType.LPAREN)
        left = self.expression()
        condition = self.current_token.value
        self.eat(TokenType.BINARY_OPERATOR)
        right = self.expression()
        self.eat(TokenType.RPAREN)
        node = Condition(condition, left, right)
        return node

    def assignable(self):
        '''
        Assignable -> Expression | boolean | string
        '''
        if (self.current_token.type == TokenType.BOOLEAN):
            return self.boolean()
        if (self.current_token.type == TokenType.STRING):
            return self.string()
        else:
            return self.expression()

    def expression(self):
        '''
        Expression -> Term (('+' | '-') Term)*
        '''
        node = self.term()

        while self.current_token.value in ('+', '-'):
            token = self.current_token
            self.eat(TokenType.BINARY_OPERATOR)
            node = BinaryOperation(token.value, node, self.term())

        return node

    def term(self):
        '''
        Term -> Factor (('*' | '/') Factor)*
        '''
        node = self.factor()

        while self.current_token.value in ('*', '/'):
            token = self.current_token
            self.eat(TokenType.BINARY_OPERATOR)

            node = BinaryOperation(token.value, node, self.factor())

        return node

    def factor(self):
        '''
        Factor -> number | identifier | '(' Expression ')'
        '''
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return NumberLiteral(token.value)

        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Identifier(token.value)

        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return node

        else:
            line = self.current_token.line + 1
            column = self.current_token.column + 1
            raise Exception("PARSER ERROR: Unexpected token " + self.current_token.value + " Expected number or identifier at line " + str(line) + " column " + str(column))

    def boolean(self):
        token = self.current_token
        self.eat(TokenType.BOOLEAN)
        return BooleanLiteral(token.value)

    def string(self):
        token = self.current_token
        self.eat(TokenType.STRING)
        return StringLiteral(token.value)

    def identifier(self):
        node = Identifier(self.current_token.value)
        self.eat(TokenType.IDENTIFIER)
        return node

    def epsilon(self):
        return Epsilon()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.next_token()
        else:
            self.error(token_type)

    def next_token(self):
        self.current += 1
        self.current_token = self.tokens[self.current]
        return self.current_token

    def error(self, expected_token_type):
        line = self.current_token.line
        column = self.current_token.line
        raise Exception("PARSER ERROR: Expected: " + str(expected_token_type) + ", but found: " + str(self.current_token.value) + " at line " + str(line) + " column " + str(column))



