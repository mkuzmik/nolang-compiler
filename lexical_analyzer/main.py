from lexical_analyzer.analyzer import Analyzer
from lexical_analyzer.token import TokenType

FILENAME = "foo"
FILEDIR = "../input_files/"


def gather_tokens(analyzer):
    token = analyzer.next_token()
    if token.token_type == TokenType.END_OF_INPUT:
        return [token]

    return [token] + gather_tokens(analyzer)


with open(FILEDIR + FILENAME) as source:
    source_code = source.read()
    analyzer = Analyzer(source_code)
    tokens = gather_tokens(analyzer)
    print(tokens)




