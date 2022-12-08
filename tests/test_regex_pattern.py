import pytest
from unittest.mock import Mock, patch, mock_open, call

from src.regex_pattern import *


# FUXTURES --------

@pytest.fixture
def mocked_text_matchs():
    def _mocked_text_matchs(text_match):
        matchs = list()
        for group, span in text_match:
            _m = Mock()
            _m.group = Mock(return_value=group)
            _m.span = Mock(return_value=span)
            _m.start = Mock(return_value=span[0])
            _m.end = Mock(return_value=span[1])
            matchs.append(_m)
        return matchs
    return _mocked_text_matchs


@pytest.fixture
def mocked_texts_matchs(mocked_text_matchs):
    def _mocked_texts_matchs(texts_match):
        matchs = list()
        for tmatch in texts_match:
            text_matchs = mocked_text_matchs(tmatch)
            matchs.append(text_matchs)
        return matchs
    return _mocked_texts_matchs


@pytest.fixture
def expected_str_output():
    def _expected_str_output(prefix, content):
        return prefix + content
    return _expected_str_output

# TEST CASES ------

@pytest.mark.parametrize('texts_list, n_items', [
    ([], 0),
    (['This is NOT a dummy pattern'], 1),
    (['This is a dummy_pattern'], 1),
    (['This is NOT a dummy pattern', 'This is a dummy_pattern'], 2),
    (['This is NOT a dummy pattern', 'dummy_pattern is a dummy_pattern'], 2)
])
def test_given_texts_list_when_find_pattern_runs_then_returns_expected_list_with_n_items(
    texts_list, n_items
    ):
    regex_pattern = RegexPattern('dummy_pattern')
    result = regex_pattern.find_pattern(texts_list)
    assert isinstance(result, list)
    assert len(result) == n_items


@pytest.mark.parametrize('texts_list, lists_of_length', [
    (['This is NOT a dummy pattern'], [0]),
    (['This is a dummy_pattern'], [1]),
    (['This is NOT a dummy pattern', 'This is a dummy_pattern'], [0, 1]),
    (['This is NOT a dummy pattern', 'dummy_pattern is a dummy_pattern'], [0, 2])
])
def test_given_texts_list_when_find_pattern_runs_then_returns_expected_list_with_lists_of_length(
    texts_list, lists_of_length
    ):
    regex_pattern = RegexPattern('dummy_pattern')
    result = regex_pattern.find_pattern(texts_list)
    assert all([isinstance(r, list) for r in result])
    assert all([len(r) == i for r, i in zip(result, lists_of_length)])


@pytest.mark.parametrize('texts_list, span_matches', [
    (['This is a dummy_pattern'], [(10, 23)]),
    (['dummy_pattern is a dummy_pattern'], [(0, 13), (19, 32)])
])
def test_given_texts_list_when_find_pattern_runs_then_returns_expected_matches(
    texts_list, span_matches
    ):
    regex_pattern = RegexPattern('dummy_pattern')
    result = regex_pattern.find_pattern(texts_list)
    assert all([isinstance(item, re.Match) for r in result for item in r])
    assert all([item.group() == 'dummy_pattern' for r in result for item in r])
    assert all([item.span() == s for r in result for item, s in zip(r,span_matches)])


@pytest.mark.parametrize('text, spans', [
    ('This is NOT a dummy pattern', []),
    ('This is a dummy_pattern', [('dummy_pattern', (10, 23))]),
    ('dummy_pattern is a dummy_pattern', [('dummy_pattern', (0, 13)), ('dummy_pattern', (19, 32))])
])
def test_given_texts_and_matches_when__highlight_match_runs_then_returns_expected_highlighted_text(
    mocked_text_matchs, text, spans
    ):
    regex_pattern = RegexPattern('dummy_pattern')
    mocked_matchs = mocked_text_matchs(spans)
    assert regex_pattern._highlight_match(text, mocked_matchs)


