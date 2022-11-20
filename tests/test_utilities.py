import pytest
from unittest import mock

from src import utilities


@mock.patch('builtins.input',  return_value='dummy_path')
def test_given_no_input_when_ask_new_file_path_runs_then_returns_user_string(dummy_input):
    assert utilities.ask_new_file_path() == 'dummy_path'


@mock.patch('builtins.input')
@pytest.mark.parametrize('user_input, expected_bool', [
    ('y', True),
    ('Y', True),
    ('', True),
    ('n', False),
    ('s', False),
    ('8', False)
])
def test_given_path_when_ask_overwrite_runs_then_returns_expected_bool(mock_input, user_input, expected_bool):
    mock_input.return_value = user_input
    assert utilities.ask_overwrite('dummy_path') == expected_bool


@mock.patch('os.path.exists',  return_value=True)
def test_given_path_when_check_input_file_path_exists_runs_then_returns_None_if_path_exists(mock_exists):
    assert utilities.check_input_file_path_exists('dummy_path') is None


@mock.patch('os.path.exists',  return_value=False)
def test_given_path_when_check_input_file_path_exists_runs_then_raises_FileNotFound_if_path_not_exists(mock_exists):
    path = 'dummy_path'
    with pytest.raises(FileNotFoundError, match=rf'File {path} not found.'):
        utilities.check_input_file_path_exists(path)


@mock.patch('os.path.exists')
@mock.patch('src.utilities.ask_overwrite')
@mock.patch('src.utilities.ask_new_file_path')
@pytest.mark.parametrize('path, path_exists, overwrite, new_path, expected_path', [
    ('dummy_path', [False], None, None, 'dummy_path'),
    ('dummy_path', [True], True, None, 'dummy_path'),
    ('dummy_path', [True], True, None, 'dummy_path'),
    ('dummy_path', [True], True, None, 'dummy_path'),
    #('dummy_path', [True, False], False, 'chicho', 'chicho') TODO: research how to test this case
])
def test_given_path_when_check_output_file_path_not_exists_runs_then_returns_expected_path(
    mock_exists, mock_overwirte, mock_new_file_path, path, path_exists, overwrite, new_path, expected_path
    ):
    mock_exists.side_effect = path_exists
    mock_overwirte.return_value = overwrite
    mock_new_file_path.return_value = new_path
    assert utilities.check_output_file_path_not_exists(path) == expected_path


@pytest.mark.parametrize('text, prefix, suffix, expected_string', [
    ('text', 'prefix-', '-suffix', 'prefix-text-suffix'),
    ('text', '', '-suffix', 'text-suffix'),
    ('text', 'prefix-', '', 'prefix-text'),
    ('', 'prefix-', '-suffix', 'prefix--suffix'),
    ('text', ' ', '-suffix', ' text-suffix'),
    ('text', 'prefix-', ' ', 'prefix-text '),
    (' ', 'prefix-', '-suffix', 'prefix- -suffix'),
])
def test_given_text_prefix_suffix_when_format_text_runs_then_returns_expected_string(
    text, prefix, suffix, expected_string
    ):
    assert utilities.format_text(text, prefix, suffix) == expected_string


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
