from nolang.lexer.lexer import *
from nolang.parser.parser import *

try:
    tokens = tokenize("../input_files/parsing_sample.no")
    parsed = Parser(tokens).parse()

    # TODO code generator
    print(parsed)
except Exception as e:
    print(str(e))