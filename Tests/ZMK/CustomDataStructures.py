import unittest

from ZMK.CustomDataStructures import Array


class TestArray(unittest.TestCase):
    """
    Testing the custom array class to check if it works as intented
    """

    def test_array_init(self):
        """
        Testing the __init__ method to ensure that is works as intended
        """

        self.assertIsInstance(Array(), Array)
        self.assertIsInstance(Array([1, 2, 3]), Array)
        self.assertEqual(Array([1, 2, 3]), [1, 2, 3])

    def test_iter_method(self):
        """
        Testing the __iter__ method to ensure that is works as intended
        """
        test_array = [1, 2, 3]
        for i, item in enumerate(Array(test_array)):
            self.assertEqual(item, test_array[i])

    def test_insert(self):
        """
        Testing the insert method to ensure that is works as intended
        """
        test = [0, None, None, 3, None, 5, 6]
        test_array = Array()
        test_array.insert(0, 0)
        test_array.insert(3, 3)
        test_array.insert(5, 5)
        test_array.insert(6, 6)
        self.assertEqual(test_array, test)

    def test_setitem(self):
        """
        Testing the __setitem__ method to ensure that is works as intended
        """
        array_ = [0, None, None, "test", None, 5, 6]
        test_array = Array([0, None, None, 3, None, 5, 6])
        test_array[3] = "test"
        self.assertEqual(test_array, array_)

    def test_len(self):
        """
        Testing the __len__ method to ensure that is works as intended
        """
        self.assertEqual(len(Array()), 0)
        self.assertEqual(len(Array([1, 2, 3])), 3)

    def test_pop(self):
        """
        Testing the pop method to ensure that is works as intended
        """
        test_array = Array([0, 1, 2, 3, 4, 5])
        pop_test = test_array.pop()
        self.assertEqual(pop_test, 5)
        self.assertEqual(test_array, [0, 1, 2, 3, 4])
        test_array.pop(0)
        self.assertEqual(test_array, [1, 2, 3, 4])

    def test_delitem(self):
        """
        Testing the __delitem__ method to ensure that is works as intended
        """
        test_array = Array([0, 1, 2, 3, 4, 5])
        del test_array[0]
        self.assertEqual(test_array, [1, 2, 3, 4, 5])
        del test_array[4]
        self.assertEqual(test_array, [1, 2, 3, 4])
        del test_array[2]
        self.assertEqual(test_array, [1, 2, 4])

    def test_getitem(self):
        """
        Testing the __getitem__ method to ensure that is works as intended
        """
        test_array = Array([0, 1, 2, 3, 4])
        self.assertEqual(test_array[0], 0)
        self.assertEqual(test_array[2], 2)
        self.assertEqual(test_array[4], 4)

    def test_append(self):
        """
        Testing the append method to ensure that is works as intended
        """
        test_array = Array()
        test_array.append(0)
        test_array.append(1)
        test_array.append(2)
        test_array.append(3)
        test_array.append(4)
        self.assertEqual(test_array, [0, 1, 2, 3, 4])

    def test_clear(self):
        """
        Testing the clear method to ensure that is works as intended
        """
        test_array = Array([0, 1, 2, 3, 4])
        test_array.clear()
        self.assertEqual(test_array, [])

    def test_list(self):
        """
        Testing the list method to ensure that is works as intended
        """
        test_array = Array([0, 1, 2, 3, 4])
        self.assertEqual(list(test_array), [0, 1, 2, 3, 4])

    def test_get_item_with_key(self):
        """
        Testing the get item method with a key
        """
        test_array = Array([0, 1, 2, 3, 4])
        self.assertEqual(test_array[:], [0, 1, 2, 3, 4])
        self.assertEqual(test_array[1:], [1, 2, 3, 4])
        self.assertEqual(test_array[:3], [0, 1, 2])
        self.assertEqual(test_array[1:3], [1, 2])


if __name__ == '__main__':
    unittest.main()
