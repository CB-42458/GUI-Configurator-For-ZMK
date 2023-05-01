"""
Test the classes of the program file KeyCodes.py of the ZMK module.
"""

import unittest

import ZMK.KeyCodes as KeyCodes


class TestKeyCodesJSON(unittest.TestCase):
    """
    Test the class KeyCodesJSON
    """

    def test_iterate(self):
        """
        Test the __iter__ method of the KeyCodesJSON class.
        """
        for key in KeyCodes.KeyCodesJSON():
            self.assertIsInstance(key, str)

    def test_getitem(self):
        """
        Test the __getitem__ method of the KeyCodesJSON class.
        """
        for key in KeyCodes.KeyCodesJSON():
            self.assertIsInstance(KeyCodes.KeyCodesJSON()[key], dict)

    def test_contains(self):
        """
        Test the __contains__ method of the KeyCodesJSON class.
        """
        self.assertIn('A', KeyCodes.KeyCodesJSON())


class TestFunctionModifiersJSON(unittest.TestCase):
    """
    Test the class FunctionModifiersJSON
    """

    def test_iterate(self):
        """
        Test the __iter__ method of the FunctionModifiersJSON class.
        """
        for key in KeyCodes.FunctionModifiersJSON():
            self.assertIsInstance(key, str)

    def test_getitem(self):
        """
        Test the __getitem__ method of the FunctionModifiersJSON class.
        """
        for key in KeyCodes.FunctionModifiersJSON():
            self.assertIsInstance(KeyCodes.FunctionModifiersJSON()[key], dict)

    def test_contains(self):
        """
        Test the __contains__ method of the FunctionModifiersJSON class.
        """
        self.assertIn('LC(xx)', KeyCodes.FunctionModifiersJSON())


class TestKeyCode(unittest.TestCase):
    """
    Test the class KeyCode
    """

    def test_init_invalid_input(self):
        """
        Test the __init__ method of the KeyCode class.
        - giving an invalid name so a KeyError should be raised
        """
        self.assertRaises(KeyError, KeyCodes.KeyCode, 'invalid name')

    def test_init_invalid_input_type(self):
        """
        Test the __init__ method of the KeyCode class.
        - giving an invalid type so that a TypeError should be raised
        """
        self.assertRaises(TypeError, KeyCodes.KeyCode, 1)

    def test_build(self):
        """
        Test the build method of the KeyCode class.
        """
        build_output = {
            '.keymap': {
                'include': ['dt-bindings/zmk/keys.h'],
                'return' : 'A'
            }
        }
        self.assertIsInstance(KeyCodes.KeyCode('A').build(), dict)
        self.assertEqual(KeyCodes.KeyCode('A').build(), build_output)


class TestFunctionModifier(unittest.TestCase):
    """
    Test the class FunctionModifier
    """

    def test_init_invalid_name(self):
        """
        Test the __init__ method of the FunctionModifier class.
        - giving an invalid name so a KeyError should be raised
        """
        self.assertRaises(KeyError, KeyCodes.FunctionModifier, 'invalid name', 1)

    def test_init_invalid_name_type(self):
        """
        Test the __init__ method of the FunctionModifier class.
        - giving an invalid type so that a TypeError should be raised
        """
        self.assertRaises(TypeError, KeyCodes.FunctionModifier, 1, 1)

    def test_init_invalid_value_type(self):
        """
        Test the __init__ method of the FunctionModifier class.
        - giving an invalid type so that a TypeError should be raised
        """
        self.assertRaises(TypeError, KeyCodes.FunctionModifier, 'LC(xx)', '1')

    def test_build(self):
        """
        Test the build method of the FunctionModifier class.
        """
        build_output = {
            '.keymap': {
                'include': ['dt-bindings/zmk/keys.h'],
                'return' : 'LC(A)'
            }
        }
        self.assertIsInstance(KeyCodes.FunctionModifier('LC(xx)', KeyCodes.KeyCode('A')).build(), dict)
        self.assertEqual(KeyCodes.FunctionModifier('LC(xx)', KeyCodes.KeyCode('A')).build(), build_output)


