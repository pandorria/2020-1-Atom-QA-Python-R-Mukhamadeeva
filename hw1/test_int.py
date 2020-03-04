import pytest
import random


class TestInt:

    def test_int_1(self):
        x = 5
        y = 6
        assert x < y

    def test_int_2(self):
        a = 4589
        assert isinstance(a, int)

    def test_int_3(self):
        x = random.randrange(1, 5)
        y = random.randrange(5, 10)
        assert x != y

    @pytest.mark.parametrize('x', list(range(-5, 7)))
    def test_int_4(self, x):
        assert x > -6

    @pytest.mark.parametrize('x', list(range(-2, 2, 2)))
    @pytest.mark.parametrize('y', list(range(3, 7, 2)))
    def test_int_5(self, x, y):
        assert x != y
