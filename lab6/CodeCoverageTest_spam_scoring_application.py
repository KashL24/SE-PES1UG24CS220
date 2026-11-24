from spam_scoring import score_message, classify, filter_inbox, inbox_status


def test_plain_message_scores_zero():
    assert score_message("hello there", False, 0) == 0


def test_spam_words_and_punctuation():
    assert score_message("FREE winner! prize, urgent. cash", False, 0) == 10


def test_uppercase_and_links():
    assert score_message("HELLO", False, 4) == 5


def test_one_link():
    assert score_message("hello", False, 1) == 1


def test_known_sender_discount():
    assert score_message("free prize", True, 0) == 1


def test_known_sender_clamped_to_zero():
    assert score_message("hello", True, 0) == 0


def test_classifications():
    assert classify(0) == "clean"
    assert classify(4) == "suspicious"
    assert classify(8) == "spam"


def test_filter_inbox_mixed():
    messages = [
        ("free winner prize urgent", False, 0),
        ("free prize", False, 0),
        ("hello", False, 0),
    ]
    assert filter_inbox(messages) == {"spam": 1, "suspicious": 1, "clean": 1}


def test_inbox_statuses():
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"
    assert inbox_status({"spam": 3, "suspicious": 0, "clean": 1}) == "flooded"
    assert inbox_status({"spam": 1, "suspicious": 1, "clean": 1}) == "noisy"
    assert inbox_status({"spam": 0, "suspicious": 1, "clean": 2}) == "healthy"
