"""
Test the Behaviours module
"""
import unittest

from ZMK import Behaviours
from ZMK.KeyCodes import KeyCode, FunctionModifier

class TestKeyPress(unittest.TestCase):
    def test_init_invalid_type(self):
        """
        Test the __init__ method of the KeyPress class.
        - giving an invalid type so a TypeError should be raised
        """
        self.assertRaises(TypeError, Behaviours.KeyPress, 1)

    def test_init_invalid_key(self):
        """
        Test the __init__ method of the KeyPress class.
        - giving an invalid key so a KeyError should be raised
        """
        with self.assertRaises(KeyError):
            Behaviours.KeyPress(KeyCode('invalid key'))

    def test_init_valid(self):
        """
        Test the __init__ method of the KeyPress class.
        - giving a valid key so no error should be raised
        """
        self.assertIsInstance(Behaviours.KeyPress(KeyCode('A')), Behaviours.KeyPress)

    def test_init_valid_with_modifier(self):
        """
        Test the __init__ method of the KeyPress class.
        - giving a valid key and modifier so no error should be raised
        """
        self.assertIsInstance(Behaviours.KeyPress(FunctionModifier('LC(xx)', KeyCode('A'))), Behaviours.KeyPress)

    def test_build(self):
        """
        Test the build method of the KeyPress class.
        """
        build_dict = {
            '.keymap': {
                'include': ['behaviors.dtsi', 'dt-bindings/zmk/keys.h'],
                'return' : '&kp A'
            }
        }
        self.assertIsInstance(Behaviours.KeyPress(KeyCode('A')).build(), dict)
        self.assertEqual(Behaviours.KeyPress(KeyCode('A')).build(), build_dict)


class TestMomentaryLayer(unittest.TestCase):
    """
    Test the class MomentaryLayer
    """

    def test_init_invalid_type(self):
        """
        Test the __init__ method of the MomentaryLayer class.
        - giving an invalid type so a TypeError should be raised
        """
        self.assertRaises(TypeError, Behaviours.MomentaryLayer, 'invalid type')

    def test_init_invalid_layer(self):
        """
        Test the __init__ method of the MomentaryLayer class.
        - giving an invalid layer so a KeyError should be raised
        """
        self.assertRaises(ValueError, Behaviours.MomentaryLayer, -1)

    def test_init_valid(self):
        """
        Test the __init__ method of the MomentaryLayer class.
        - giving a valid layer so no error should be raised
        """
        self.assertIsInstance(Behaviours.MomentaryLayer(1), Behaviours.MomentaryLayer)

    def test_build(self):
        """
        Test the build method of the MomentaryLayer class.
        """
        build_dict = {
            '.keymap': {
                'include': ['behaviors.dtsi'],
                'return' : '&mo 1'
            }
        }
        self.assertIsInstance(Behaviours.MomentaryLayer(1).build(), dict)
        self.assertEqual(Behaviours.MomentaryLayer(1).build(), build_dict)


class TestLayerTap(unittest.TestCase):
    """
    Test the class LayerTap
    """

    def test_init_invalid_layer_type(self):
        """
        Test the __init__ method of the LayerTap class.
        - giving an invalid type to parameter 'layer' so a TypeError should be raised
        """
        self.assertRaises(TypeError, Behaviours.LayerTap, 'invalid type', KeyCode('A'))

    def test_init_invalid_layer(self):
        """
        Test the __init__ method of the LayerTap class.
        - giving an invalid layer so a ValueError should be raised
        """
        self.assertRaises(ValueError, Behaviours.LayerTap, -1, KeyCode('A'))

    def test_init_invalid_key_type(self):
        """
        Test the __init__ method of the LayerTap class.
        - giving an invalid type to parameter 'key' so a TypeError should be raised
        """
        self.assertRaises(TypeError, Behaviours.LayerTap, 1, 'invalid type')

    def test_init_invalid_key(self):
        """
        Test the __init__ method of the LayerTap class.
        - giving an invalid key so a KeyError should be raised
        """
        with self.assertRaises(KeyError):
            Behaviours.LayerTap(1, KeyCode('invalid key'))

    def test_init_valid(self):
        """
        Test the __init__ method of the LayerTap class.
        - giving a valid layer and key so no error should be raised
        """
        self.assertIsInstance(Behaviours.LayerTap(1, KeyCode('A')), Behaviours.LayerTap)

    def test_init_valid_with_modifier(self):
        """
        Test the __init__ method of the LayerTap class.
        - giving a valid layer, key and modifier so no error should be raised
        """
        self.assertIsInstance(Behaviours.LayerTap(1, FunctionModifier('LC(xx)', KeyCode('A'))), Behaviours.LayerTap)

    def test_build(self):
        """
        Test the build method of the LayerTap class.
        """
        build_dict = {
            '.keymap': {
                'include': ['behaviors.dtsi', 'dt-bindings/zmk/keys.h'],
                'return' : '&lt 1 A'
            }
        }
        self.assertIsInstance(Behaviours.LayerTap(1, KeyCode('A')).build(), dict)
        self.assertEqual(Behaviours.LayerTap(1, KeyCode('A')).build(), build_dict)


