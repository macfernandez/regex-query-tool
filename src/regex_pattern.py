import re
from typing import List

from src.utilities import highlight_span, check_output_file_path_not_exists


class RegexPattern():

    def __init__(self, pattern: str)->None:
        self.pattern = re.compile(rf'{pattern}')

    def find_all(self, texts: List[str])->List[re.Match]:
        matches = [list(self.pattern.finditer(t)) for t in texts]
        return matches

    def highlighted_match(self, texts: List[str], matches: List[re.Match])->str:
        message = f'\nMatches for pattern \x1b[4;30;43m{self.pattern.pattern}\x1b[0m:\n'
        for i, text in enumerate(texts):
            if matches[i]:
                for e, m in enumerate(matches[i]):
                    text = highlight_span(text, m.span(), e)
            message += f'\t- {text}\n'
        return message

    def _generate_file_output(self, texts: List[str], matches: List[re.Match])->str:
        output = 'input,match,span_start,span_end\n'
        for i, text in enumerate(texts):
                for m in matches[i]:
                    output += f'{text},{m.group()},{m.start()},{m.end()}\n'
        return output

    def save_file(self, texts: List[str], matches: List[re.Match], path: str)->None:
        path = check_output_file_path_not_exists(path)
        data = self._generate_file_output(texts, matches)
        with open(path, 'w') as f:
            _ = f.write(data)
            