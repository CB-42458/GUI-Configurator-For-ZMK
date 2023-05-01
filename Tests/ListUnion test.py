"""
This program will test the ZMK module
"""
import unittest

from ListUnion import list_union


class TestListUnion(unittest.TestCase):
    def test_list_union_with_no_duplicates(self):
        expected_list = [1, 2, 3, 4, 5, 6]
        list_a = [1, 2, 3]
        list_b = [4, 5, 6]
        self.assertEqual(list_union(list_a, list_b), expected_list)

    def test_list_union_with_duplicates(self):
        expected_list = [1, 2, 3, 4, 5, 6]
        list_a = [1, 2, 3]
        list_b = [4, 5, 6, 1, 2, 3]
        self.assertEqual(list_union(list_a, list_b), expected_list)


if __name__ == '__main__':
    unittest.main()
