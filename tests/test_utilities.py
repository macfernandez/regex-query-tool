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


#class MockOsPathExists():
#    def __init__(self, name, false_after: int=0) -> None:
#        self.counter = 0
#        self.false_after = false_after
#    def __call__(self, path:str):
#        called = self.counter
#        self.counter += 1
#        return called < self.false_after
#
#
#@pytest.fixture
#def mock_ask_overwrite(monkeypatch):
#    def _mock_ask_overwrite(path):
#        _mock = mock.Mock()
#        return _mock
#    monkeypatch.setattr(utilities, 'ask_overwrite', _mock_ask_overwrite)
#
#@pytest.fixture
#def mock_os_path_exists(monkeypatch, exists):
#    def _mock_os_path_exists(path):
#        _mock = mock.Mock()
#        _mock.side_effect = exists
#        return _mock
#    monkeypatch.setattr(utilities.os.path, 'exists', _mock_os_path_exists)

@mock.patch('os.path.exists', name='exists', return_value=False)
def test_given_non_existent_path_when_check_output_file_path_not_exists_runs_then_returns_same_path(
    exists
    ):
    assert utilities.check_output_file_path_not_exists('dummy_path') == 'dummy_path'


@mock.patch('os.path.exists', name='exists', return_value=True)
@mock.patch('src.utilities.ask_overwrite', name='overwrite', return_value=True)
def test_given_existent_path_when_check_output_file_path_not_exists_runs_then_returns_same_path_if_overwrite(
    exists, overwrite
    ):
    assert utilities.check_output_file_path_not_exists('dummy_path') == 'dummy_path'


@mock.patch('os.path.exists', name='exists', side_effect=[True, False])
@mock.patch('src.utilities.ask_overwrite', name='overwrite', return_value=False)
@mock.patch('src.utilities.ask_new_file_path', name='new_file_path', return_value='new_dummy_path')
def test_given_existent_path_when_check_output_file_path_not_exists_runs_then_returns_new_path_if_not_overwrite(
    exists, overwrite, new_file_path
    ):
    assert utilities.check_output_file_path_not_exists('dummy_path') == 'new_dummy_path'


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
