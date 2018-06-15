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
        Compound -> '{' StatementList '}'
        '''
        self.eat(TokenType.LBRACKET)
        nodes = self.statement_list()
        self.eat(TokenType.RBRACKET)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        '''
        StatementList -> Statement Statement | Epsilon
        '''
        statement_list = []
        while self.current_token.type != TokenType.RBRACKET:
            node = self.statement()
            statement_list.append(node)

        return statement_list

    def statement(self):
        '''
          Statement -> Assignment | VarDeclaration | PrintStatement | WhileLoop | IfStatement | FunctionDefinition | FunctionCall ';' | ReturnStatement
        '''
        if self.current_token.type == TokenType.IDENTIFIER:
            if self.tokens[self.current + 1].type == TokenType.LPAREN:
                node = self.function_call()
                self.eat(TokenType.END_OF_STATEMENT)
            else:
                node = self.assignment()
        elif self.current_token.type == TokenType.VARIABLE:
            node = self.var_declaration()
        elif self.current_token.type == TokenType.PRINT:
            node = self.print_statement()
        elif self.current_token.type == TokenType.WHILE:
            node = self.while_loop()
        elif self.current_token.type == TokenType.IF:
            node = self.if_statement()
        elif self.current_token.type == TokenType.FUNCTION:
            node = self.function_definition()
        elif self.current_token.type == TokenType.RETURN:
            node = self.return_statement()
        else:
            line = self.current_token.line + 1
            column = self.current_token.column + 1
            raise Exception("PARSER ERROR: Unexpected token " + self.current_token.value + " Expected STATEMENT at line " + str(line) + " column " + str(column))
        return node

    def assignment(self):
        '''
        Assignment -> identifier '=' Expression ';'
        '''
        variable = self.identifier()
        self.eat(TokenType.ASSIGN)
        assignable = self.assignable()
        self.eat(TokenType.END_OF_STATEMENT)
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
        self.eat(TokenType.END_OF_STATEMENT)
        node = Declaration(variable, assignable)
        return node

    def print_statement(self):
        '''
        PrintStatement -> 'print' Expression ';'
        '''
        self.eat(TokenType.PRINT)
        expression = self.assignable()
        self.eat(TokenType.END_OF_STATEMENT)
        node = PrintStatement(expression)
        return node

    def if_statement(self):
        '''
        IfStatement -> 'if' Condition Compound
        '''
        self.eat(TokenType.IF)
        condition_exp = self.condition()
        body = self.compound()
        node = IfStatement(condition_exp, body)
        return node

    def while_loop(self):
        '''
        WhileLoop -> 'while' Condition Compound
        '''
        self.eat(TokenType.WHILE)
        condition_exp = self.condition()
        body = self.compound()
        node = WhileLoop(condition_exp, body)
        return node

    def function_definition(self):
        '''
        FunctionDefinition -> 'function' identifier ArgumentsList Compound ';'
        '''
        self.eat(TokenType.FUNCTION)
        identifier = self.identifier()
        arguments = self.identifiers()
        body = self.compound()
        node = FunctionDefinition(identifier, arguments, body)
        return node

    def identifiers(self):
        '''
        Identifiers -> '(' IdentifierList ')'
        '''
        self.eat(TokenType.LPAREN)
        idents = Identifiers()
        idents.children = self.identifier_list()
        self.eat(TokenType.RPAREN)
        return idents

    def identifier_list(self):
        '''
        IdentifiersList -> identifier | identifier ',' IdentifierList
        '''
        identifiers = []
        while self.current_token.type == TokenType.IDENTIFIER:
            token = self.current_token
            self.eat(TokenType.IDENTIFIER)
            identifiers.append(Identifier(token.value))
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
            else:
                return identifiers
        return identifiers

    def return_statement(self):
        '''
        ReturnStatement-> 'return' Expression ';'
        '''
        self.eat(TokenType.RETURN)
        expression = self.expression()
        self.eat(TokenType.END_OF_STATEMENT)
        node = ReturnStatement(expression)
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
        Factor -> numberLiteral | identifier | FunctionCall | '(' Expression ')'
        '''
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return NumberLiteral(token.value)

        elif token.type == TokenType.IDENTIFIER:
            if self.tokens[self.current + 1].type == TokenType.LPAREN:
                return self.function_call()
            else:
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
            raise Exception("PARSER ERROR: Unexpected token " + self.current_token.value + " Expected NUMBER or IDENTIFIER at line " + str(line) + " column " + str(column))

    def function_call(self):
        '''
        FunctionCall -> identifier '(' ArgumentsList ')'
        '''
        identifier = Identifier(self.current_token.value)
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.LPAREN)
        arguments = self.arguments_list()
        self.eat(TokenType.RPAREN)
        return FunctionCall(identifier, arguments)

    def arguments_list(self):
        '''
        ArgumentsList -> Assignable | Assignable ',' ArgumentsList
        '''
        assigns = []
        while self.current_token.type != TokenType.RPAREN:
            assigns.append(self.assignable())
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
            else:
                return assigns
        return assigns

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
        line = self.current_token.line + 1
        column = self.current_token.line + 1
        raise Exception("PARSER ERROR: Expected: " + str(expected_token_type) + ", but found: " + str(self.current_token.value) + " at line " + str(line) + " column " + str(column))



