import argparse

from src.regex_pattern import RegexPattern
from src.utilities import check_input_file_path_exists, read_file_lines

parser = argparse.ArgumentParser(
    prog='Regex Query Tool', description='Tool for testing regex queries.'
)

parser.add_argument('pattern', help='Pattern for matching.')
parser.add_argument('input', help='Input for matching.')
parser.add_argument('--file', '-f', action='store_true', help='Input is a file path.')
parser.add_argument('--silent', '-s', action='store_true', help='Silent output.')
parser.add_argument('--output-file', '-o', default=None, help='File path for saving output.')
args = parser.parse_args()

pattern = RegexPattern(args.pattern)

if args.file:
    check_input_file_path_exists(args.input)
    texts = read_file_lines(args.input)

else:
    texts = [args.input]

matches = pattern.find_pattern(texts)

if not args.silent:
    output = pattern.highlight_text(texts, matches)
    print(output)

if args.output_file:
    pattern.save_file(texts, matches, args.output_file)
