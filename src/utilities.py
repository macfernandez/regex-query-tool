import os
from typing import List, Tuple


def ask_new_file_path()->str:
    return input('New path: ')


def ask_overwritte(path: str)->bool:
    overwritte = input(f'File {path} already exists. Overwritte? y/n: ')
    return overwritte in ['y','Y','']


def check_input_file_path_exists(path: str)->None:
    if not os.path.exists(path):
        raise FileNotFoundError(f'File {path} not found.')


def check_output_file_path_not_exists(path: str)->str:
    if os.path.exists(path):
        overwritte = ask_overwritte(path)
        if not overwritte:
            path = ask_new_file_path()
            path = check_output_file_path_not_exists(path)
    return path


def format_text(text: str, prefix: str, suffix: str):
    return f'{prefix}{text}{suffix}'


def highlight_span(text: str, span: Tuple[int], n_match: int)->str:
    '''
        Take a text, a span in that text and a number of previous highlighted
        spans and returns a new text with the current span highlighted.

        Parameters
        ----------
        text: str
        
        span: tuple

        n_match: int

        Return
        ------
        highlighted_span: str
            Text with span highlighted.

    '''
    scolor, ecolor = '\x1b[6;30;42m', '\x1b[0m'
    extra_chars = len(scolor) + len(ecolor)
    sspan = span[0] + (n_match*extra_chars)
    espan = span[1] + (n_match*extra_chars)
    highlighted_span = f'{text[:sspan]}{scolor}{text[sspan:espan]}{ecolor}{text[espan:]}'
    return highlighted_span


def read_file_lines(path: str)->List[str]:
    with open(path, 'r') as f:
        texts = list(map(str.strip,f.readlines()))
    return texts
