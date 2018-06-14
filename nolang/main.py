from nolang.lexer.lexer import *
from nolang.parser.parser import *
from nolang.code_generator.generator import *


try:
    tokens = tokenize("../input_files/code_generation_sample.no")
    ast = Parser(tokens).parse()
    code = CodeGenerator(ast).generate()
    print(code)
except Exception as e:
    print(str(e))