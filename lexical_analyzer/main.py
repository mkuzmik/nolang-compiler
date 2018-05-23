from lexical_analyzer.analyzer import Analyzer
from lexical_analyzer.token import TokenType

FILENAME = "foo"
FILEDIR = "../input_files/"

with open(FILEDIR + FILENAME) as source:
    source_code = source.read()
    analyzer = Analyzer(source_code)
    tokens = analyzer.gather_tokens()
    print(tokens)




