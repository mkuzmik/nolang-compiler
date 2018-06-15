from nolang.lexer.lexer import *
from nolang.parser.parser import *
from nolang.code_generator.generator import *


try:
    tokens = tokenize("../input_files/factorial.no")
    ast = Parser(tokens).parse()
    code = CodeGenerator(ast).generate()
    print(code)
    with open("../generated_files/out.py", "w") as out_file:
        out_file.write(code)
except Exception as e:
    print(str(e))