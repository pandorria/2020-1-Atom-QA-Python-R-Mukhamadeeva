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

    @pytest.mark.parametrize('x', list(range(-5, 7, 2)))
    def test_int_4(self, x):
        assert x > -6

    @pytest.mark.parametrize('x', list(range(-2, 2, 2)))
    @pytest.mark.parametrize('y', list(range(-2, 2, 2)))
    def test_int_4(self, x, y):
        assert x != y


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

    @pytest.mark.parametrize('x', ['a', 'b', 'cd'])
    def test_str_5(self, x):
        assert len(x) == 1


class TestList:

    def test_list_1(self):
        list1 = ['hop', 'hey']
        list2 = ['hey']
        del list1[0]
        assert list1 == list2

    def test_list_2(self):
        list1 = ["la", "la", "lend"]
        list1.clear()
        list2 = []
        assert list1 == list2

    def test_list_3(self):
        x = ['small', 'medium', 'large']
        assert x[0] != x[2]

    @pytest.mark.parametrize('x', [[1, 0, 1], [1, 0, 2], [1, 0, 3]])
    def test_list_4(self, x):
        assert 1 in x

    def test_list_5(self):
        list1 = ["a", "b", "c"]
        list2 = ["d", "e", "f"]
        list1.extend(list2)
        assert len(list1) == 6


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


class TestDict:

    def test_dict_1(self):
        x = {
            "A": 5,
            "B": 4,
            "C": 4,
            "D1": 4,
            "D2": 3,
            "F": 2,
        }
        assert x["C"] == 4

    def test_dict_2(self):
        x = {
            "A": 5,
            "B": 4,
            "C": 4,
            "D1": 4,
            "D2": 3,
            "F": 2,
        }
        assert "C", "D1" in x

    def test_dict_3(self):
        x = {
            "A": 5,
            "B": 4,
            "C": 4,
            "D1": 4,
            "D2": 3,
            "F": 2,
        }
        assert len(x) == 6

    def test_dict_4(self):
        x = {
            "A": 5,
            "B": 4,
            "C": 4,
            "D1": 4,
            "D2": 3,
            "F": 2,
        }
        assert x["D1"] != x["D2"]

    @pytest.mark.parametrize('x', [{
        "A": 5,
        "B": 4,
        "C": 4,
        "D1": 4,
        "D2": 3,
        "F": 2,
    }, {"B": 4}])
    def test_dict_4(self, x):
        assert x["B"] == 4
