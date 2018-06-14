class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class CodeGenerator(NodeVisitor):

    def __init__(self, ast):
        self.ast = ast
        self.deep = 0
        self.declared_variables = []
        self.defined_functions = []

    def generate(self):
        return self.visit(self.ast)

    def visit_Compound(self, compound):
        block = ""
        indent = self.deep * 4 * " "
        for child in compound.children:
            self.deep += 1
            line = indent + self.visit(child)
            self.deep -= 1
            block = block + line + "\n"
        return block

    def visit_PrintStatement(self, print_statement):
        return "print(" + self.visit(print_statement.argument) + ")"

    def visit_StringLiteral(self, string_literal):
        return "\"" + string_literal.value + "\""

    def visit_NumberLiteral(self, number_literal):
        return str(number_literal.value)

    def visit_BinaryOperation(self, binary_operation):
        return self.visit(binary_operation.left) + binary_operation.operation + self.visit(binary_operation.right)

    def visit_Declaration(self, declaration):
        return self.visit(declaration.identifier) + '=' + self.visit(declaration.expression)

    def visit_Identifier(self, identifier):
        return str(identifier.value)

    def visit_IfStatement(self, if_statement):
        return 'if ' + self.visit(if_statement.condition) + ' :\n' + self.visit(if_statement.body)

    def visit_Condition(self, condition):
        return '(' + self.visit(condition.left) + ')' + condition.condition + '(' + self.visit(condition.right) + ')'