class TestToggleLayer(unittest.TestCase):
    """
    Test the class ToggleLayer
    """

    def test_init_invalid_type(self):
        """
        Test the __init__ method of the ToggleLayer class.
        - giving an invalid type so a TypeError should be raised
        """
        self.assertRaises(TypeError, Behaviours.ToggleLayer, 'invalid type')

    def test_init_invalid_layer(self):
        """
        Test the __init__ method of the ToggleLayer class.
        - giving an invalid layer so a KeyError should be raised
        """
        self.assertRaises(ValueError, Behaviours.ToggleLayer, -1)

    def test_init_valid(self):
        """
        Test the __init__ method of the ToggleLayer class.
        - giving a valid layer so no error should be raised
        """
        self.assertIsInstance(Behaviours.ToggleLayer(1), Behaviours.ToggleLayer)

    def test_build(self):
        """
        Test the build method of the ToggleLayer class.
        """
        build_dict = {
            '.keymap': {
                'include': ['behaviors.dtsi'],
                'return' : '&tog 1'
            }
        }
        self.assertIsInstance(Behaviours.ToggleLayer(1).build(), dict)
        self.assertEqual(Behaviours.ToggleLayer(1).build(), build_dict)


class TestTransparent(unittest.TestCase):
    """
    Test the class Transparent
    """

    def test_build(self):
        """
        Test the build method of the Transparent class.
        """
        build_dict = {
            '.keymap': {
                'include': ['behaviors.dtsi'],
                'return' : '&trans'
            }
        }
        self.assertIsInstance(Behaviours.Transparent().build(), dict)
        self.assertEqual(Behaviours.Transparent().build(), build_dict)


class TestNoneBehaviour(unittest.TestCase):
    """
    Test the class NoneBehaviour
    """

    def test_build(self):
        """
        Test the build method of the NoneBehaviour class.
        """
        build_dict = {
            '.keymap': {
                'include': ['behaviors.dtsi'],
                'return' : '&none'
            }
        }
        self.assertIsInstance(Behaviours.NoneBehaviour().build(), dict)
        self.assertEqual(Behaviours.NoneBehaviour().build(), build_dict)


class TestReset(unittest.TestCase):
    """
    Test the class Reset
    """

    def test_build(self):
        """
        Test the build method of the Reset class.
        """
        build_dict = {
            '.keymap': {
                'include': ['behaviors.dtsi'],
                'return' : '&reset'
            }
        }
        self.assertIsInstance(Behaviours.Reset().build(), dict)
        self.assertEqual(Behaviours.Reset().build(), build_dict)


class TestBootloaderReset(unittest.TestCase):
    """
    Test the class BootloaderReset
    """

    def test_build(self):
        """
        Test the build method of the BootloaderReset class.
        """
        build_dict = {
            '.keymap': {
                'include': ['behaviors.dtsi'],
                'return' : '&bootloader'
            }
        }
        self.assertIsInstance(Behaviours.BootloaderReset().build(), dict)
        self.assertEqual(Behaviours.BootloaderReset().build(), build_dict)


class TestBluetooth(unittest.TestCase):
    """
    Test the class Bluetooth
    """


if __name__ == '__main__':
    unittest.main()
