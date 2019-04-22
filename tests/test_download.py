from subtidal.download import download


def test_input():
    assert download('/Users/brenner/Movies/') == 0
