import re
from typing import *

from src.utilities import highlight_span, check_output_file_path_not_exists, format_text


class RegexPattern():

    def __init__(self, pattern: str)->None:
        self.pattern = re.compile(rf'{pattern}')


    def find_pattern(self, texts: List[str])->List[List[re.Match]]:
        matches = [
            list(self.pattern.finditer(text))
            for text in texts
        ]
        return matches


    def _highlight_match(self, text: str, matches: List[re.Match])->str:
        for i, m in enumerate(matches):
            text = highlight_span(text, m.span(), i)
        return text


    def highlight_text(self, texts: List[str], matches: List[List[re.Match]])->str:
        message = f'''
        Matches for pattern \x1b[4;30;43m{self.pattern.pattern}\x1b[0m:\n
        '''
        for text, match in zip(texts, matches):
            highlight = self._highlight_match(text, match)
            message += format_text(highlight, '\t\t', '\n')
        return message


    def _generate_file_output(self, texts: List[str], matches: List[re.Match])->str:
        output = 'input,match,span_start,span_end\n'
        for text, match in zip(texts, matches):
            for m in match:
                output += f'{text},{m.group()},{m.start()},{m.end()}\n'
        return output


    def save_file(self, texts: List[str], matches: List[List[re.Match]], path: str)->None:
        path = check_output_file_path_not_exists(path)
        data = self._generate_file_output(texts, matches)
        with open(path, 'w') as f:
            _ = f.write(data)
            