class Compound:
    def __init__(self):
        self.children = []

class StatementSequence:
    def __init__(self):
        self.statements = []

    def add(self, statement):
        if (statement != None):
            self.statements.append(statement)

class WhileLoop:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class NumberLiteral:
    def __init__(self, value):
        self.value = value

class StringLiteral:
    def __init__(self, value):
        self.value = value

class Variable:
    def __init__(self, identifier):
        self.identifier = identifier

class Declaration:
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

class Assignment:
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

class BinaryOperation:
    def __init__(self, operation, expression1, expression2):
        self.operation = operation
        self.left = expression1
        self.right = expression2

class Empty:
    pass
