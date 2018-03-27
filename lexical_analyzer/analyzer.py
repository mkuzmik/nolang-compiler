from lexical_analyzer.scanner_automaton import ScannerAutomaton
from lexical_analyzer.token import Token


class Analyzer:

    def __init__(self):
        self.token_array = []
        self.current_token_value = ""
        self.scanner = ScannerAutomaton()

    # source_code is an array of string (lines of code)
    def analyse(self, source_code):
        for line_number in range(len(source_code)):
            for column_number in range(len(source_code[line_number])):
                char = source_code[line_number][column_number]
                print("Scanning symbol: " + char)
                if not char.isspace():
                    self.current_token_value = self.current_token_value + char
                    self.scanner.push(char)
                else:
                    self.flush_token_and_reset_buffer()
        self.flush_token_and_reset_buffer()
        return self.token_array

    def flush_token_and_reset_buffer(self):
        self.token_array.append(Token(self.scanner.get_current_token_type(), self.current_token_value))
        self.current_token_value = ""
