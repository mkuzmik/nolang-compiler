from nolang.lexer.lexer import *
from nolang.parser.parser import *

tokens = tokenize("../input_files/parsing_sample.no")
parsed = parse(tokens)

print(parsed)