class TestBluetoothKeyCode_without_parameter(unittest.TestCase):
    """
    Test the class BluetoothKeyCode without parameter
    """

    def test_init_invalid_name_type(self):
        """
        Test the __init__ method of the BluetoothKeyCode class.
        - giving an invalid type so that a TypeError should be raised
        """
        self.assertRaises(TypeError, KeyCodes.BluetoothKeyCode, 1)

    def test_init_invalid_name(self):
        """
        Test the __init__ method of the BluetoothKeyCode class.
        - giving an invalid name so a KeyError should be raised
        """
        self.assertRaises(KeyError, KeyCodes.BluetoothKeyCode, 'invalid name')

    def test_valid_init(self):
        """
        Test the __init__ method of the BluetoothKeyCode class.
        - giving a valid name
        """
        self.assertIsInstance(KeyCodes.BluetoothKeyCode('BT_CLR'), KeyCodes.BluetoothKeyCode)

    def test_build(self):
        """
        Test the build method of the BluetoothKeyCode class.
        """
        build_output = {
            '.keymap': {
                'include': ['dt-bindings/zmk/bt.h'],
                'return' : 'BT_CLR'
            }
        }
        self.assertIsInstance(KeyCodes.BluetoothKeyCode('BT_CLR').build(), dict)
        self.assertEqual(KeyCodes.BluetoothKeyCode('BT_CLR').build(), build_output)


class TestBluetoothKeyCode_with_parameter(unittest.TestCase):
    """
    Test the class BluetoothKeyCode with parameter
    """

    def test_init_invalid_name_type(self):
        """
        Test the __init__ method of the BluetoothKeyCode class.
        - giving an invalid type so that a TypeError should be raised
        """
        self.assertRaises(TypeError, KeyCodes.BluetoothKeyCode, 1, 1)

    def test_init_invalid_name(self):
        """
        Test the __init__ method of the BluetoothKeyCode class.
        - giving an invalid name so a KeyError should be raised
        """
        self.assertRaises(KeyError, KeyCodes.BluetoothKeyCode, 'invalid name', 1)

    def test_init_invalid_parameter_type(self):
        """
        Test the __init__ method of the BluetoothKeyCode class.
        - giving an invalid type so that a TypeError should be raised
        """
        self.assertRaises(TypeError, KeyCodes.BluetoothKeyCode, 'BT_SEL(xx)', '1')

    def test_init_invalid_parameter(self):
        """
        Test the __init__ method of the BluetoothKeyCode class.
        - giving an invalid parameter so that a ValueError should be raised
        """
        self.assertRaises(ValueError, KeyCodes.BluetoothKeyCode, 'BT_SEL(xx)', -1)

    def test_valid_init(self):
        """
        Test the __init__ method of the BluetoothKeyCode class.
        - giving a valid name
        """
        self.assertIsInstance(KeyCodes.BluetoothKeyCode('BT_SEL(xx)', 1), KeyCodes.BluetoothKeyCode)

    def test_build(self):
        """
        Test the build method of the BluetoothKeyCode class.
        """
        build_output = {
            '.keymap': {
                'include': ['dt-bindings/zmk/bt.h'],
                'return' : 'BT_SEL 1'
            }
        }
        self.assertIsInstance(KeyCodes.BluetoothKeyCode('BT_SEL(xx)', 1).build(), dict)
        self.assertEqual(KeyCodes.BluetoothKeyCode('BT_SEL(xx)', 1).build(), build_output)


class TestOutputKeyCode(unittest.TestCase):
    """
    Test the class OutputKeyCode
    """

    def test_init_invalid_name_type(self):
        """
        Test the __init__ method of the OutputKeyCode class.
        - giving an invalid type so that a TypeError should be raised
        """
        self.assertRaises(TypeError, KeyCodes.OutputKeyCode, 1)

    def test_init_invalid_name(self):
        """
        Test the __init__ method of the OutputKeyCode class.
        - giving an invalid name so a KeyError should be raised
        """
        self.assertRaises(KeyError, KeyCodes.OutputKeyCode, 'invalid name')

    def test_build(self):
        """
        Test the build method of the OutputKeyCode class.
        """
        build_output = {
            '.keymap': {
                'include': ['dt-bindings/zmk/outputs.h'],
                'return' : 'OUT_USB'
            }
        }
        self.assertIsInstance(KeyCodes.OutputKeyCode('OUT_USB').build(), dict)
        self.assertEqual(KeyCodes.OutputKeyCode('OUT_USB').build(), build_output)


if __name__ == '__main__':
    unittest.main()
