import pytest


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

    @pytest.mark.parametrize('x, flag', [([1, 0, 2], True), ([0, 0, 2], False), ([1, 1, 1], True)])
    def test_list_4(self, x, flag):
        if flag:
            assert 1 in x
        else:
            assert 1 not in x

    def test_list_5(self):
        list1 = ["a", "b", "c"]
        list2 = ["d", "e", "f"]
        list1.extend(list2)
        assert len(list1) == 6
