import random
import pytest
from spam_scoring import sender_domain, first_link, shout_ratio

# Dependency-free fallback: reproducible randomized and explicit edge cases.
def samples():
    rng = random.Random(7)
    yield from ('', None, '123 !!!', 'no link', 'a@@b', '\t', 42, [], {})
    alphabet = 'abcXYZ012@:/ .\t\nßé中'
    for _ in range(300):
        yield ''.join(rng.choice(alphabet) for _ in range(rng.randrange(40)))

def test_sender_domain():
    assert sender_domain('offers@Deals.com') == 'deals.com'
    for s in samples():
        result = sender_domain(s)
        assert isinstance(result, str)
        if not isinstance(s, str) or s.count('@') != 1:
            assert result == ''

def test_first_link():
    assert first_link('See https://example.com\tmore') == 'https://example.com'
    for s in samples():
        assert isinstance(first_link(s), str)
    assert first_link('http') == ''

def test_shout_ratio():
    assert shout_ratio('Aa') == 0.5
    for s in samples():
        assert 0 <= shout_ratio(s) <= 1
    assert shout_ratio('123 !!!') == 0.0
