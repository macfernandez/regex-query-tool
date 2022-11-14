import argparse

from src.regex_pattern import RegexPattern
from src.utilities import check_input_file_path_exists, read_file_lines

parser = argparse.ArgumentParser(
    prog='Regex Query Tool', description='Tool for testing regex queries.'
)

parser.add_argument('pattern', help='Pattern for matching.')
parser.add_argument('--silent', '-s', action='store_true', help='Silent output.')
parser.add_argument('--output-file', '-o', default=None, help='File path for saving output.')

subparser = parser.add_subparsers(dest='input')
prompt_subpars = subparser.add_parser('prompt')
prompt_subpars.add_argument('texts', action='store', nargs='+', help='Input for matching.')
file_subpars = subparser.add_parser('file')
file_subpars.add_argument('file_path')

args = parser.parse_args()

pattern = RegexPattern(args.pattern)

if args.input == 'prompt':
    texts = args.texts

elif args.input == 'file':
    check_input_file_path_exists(args.file_path)
    texts = read_file_lines(args.file_path)

match = pattern.find_all(texts)
if not args.silent:
    output = pattern.hightlight_match(texts, match)
    print(output)

if args.output_file:
    pattern.save_file(texts, match, args.output_file)
