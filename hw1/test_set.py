import pytest


class TestSet:

    def test_set_1(self):
        x = {"i", "hate", "Mondays"}
        y = {"i", "love", "Sundays"}
        z = x.difference(y)
        assert len(z) == 2

    def test_set_2(self):
        x = {0, 1, 2, 3}
        y = {0, 1, 2, 3, 4, 5}
        assert y.issuperset(x)

    def test_set_3(self):
        set1 = {1, 2, 3}
        assert set1.pop() == 1 and set1 == {2, 3}

    def test_set_4(self):
        y = {1, 2}
        x = {'a', 'b'}
        assert y.isdisjoint(x)

    @pytest.mark.parametrize('x', set(range(5)))
    def test_set_5(self, x):
        assert x ** 0 == 1
