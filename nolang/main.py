from nolang.lexer.lexer import *
from nolang.parser.parser import *

tokens = tokenize("../input_files/parsing_sample.no")
parsed = Parser(tokens).parse()

print(parsed)