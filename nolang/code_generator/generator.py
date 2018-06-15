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
        self.declared_identifiers = []

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
        return block if len(block) > 0 else indent + "pass\n"

    def visit_PrintStatement(self, print_statement):
        return "print(" + self.visit(print_statement.argument) + ")"

    def visit_StringLiteral(self, string_literal):
        return "\"" + string_literal.value + "\""

    def visit_NumberLiteral(self, number_literal):
        return str(number_literal.value)

    def visit_BooleanLiteral(self, boolean_literal):
        return 'True' if (boolean_literal.value == 'true') else 'False'

    def visit_BinaryOperation(self, binary_operation):
        return self.visit(binary_operation.left) + binary_operation.operation + self.visit(binary_operation.right)

    def visit_Declaration(self, declaration):
        self.declared_identifiers.append(declaration.identifier.value)
        return self.visit(declaration.identifier) + '=' + self.visit(declaration.expression)

    def visit_Assignment(self, assignment):
        return self.visit(assignment.identifier) + '=' + self.visit(assignment.expression)

    def visit_Identifier(self, identifier):
        if (identifier.value not in self.declared_identifiers):
            identifier_not_declared(identifier.value)
        return str(identifier.value)

    def visit_IfStatement(self, if_statement):
        return 'if ' + self.visit(if_statement.condition) + ' :\n' + self.visit(if_statement.body)

    def visit_Condition(self, condition):
        return '(' + self.visit(condition.left) + ')' + condition.condition + '(' + self.visit(condition.right) + ')'

    def visit_WhileLoop(self, while_loop):
        return 'while ' + self.visit(while_loop.condition) + ':\n' + self.visit(while_loop.body)

    def visit_ReturnStatement(self, return_statement):
        return "return " + self.visit(return_statement.argument)

    def visit_FunctionDefinition(self, function_definition):
        self.declared_identifiers.append(function_definition.identifier.value)
        return "def " + self.visit(function_definition.identifier) + "(" + self.visit(function_definition.arguments) + "):\n" + self.visit(function_definition.body)

    def visit_Identifiers(self, identifiers):
        res = ""
        for child in identifiers.children:
            self.declared_identifiers.append(child.value)
            res += self.visit(child) + ","
        # remove lat comma
        return res[:-1]

    def visit_FunctionCall(self, function_call):
        res = self.visit(function_call.identifier) + "("
        args = ""
        for expr in function_call.arguments:
            args += self.visit(expr) + ","
        return res + args[:-1] + ")"


def identifier_not_declared(identifier):
    raise Exception('CODE GENERATION ERROR: Identifier \"' + identifier + '\" undefined')