@pytest.mark.parametrize('texts, spans, content', [
    (
        ['This is NOT a dummy pattern'],
        [[]],
        '\t\tThis is NOT a dummy pattern\n'
    ),
    (
        ['This is a dummy_pattern'],
        [[('dummy_pattern', (10, 23))]],
        '\t\tThis is a \x1b[6;30;42mdummy_pattern\x1b[0m\n'
    ),
    (
        ['This is NOT a dummy pattern', 'This is a dummy_pattern'],
        [[], [('dummy_pattern', (10, 23))]],
        '\t\tThis is NOT a dummy pattern\n\t\tThis is a \x1b[6;30;42mdummy_pattern\x1b[0m\n'
    ),
    (
        ['This is a dummy_pattern', 'dummy_pattern is a dummy_pattern'],
        [[('dummy_pattern', (10, 23))], [('dummy_pattern', (0, 13)), ('dummy_pattern', (19, 32))]],
        '\t\tThis is a \x1b[6;30;42mdummy_pattern\x1b[0m\n\t\t\x1b[6;30;42mdummy_pattern\x1b[0m is a \x1b[6;30;42mdummy_pattern\x1b[0m\n'
    )
])
def test_given_texts_and_matches_when_highlight_text_runs_then_returns_expected_message(
    mocked_texts_matchs, expected_str_output, texts, spans, content
    ):
    pattern = 'dummy_pattern'
    regex_pattern = RegexPattern(pattern)
    mocked_matchs = mocked_texts_matchs(spans)
    prefix = f'''
        Matches for pattern \x1b[4;30;43m{pattern}\x1b[0m:\n
        '''
    expected_message = expected_str_output(prefix, content)
    assert regex_pattern.highlight_text(texts, mocked_matchs) == expected_message

@pytest.mark.parametrize('texts, spans, content', [
    (
        ['This is NOT a dummy pattern'],
        [[]],
        'This is NOT a dummy pattern,None,None,None\n'
    ),
    (
        ['This is a dummy_pattern'],
        [[('dummy_pattern', (10, 23))]],
        'This is a dummy_pattern,dummy_pattern,10,23\n'
    ),
    (
        ['This is NOT a dummy pattern', 'This is a dummy_pattern'],
        [[], [('dummy_pattern', (10, 23))]],
        'This is NOT a dummy pattern,None,None,None\nThis is a dummy_pattern,dummy_pattern,10,23\n'
    ),
    (
        ['This is a dummy_pattern', 'dummy_pattern is a dummy_pattern'],
        [[('dummy_pattern', (10, 23))], [('dummy_pattern', (0, 13)), ('dummy_pattern', (19, 32))]],
        'This is a dummy_pattern,dummy_pattern,10,23\ndummy_pattern is a dummy_pattern,dummy_pattern,0,13\ndummy_pattern is a dummy_pattern,dummy_pattern,19,32\n'
    )
])
def test_given_texts_and_matches_when__generate_file_output_runs_then_returns_expected_text(
    mocked_texts_matchs, expected_str_output, texts, spans, content
):
    pattern = 'dummy_pattern'
    regex_pattern = RegexPattern(pattern)
    mocked_matchs = mocked_texts_matchs(spans)
    prefix = 'input,match,span_start,span_end\n'
    expected_message = expected_str_output(prefix, content)
    assert regex_pattern._generate_file_output(texts, mocked_matchs) == expected_message


@pytest.mark.parametrize('texts, spans, content', [
    (
        ['This is NOT a dummy pattern'],
        [[]],
        'This is NOT a dummy pattern,None,None,None\n'
    ),
    (
        ['This is a dummy_pattern'],
        [[('dummy_pattern', (10, 23))]],
        'This is a dummy_pattern,dummy_pattern,10,23\n'
    ),
    (
        ['This is NOT a dummy pattern', 'This is a dummy_pattern'],
        [[], [('dummy_pattern', (10, 23))]],
        'This is NOT a dummy pattern,None,None,None\nThis is a dummy_pattern,dummy_pattern,10,23\n'
    ),
    (
        ['This is a dummy_pattern', 'dummy_pattern is a dummy_pattern'],
        [[('dummy_pattern', (10, 23))], [('dummy_pattern', (0, 13)), ('dummy_pattern', (19, 32))]],
        'This is a dummy_pattern,dummy_pattern,10,23\ndummy_pattern is a dummy_pattern,dummy_pattern,0,13\ndummy_pattern is a dummy_pattern,dummy_pattern,19,32\n'
    )
])
def test_given_texts_and_matches_when_save_file_runs_then_saves_expected_content(
    mocked_texts_matchs, expected_str_output, texts, spans, content
    ):
    pattern = 'dummy_pattern'
    regex_pattern = RegexPattern(pattern)
    mocked_matchs = mocked_texts_matchs(spans)
    prefix = 'input,match,span_start,span_end\n'
    expected_message = expected_str_output(prefix, content)
    with patch('builtins.open', mock_open()) as mocked_file:
        dummy_path = 'dummy_path'
        regex_pattern.save_file(texts, mocked_matchs, dummy_path)
        mocked_file.assert_called_once_with(dummy_path, 'w')
        handle = mocked_file()
        handle.write.assert_called_once_with(expected_message)
