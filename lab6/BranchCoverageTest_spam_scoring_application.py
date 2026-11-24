from spam_scoring import score_message, classify, filter_inbox, inbox_status


def test_no_words_no_links_unknown_sender():
    assert score_message("", False, 0) == 0


def test_spam_words_case_and_punctuation():
    assert score_message("FREE winner! prize, urgent. cash", False, 0) == 10


def test_uppercase_non_spam_word():
    assert score_message("HELLO", False, 0) == 1


def test_short_uppercase_word_not_counted():
    assert score_message("WOW", False, 0) == 0


def test_lowercase_non_spam_word_not_counted():
    assert score_message("hello", False, 0) == 0


def test_many_links():
    assert score_message("hello", False, 4) == 4


def test_few_links_boundary():
    assert score_message("hello", False, 3) == 1


def test_known_sender_positive_score():
    assert score_message("free prize", True, 0) == 1


def test_known_sender_score_clamped():
    assert score_message("hello", True, 0) == 0


def test_classify_boundaries():
    assert classify(3) == "clean"
    assert classify(4) == "suspicious"
    assert classify(7) == "suspicious"
    assert classify(8) == "spam"


def test_filter_empty_inbox():
    assert filter_inbox([]) == {"spam": 0, "suspicious": 0, "clean": 0}


def test_filter_all_categories():
    messages = [
        ("free winner prize urgent", False, 0),
        ("free prize", False, 0),
        ("hello", False, 0),
    ]
    assert filter_inbox(messages) == {"spam": 1, "suspicious": 1, "clean": 1}


def test_inbox_status_empty():
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"


def test_inbox_status_flooded():
    assert inbox_status({"spam": 3, "suspicious": 0, "clean": 1}) == "flooded"


def test_inbox_status_noisy():
    assert inbox_status({"spam": 1, "suspicious": 1, "clean": 1}) == "noisy"


def test_inbox_status_healthy():
    assert inbox_status({"spam": 0, "suspicious": 1, "clean": 2}) == "healthy"
