import qleet


def test_version():
    assert isinstance(qleet.__version__, str), "qLEET version should be a string"
    assert (
        len(qleet.__version__.split(".")) == 3
    ), "Version number doesn't have 3 dot separated values"
