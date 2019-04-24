from subtidal.download import download


def test_input():
    assert download('nonexistent directory') == 0
