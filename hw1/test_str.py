import pytest


class TestStr:

    def test_str_1(self):
        a = "Meow"
        assert isinstance(a, str)

    def test_str_2(self):
        a = "air"
        b = "hair"
        assert a[0:3] == b[1:4]

    def test_str_3(self):
        a = 'cat'
        b = 'dog'
        assert len(a) == len(b)

    def test_str_4(self):
        text = 'the thunder'
        assert 'th' in text

    @pytest.mark.parametrize('x', ['a', 'ab', 'abc'])
    def test_str_5(self, x):
        assert len(x) >= 1
