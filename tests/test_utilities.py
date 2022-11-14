import pytest
from unittest import mock

from src import utilities


@mock.patch('os.path.exists',  return_value=True)
def test_given_path_when_check_input_file_path_exists_runs_then_returns_None_if_path_exists(mock_exists):
    assert utilities.check_file_path_exists('dummy_path') is None


@mock.patch('os.path.exists',  return_value=False)
def test_given_path_when_check_input_file_path_exists_runs_then_raises_FileNotFound_if_path_not_exists(mock_exists):
    path = 'dummy_path'
    with pytest.raises(FileNotFoundError, match=rf'File {path} not found.'):
        utilities.check_file_path_exists(path)


def test_given_path_when_check_output_file_path_not_exists_runs_then_returns_ ():
    assert True


@pytest.mark.parametrize('text, span, n_match, expected_string', [
    (
        'dummy string dummy',
        (0, 5),
        0,
        '\x1b[6;30;42mdummy\x1b[0m string dummy'
    ),
    (
        'dummy string dummy',
        (13, 18),
        0,
        'dummy string \x1b[6;30;42mdummy\x1b[0m'
    ),
    (
        '\x1b[6;30;42mdummy\x1b[0m string dummy',
        (13, 18),
        0,
        '\x1b[6;30;42mdum\x1b[6;30;42mmy\x1b[0\x1b[0mm string dummy'
    ),
    (
        'dummy string dummy',
        (0, 0),
        0,
        '\x1b[6;30;42m\x1b[0mdummy string dummy',
    )
])
def test_given_text_span_n_match_when_highlight_span_runs_then_returns_expected_string(
    text, span, n_match, expected_string
):
    assert utilities.highlight_span(text, span, n_match) == expected_string


@mock.patch('builtins.open', new_callable=mock.mock_open, read_data='dummy\ndata\nfor\ntesting')
def test_given_path_when_read_file_lines_runs_then_returns_extepected_lines(mock_open):
    assert utilities.read_file_lines('dummy_path') == ['dummy', 'data', 'for', 'testing']