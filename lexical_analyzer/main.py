from lexical_analyzer.analyzer import Analyzer

FILENAME = "foo"
FILEDIR = "../input_files/"

with open(FILEDIR + FILENAME) as source:
    source_code = source.readlines()
    analyzer = Analyzer()
    print(analyzer.analyse(source_code))


