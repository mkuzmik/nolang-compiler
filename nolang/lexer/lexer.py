from nolang.lexer.analyzer import Analyzer


def tokenize(file):
    with open(file) as source:
        source_code = source.read()
        analyzer = Analyzer(source_code)
        return analyzer.gather_tokens()




