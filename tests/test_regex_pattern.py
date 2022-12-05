import pytest
from unittest.mock import Mock

from src.regex_pattern import *


@pytest.mark.parametrize('texts_list, n_items', [
    ([], 0),
    (['This is NOT a dummy pattern'], 1),
    (['This is a dummy_pattern'], 1),
    (['This is NOT a dummy pattern', 'This is a dummy_pattern'], 2),
    (['This is NOT a dummy pattern', 'dummy_pattern is a dummy_pattern'], 2)
])
def test_given_texts_list_when_find_pattern_runs_then_returns_expected_list_with_n_items(texts_list, n_items):
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
def test_given_texts_list_when_find_pattern_runs_then_returns_expected_list_with_lists_of_length(texts_list, lists_of_length):
    regex_pattern = RegexPattern('dummy_pattern')
    result = regex_pattern.find_pattern(texts_list)
    assert all([isinstance(r, list) for r in result])
    assert all([len(r) == i for r, i in zip(result, lists_of_length)])


@pytest.mark.parametrize('texts_list, span_matches', [
    (['This is a dummy_pattern'], [(10, 23)]),
    (['dummy_pattern is a dummy_pattern'], [(0, 13), (19, 32)])
])
def test_given_texts_list_when_find_pattern_runs_then_returns_expected_matches(texts_list, span_matches):
    regex_pattern = RegexPattern('dummy_pattern')
    result = regex_pattern.find_pattern(texts_list)
    assert all([isinstance(item, re.Match) for r in result for item in r])
    assert all([item.group() == 'dummy_pattern' for r in result for item in r])
    assert all([item.span() == s for r in result for item, s in zip(r,span_matches)])


@pytest.fixture
def mocked_match_list():
    def _mocked_match(spans):
        _matchs = list()
        for s in spans:
            _m = Mock()
            _m.span = Mock(return_value=s)
            _matchs.append(_m)
        return _matchs
    return _mocked_match

@pytest.mark.parametrize('text, spans', [
    ('This is NOT a dummy pattern', []),
    ('This is a dummy_pattern', [(10, 23)]),
    ('dummy_pattern is a dummy_pattern', [(0, 13), (19, 32)])
])
def test_given_texts_and_matches_when__highlight_match_runs_then_returns_expected_highlighted_text(mocked_match_list, text, spans):
    regex_pattern = RegexPattern('dummy_pattern')
    mocked_match_list = mocked_match_list(spans)
    assert regex_pattern._highlight_match(text, mocked_match_list)


def test_given_texts_and_matches_when_highlight_match_runs_then_returns_expected_message():
    pass
def test_given_texts_and_matches_when__generate_file_output_runs_then_returns_expected_text():
    pass
def test_given_texts_and_matches_when_save_file_runs_then_returns_None():
    pass




