from lexical_analyzer.analyzer import Analyzer


FILENAME = "sample.no"
FILEDIR = "../input_files/"

with open(FILEDIR + FILENAME) as source:
    source_code = source.read()
    analyzer = Analyzer(source_code)
    tokens = analyzer.gather_tokens()
    print(tokens)




