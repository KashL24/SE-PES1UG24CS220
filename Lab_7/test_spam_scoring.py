from hypothesis import given, strategies as st, settings, example
from spam_scoring import sender_domain, first_link, shout_ratio

inputs = st.one_of(st.text(), st.none(), st.integers(), st.lists(st.integers()))

@settings(max_examples=300)
@given(inputs)
@example('')
@example(None)
@example('a@@b')
def test_sender_domain_no_crash(s):
    result = sender_domain(s)
    assert isinstance(result, str)
    if not isinstance(s, str) or s.count('@') != 1:
        assert result == ''
    else:
        local, domain = s.strip().split('@')
        expected = domain.lower() if local and domain and not any(c.isspace() for c in local + domain) else ''
        assert result == expected

@settings(max_examples=300)
@given(inputs)
@example('')
@example(None)
@example('See https://example.com\tmore')
def test_first_link_no_crash(s):
    result = first_link(s)
    assert isinstance(result, str)
    if result:
        assert result.startswith(('http://', 'https://'))
        assert result in s
        assert not any(c.isspace() for c in result)
    if not isinstance(s, str):
        assert result == ''

@settings(max_examples=300)
@given(inputs)
@example('123 !!!')
@example(None)
@example('Aa')
def test_shout_ratio_no_crash(s):
    result = shout_ratio(s)
    assert 0.0 <= result <= 1.0
    letters = [c for c in s if c.isalpha()] if isinstance(s, str) else []
    expected = sum(c.isupper() for c in letters) / len(letters) if letters else 0.0
    assert result == expected
