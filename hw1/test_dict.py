import pytest


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
        assert "C" in x and "D1" in x

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
    def test_dict_5(self, x):
        assert "E" not in x
