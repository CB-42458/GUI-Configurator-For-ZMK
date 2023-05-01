"""
This is the main.py program which is to be run
"""
from __future__ import annotations

import math

# kivy imports
from kivy import metrics
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.scatter import Scatter
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.stacklayout import StackLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
import wx
# noinspection SpellCheckingInspection
import pykle_serial as pykle
import ZMK

# imports for the application
import standard_widgets as std
import functions as func

DEBUG_MODE = True
"""Boolean which will allow the print_debug function to print debug messages to the console if set to True"""
SHOW_ON_PARENT_DEBUG = False
"""Boolean condition for the print_debug which will allow "ON PARENT" messages to be printed if set to True"""


def print_debug(*args, **kwargs):
    """
    Function is used to print debug messages to the console

    @param args: objects which can be converted to strings
    @param kwargs: keyword arguments
    """
    if "info" in kwargs:
        if kwargs["info"] == "ON PARENT" and not SHOW_ON_PARENT_DEBUG:
            return
    if not DEBUG_MODE:
        return
    elif "info" in kwargs:
        info = kwargs["info"]
        del kwargs["info"]
        print("\033[1;31mDEBUG_PRINT |\033[1;32m", info, "|\033[0;37m", *args, **kwargs)
    else:
        print("\033[1;31mDEBUG_PRINT |\033[0m", *args, **kwargs)


def select_directory_dialog(prompt: str = "Select a directory") -> str:
    """
    uses the wxPython library to use the file explorer dialog to select a directory

    @param prompt: prompt which is displayed at the top of the dialog
    @return: a string to the path

    used https://docs.wxpython.org/wx.DirDialog.html for reference
    """
    # noinspection PyUnusedLocal
    app = wx.App()
    directory_dialog = wx.DirDialog(None, prompt)
    directory_dialog.ShowModal()
    path = directory_dialog.GetPath()
    if path == "":
        path = None
    directory_dialog.Destroy()
    return path


def select_file_dialog(prompt: str = "Select a file", wildcard: str = "") -> str:
    """
    uses the wxPython library to use the file explorer dialog to select a file
    used https://docs.wxpython.org/wx.FileDialog.html for reference

    @param prompt: prompt which is displayed at the top of the dialog
    @param wildcard: wildcard parameter is used to filter which files are shown and accepted
    @return: a string to the path
    """
    # noinspection PyUnusedLocal
    app = wx.App()
    file_dialog = wx.FileDialog(None, prompt, wildcard=wildcard)
    file_dialog.ShowModal()
    path = file_dialog.GetPath()
    file_dialog.Destroy()
    return path


def find_id(parent: Widget, widget: Widget) -> str:
    """
    function finds the id of the widget in the parent widget's ids dictionary

    @param parent: the parent widget
    @param widget: widget to find the id of
    @return: the id of the widget in the ids of the parent widget
    @deprecated: this function is planned to be removed
    """
    for key, value in parent.ids.items():
        if value == widget:
            return key
    return ""


class MCUSelectionScreen(Screen):
    """
    The MCU selection screen allows the user to select the MCU they would like to use for their keyboard
    """




    class MCUButton(Button):
        """
        MCUButton is a button which is used to select the MCU
        """

        def __init__(self, mcu_class: ZMK.MCUs.AbstractMCU, **kwargs):
            """
            @param mcu_class: the class of the MCU
            @param kwargs: keyword arguments
            """
            super().__init__(**kwargs)
            self.size_hint_y = None
            self.height = std.STD_BUTTON_HEIGHT * 1.5
            self.size_hint_x = 0.25
            self.font_size = std.STD_FONT_SIZE
            self.McuClass = mcu_class

        def on_release(self):
            """
            on_release is called when the button is released
            """
            main_window: MainWindow = App.get_running_app().root
            try:
                print_debug(f"MCUButton.on_release: {self.McuClass}")
                main_window.zmk_config.set_mcu(self.McuClass)
            except TypeError as error:
                main_window.zmk_error(error)
            main_window.screen_manager.current = "Properties"
            properties_screen: PropertiesScreen = main_window.screen_manager.get_screen("Properties")
            properties_screen.update_mcu_text()




    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stack_layout = StackLayout(size_hint=(1, 1), orientation="tb-lr", spacing=std.STD_SPACING * 2,
                                        padding=std.STD_SPACING * 2)
        """StackLayout is used for this screen as it allows to create list of buttons"""
        self.add_widget(self.stack_layout)
        # gets the list of the MCUs which have been implemented in the ZMK package
        self.mcu_list = [_class for _class in ZMK.MCUs.__dict__.values() if
                         isinstance(_class, type) and issubclass(_class, ZMK.MCUs.AbstractMCU)
                         and _class != ZMK.MCUs.AbstractMCU]
        """list of the MCUs which have been implemented in the ZMK package"""

    def on_parent(self, widget: MCUSelectionScreen, parent: ScreenManager):
        """
        on_parent is called when this widget is added to a parent widget

        @param widget: self
        @param parent: parent widget, ScreenManager
        """
        print_debug(f"{self.__class__.__name__}: {widget} {parent}", info="ON PARENT")
        if not self.stack_layout.children and parent:
            self.create_mcu_buttons()

    def create_mcu_buttons(self):
        """
        Creates the buttons for the MCU selection screen which allow the user to select the MCU for their keyboard
        """
        for mcu in self.mcu_list:
            print_debug(f"MCUSelectionScreen.create_mcu_buttons: {mcu}")
            button = self.MCUButton(text=str(mcu.__name__), mcu_class=mcu())
            self.stack_layout.add_widget(button)


class PropertiesScreen(Screen):
    """
    Properties screen manages the main properties of the ZMK config
    such as:
        - working directory
        - keyboard name
        - layout from the keyboard layout editor json file
        - the microcontroller unit
        - whether the keyboard is a split keyboard and which side is the main side
        - number of paired and simultaneous connections
        - whether rotary encoders are used and if so how many
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box_layout = BoxLayout(size_hint=(1, 1), orientation="vertical", spacing=std.STD_SPACING)
        """BoxLayout is used to create a vertical list of properties"""
        self.add_widget(self.box_layout)

    def on_parent(self, widget: PropertiesScreen, parent: ScreenManager):
        """
        on_parent is called when this widget is added to a parent widget

        @param widget: self
        @param parent: parent widget, ScreenManager
        """
        print_debug(f"{self.__class__.__name__}: {widget} {parent}", info="ON PARENT")

        # if there is a parent and the widgets have not been initialized
        # each widget which has intended user interaction has its id set to the self.box_layout.ids dictionary
        # as quick access for other parts of the program.
        # additionally these widgets have callback methods that are called when the user has made a change, which have
        # a callback method in the MainWindow class.
        if not self.box_layout.children and parent:
            # ========================================
            # Properties Screen: Working directory property

            box_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=std.STD_ROW_HEIGHT,
                                   spacing=std.STD_SPACING)
            # text label describing the property
            box_layout.add_widget(std.ConfigPropertyLabel(text="Working Directory:"))
            # text label to display the path to the working directory
            widget = std.ConfigPropertyLabel(text="", markup=True, size_hint_x=0.5, halign="left", max_lines=1)
            # widget added to the dictionary for easy access from the MainWindow class
            self.box_layout.ids["working directory"] = widget
            box_layout.add_widget(widget)
            self.update_directory_path()
            # button to open the file explorer dialog
            widget = Button(text="Select Directory", font_size=std.STD_PAGE_FONT_SIZE, size_hint_x=None,
                            width=metrics.sp(200))
            # bind the button to the callback
            widget.bind(on_release=self.on_select_working_directory)
            # add the widget to the dictionary
            self.box_layout.ids["select directory"] = widget
            # add the widget to the layout and add the layout to the main layout
            box_layout.add_widget(widget)
            self.box_layout.add_widget(box_layout)

            # ========================================
            # Properties Screen: Configuration name property

            box_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=std.STD_ROW_HEIGHT,
                                   spacing=std.STD_SPACING)
            # text label describing the property
            box_layout.add_widget(std.ConfigPropertyLabel(text="Configuration Name:"))
            # text input for the configuration name
            widget = TextInput(text="", font_size=std.STD_PAGE_FONT_SIZE, multiline=False)
            # bind the text input to the callback
            widget.bind(focus=self.on_config_name_focus)
            # add the widget to the dictionary
            self.box_layout.ids["configuration name"] = widget
            # add the widget to the layout and add the layout to the main layout
            box_layout.add_widget(widget)
            self.box_layout.add_widget(box_layout)

            # ========================================
            # configuration ID property
            box_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=std.STD_ROW_HEIGHT,
                                   spacing=std.STD_SPACING)
            # text label describing the property
            box_layout.add_widget(std.ConfigPropertyLabel(text="Configuration ID:"))
            # text input for the configuration ID
            widget = TextInput(text="", font_size=std.STD_PAGE_FONT_SIZE, multiline=False)
            # bind the text input to the callback
            widget.bind(focus=self.on_config_id_focus)
            # add the widget to the dictionary
            self.box_layout.ids["configuration id"] = widget
            # add the widget to the layout and add the layout to the main layout
            box_layout.add_widget(widget)
            self.box_layout.add_widget(box_layout)

            # ========================================
            # shield directory property
            box_layout = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=std.STD_ROW_HEIGHT,
                spacing=std.STD_SPACING
            )
            # text label describing the property
            box_layout.add_widget(std.ConfigPropertyLabel(text="Shield Directory:"))
            # text input for the shield directory
            widget = TextInput(text="", font_size=std.STD_PAGE_FONT_SIZE, multiline=False)
            # bind the text input to the callback
            widget.bind(focus=self.on_shield_directory_focus)
            # add the widget to the dictionary
            self.box_layout.ids["shield directory"] = widget
            # add the widget to the layout and add the layout to the main layout
            box_layout.add_widget(widget)
            self.box_layout.add_widget(box_layout)

            # ========================================
            # Properties Screen: Select the KLE JSON file
            box_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=std.STD_ROW_HEIGHT,
                                   spacing=std.STD_SPACING)
            # text label describing the property
            box_layout.add_widget(std.ConfigPropertyLabel(text="Keyboard Layout Editor JSON File:"))
            # text label displaying the path to the KLE JSON file
            widget = std.ConfigPropertyLabel(text="", markup=True, size_hint_x=0.5, halign="left", max_lines=1)
            # widget added to the dictionary for easy access from the MainWindow class
            self.box_layout.ids["kle json path"] = widget
            box_layout.add_widget(widget)
            self.update_json_file_path()
            # button to open the file explorer dialog
            widget = Button(text="Select JSON", font_size=std.STD_PAGE_FONT_SIZE, size_hint_x=None,
                            width=metrics.sp(200))
            # binding the button to the callback
            widget.bind(on_release=self.on_select_json_file)
            # add the widget to the dictionary
            self.box_layout.ids["select json"] = widget
            # add the widget to the layout and add the layout to the main layout
            box_layout.add_widget(widget)
            self.box_layout.add_widget(box_layout)

            # ========================================
            # Properties Screen: MCU selection
            box_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=std.STD_ROW_HEIGHT,
                                   spacing=std.STD_SPACING)
            # text label describing the property
            box_layout.add_widget(std.ConfigPropertyLabel(text="Microcontroller:"))
            # text label displaying the selected MCU
            widget = std.ConfigPropertyLabel(text="", markup=True, size_hint_x=0.5, halign="left", max_lines=1)
            # widget added to the dictionary for easy access from the MainWindow class
            self.box_layout.ids["selected mcu"] = widget
            box_layout.add_widget(widget)
            self.update_mcu_text()
            # using a button to select the MCU
            widget = Button(text="Select MCU", font_size=std.STD_PAGE_FONT_SIZE, size_hint_x=None,
                            width=metrics.sp(200))
            # bind the button to the callback
            widget.method = "mcu_screen"
            widget.bind(on_release=self.on_select_mcu_button)
            # add the widget to the dictionary
            self.box_layout.ids["select mcu"] = widget
            # add the widget to the layout and add the layout to the main layout
            box_layout.add_widget(widget)
            self.box_layout.add_widget(box_layout)

            # ========================================
            # Properties Screen: Split Keyboard Property Enable Toggle
            box_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=std.STD_ROW_HEIGHT,
                                   spacing=std.STD_SPACING)
            # text label describing the property
            box_layout.add_widget(std.ConfigPropertyLabel(text="Split Keyboard:"))
            # toggle button to select if the keyboard is a split keyboard
            widget = ToggleButton(text="No", font_size=std.STD_PAGE_FONT_SIZE, size_hint_x=None,
                                  width=metrics.sp(100))
            # bind the toggle on_press event to the callback which will flipflop the text
            widget.bind(on_press=self.split_config_text_callback)
            # bind the on_release event to the
            widget.bind(on_release=lambda button: print_debug("Split Keyboard Toggle Button Pressed"))
            # add the widget to the dictionary and the layout
            self.box_layout.ids["split keyboard"] = widget
            box_layout.add_widget(widget)
            # label to for the selected side
            box_layout.add_widget(std.ConfigPropertyLabel(text="Side:", size_hint_x=1))
            # Toggle button to select the side of the split keyboard
            widget = ToggleButton(text="N/A", font_size=std.STD_PAGE_FONT_SIZE, size_hint_x=None,
                                  width=metrics.sp(100), disabled=True)
            # binding the on_press event to the callback which will flipflop the text between left and right
            widget.bind(on_press=self.split_keyboard_side_toggle_state_callback)
            # TODO add comment here
            widget.bind(on_release=lambda button: print_debug("Split Keyboard Side Button Pressed"))
            # add the widget to the dictionary
            self.box_layout.ids["split keyboard side"] = widget
            # add the widget to the layout and add the layout to the main layout
            box_layout.add_widget(widget)
            self.box_layout.add_widget(box_layout)

            # ========================================
            # Properties Screen: Number of paired and simultaneous connections
            box_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=std.STD_ROW_HEIGHT,
                                   spacing=std.STD_SPACING)
            # text label for number of paired connections
            box_layout.add_widget(std.ConfigPropertyLabel(text="Number of Paired Connections:"))
            # integer text input for the number of paired connections
            widget = TextInput(text="1", font_size=std.STD_PAGE_FONT_SIZE, multiline=False, input_filter="int")
            # bind the text input to the callback
            widget.method = "set_paired_connections"
            widget.bind(focus=self.on_text_intput_focus)
            # add the widget to the dictionary
            self.box_layout.ids["paired_connections"] = widget
            # add the widget to the layout
            box_layout.add_widget(widget)
            # text label for number of simultaneous connections
            box_layout.add_widget(std.ConfigPropertyLabel(text="Number of Simultaneous Connections:"))
            # integer text input for the number of simultaneous connections
            widget = TextInput(text="1", font_size=std.STD_PAGE_FONT_SIZE, multiline=False, input_filter="int")
            # TODO add comment here
            widget.bind(focus=lambda text_intput, focus: print_debug(
                "Simultaneous Connections Text Input Focus: " + str(focus)))
            # add the widget to the dictionary
            box_layout.add_widget(widget)
            # add the widget to the dictionary
            self.box_layout.ids["simultaneous_connections"] = widget
            # add the layout to the main layout
            self.box_layout.add_widget(box_layout)

            # ========================================
            # Properties Screen: Rotary Encoders
            box_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=std.STD_ROW_HEIGHT,
                                   spacing=std.STD_SPACING)
            # text label that is used to display is the rotary encoders are enabled
            box_layout.add_widget(std.ConfigPropertyLabel(text="Rotary Encoders:"))
            # toggle button to select if the rotary encoders are enabled
            widget = ToggleButton(text="No", font_size=std.STD_PAGE_FONT_SIZE, size_hint_x=None,
                                  width=metrics.sp(100))
            # bind the toggle on_press event to the callback which will flipflop the text
            widget.bind(on_press=self.encoder_config_toggle_text_call_back)
            # bind the on_release event to the callback
            widget.bind(on_release=lambda button: print_debug("Rotary Encoder Toggle Button Pressed"))
            # add the widget to the dictionary
            self.box_layout.ids["rotary encoders"] = widget
            # add the widget to the layout
            box_layout.add_widget(widget)
            # text label describing the property
            box_layout.add_widget(std.ConfigPropertyLabel(text="Number of Rotary Encoders:"))
            # integer text input
            widget = TextInput(text="0", font_size=std.STD_PAGE_FONT_SIZE, multiline=False, input_filter="int",
                               disabled=True)
            # bind the text input to the callback
            widget.method = "set_number_of_rotary_encoders"
            widget.bind(focus=self.on_text_intput_focus)
            # add the widget to the dictionary
            self.box_layout.ids["number of rotary encoders"] = widget
            # add the widget to the layout and add the layout to the main layout
            box_layout.add_widget(widget)
            self.box_layout.add_widget(box_layout)

            # ========================================
            # little message to say that all properties are not implemented yet
            label = Label(
                text="Extra configuration properties are not implemented yet but can be added in the output files",
                halign="center", valign="center")
            label.bind(size=label.setter("text_size"))
            self.box_layout.add_widget(label)

            #         # ========================================
            #         # test button
            #         self.box_layout.add_widget(Button(
            #             text="Test",
            #             font_size=std_widgets.STD_PAGE_FONT_SIZE,
            #             size_hint_y=None,
            #             height=std_widgets.STD_ROW_HEIGHT,
            #             on_press=self.test_button_callback
            #         ))
            #
            # def test_button_callback(self, button: Button):
            #     print_debug(self.box_layout.ids)

    # noinspection PyUnusedLocal
    def on_select_working_directory(self, button: Button):
        """
        callback for when the select working directory button is pressed
        """
        main_window: MainWindow = App.get_running_app().root
        directory_path = select_directory_dialog(
            "Select Working Directory, top level directory which holds the github repository")
        if directory_path:
            try:
                main_window.zmk_config.set_working_directory(directory_path)
                self.update_directory_path(directory_path)
            except Exception as error:
                main_window.zmk_error(error)

    def update_directory_path(self, directory_path: str = None):
        """
        updates the directory path

        @param directory_path: the directory path as a string or None, if it is None it will attempt to get the
        directory path from the main window
        """
        if directory_path is None:
            main_window: MainWindow = App.get_running_app().root
            if main_window is not None:
                directory_path = main_window.zmk_config.get_working_directory()

        self.box_layout.ids["working directory"].text = directory_path if directory_path else "No Directory Selected"

    @staticmethod
    def on_config_name_focus(text_input: TextInput, focus: bool):
        """
        Callback for when the text input for the config name is focused or unfocused, if it is unfocused it is assumed
        that the user has finished with the text input. so the method will attempt to set the config name.
        """
        if focus:
            return
        # this is not strictly necessary to make a reference to the MainWindow, but it makes the type checking happy
        main_window: MainWindow = App.get_running_app().root
        current_config_name = main_window.zmk_config.get_config_name()
        # attempt to set the config name
        try:
            main_window.zmk_config.set_config_name(name=str(text_input.text))
        # it is "possible" to get a TypeError but because the text input is a string it should not happen
        # hence why I added the extra message.
        except TypeError as error:
            error.args = (str(error) + ". If you got this error then you have managed to break something")
            main_window.zmk_error(error)
            text_input.text = current_config_name if current_config_name else ""
        # if the config name already exists then raise a ValueError
        except ValueError as error:
            main_window.zmk_error(error)
            text_input.text = current_config_name if current_config_name else ""

    @staticmethod
    def on_config_id_focus(text_input: TextInput, focus: bool):
        """
        Callback for when the text input for the config id is focused or unfocused, if it is unfocused it is assumed
        that the user has finished with the text input. so the method will attempt to set the config id.
        """
        if focus:
            return
        # this is not strictly necessary to make a reference to the MainWindow, but it makes the type checking happy
        main_window: MainWindow = App.get_running_app().root
        current_config_id = main_window.zmk_config.get_config_id()
        try:
            main_window.zmk_config.set_config_id(config_id=str(text_input.text))
        # it is "possible" to get a TypeError but considering that the config_id is a string it should never happen
        # hence why I added to the error message
        except TypeError as error:
            error.args = (str(error) + ". If you got this error then you have managed to break something")
            main_window.zmk_error(error)
            text_input.text = current_config_id if current_config_id else ""
        # if the config id already exists then it will raise a ValueError
        except ValueError as error:
            main_window.zmk_error(error)
            text_input.text = current_config_id if current_config_id else ""

    @staticmethod
    def on_shield_directory_focus(text_input: TextInput, focus: bool):
        """
        Callback for when the text input for the shield directory is focused or unfocused, if it is unfocused it is
        assumed that the user has finished with the text input. so the method will attempt to set the shield directory.
        """
        if focus:
            return
        # this is not strictly necessary to make a reference to the MainWindow, but it makes the type checking happy
        main_window: MainWindow = App.get_running_app().root
        current_shield_directory = main_window.zmk_config.get_shield_directory()
        # attempts to set the shield directory
        try:
            main_window.zmk_config.set_shield_directory(shield_directory=str(text_input.text))
        # it is a "possible" error but given that the text input is a string it should never happen
        # hence why I wrote the error message like this
        except TypeError as error:
            error.args = (str(error) + ". If you got this error then you have managed to break something")
            main_window.zmk_error(error)
            text_input.text = current_shield_directory if current_shield_directory else ""
        # if the directory already exists then it will raise a ValueError
        except ValueError as error:
            main_window.zmk_error(error)
            text_input.text = current_shield_directory if current_shield_directory else ""

    # noinspection PyUnusedLocal
    def on_select_json_file(self, button: Button):
        """
        callback for when the select json file button is pressed
        """
        main_window: MainWindow = App.get_running_app().root
        json_file_path = select_file_dialog("Select JSON File, file that contains the keyboard layout",
                                            wildcard="*.json")
        if json_file_path and json_file_path != main_window.json_file_path:
            try:
                # attempt to parse the json file before setting the json file path to make sure that the json file
                # is valid
                main_window.kle_json = pykle.parse(open(json_file_path, encoding="utf-8").read())
                main_window.json_file_path = json_file_path
                # because the json file has changed, the assumption is that the layout has changed and the current
                # keymap/row/columns are no longer valid therefore they are cleared and the keymaps are redrawn
                main_window.zmk_config.clear_key_data()
                main_window.redraw_keymap()
            except Exception as error:
                main_window.zmk_error(error)
        # update the json file path in the GUI
        self.update_json_file_path()

    def update_json_file_path(self, json_file_path: str = None):
        """
        updates the json file path, if no file path is passed then it will attempt to get the file path from the main
        window
        """
        main_window: MainWindow = App.get_running_app().root
        if main_window is None:
            return
        json_file_path = main_window.json_file_path if json_file_path is None else json_file_path
        self.box_layout.ids["kle json path"].text = json_file_path if json_file_path else "No JSON File Selected"

    # noinspection PyUnusedLocal
    @staticmethod
    def on_select_mcu_button(button: Button):
        """
        method changes the screen manager's screen to the MCU selection screen
        """
        main_window: MainWindow = App.get_running_app().root
        main_window.screen_manager.current = "MCU Selection"

    # noinspection PyUnusedLocal
    def update_mcu_text(self, mcu: str = None):
        """
        updates the mcu text. if no mcu is passed then it will attempt to get the mcu from the main window
        """
        main_window: MainWindow = App.get_running_app().root
        if main_window is None:
            return
        mcu = main_window.zmk_config.get_mcu()
        self.box_layout.ids["selected mcu"].text = str(mcu) if mcu else "No MCU Selected"

    def split_config_text_callback(self, toggle_button: ToggleButton):
        """
        Flipflops the text on the button for enabling the split keyboard between "Yes" and "No"
        """
        # used to enable or disable the split keyboard side toggle button
        split_keyboard_side = self.box_layout.ids["split keyboard side"]
        if toggle_button.state == "down":
            toggle_button.text = "Yes"
            split_keyboard_side.disabled = False
        else:
            toggle_button.text = "No"
            split_keyboard_side.disabled = True
        # update the text on the split keyboard side toggle button
        self.split_config_side_text_callback(split_keyboard_side)

    @staticmethod
    def split_config_side_text_callback(toggle_button: ToggleButton):
        """
        Flipflops the text on the button for enabling the split keyboard between "Left" and "Right"
        """
        if toggle_button.disabled:
            toggle_button.text = "N/A"
        elif toggle_button.state == "down":
            toggle_button.text = "Right"
        else:
            toggle_button.text = "Left"

    def split_config_side_enabled(self, toggle_button: ToggleButton):
        """
        Enables the button for selecting the side of the split keyboard
        """
        if toggle_button.state == "down":
            self.box_layout.ids["split keyboard"].disabled = True
        else:
            self.box_layout.ids["split keyboard"].disabled = True
        print_debug("method called: split config side enabled")

    def encoder_config_toggle_text_call_back(self, toggle_button: ToggleButton):
        """
        Flipflops the text on the toggle button between "Yes" and "No"
        """
        if toggle_button.state == "down":
            toggle_button.text = "Yes"
            self.box_layout.ids["number of rotary encoders"].disabled = False
        else:
            toggle_button.text = "No"
            self.box_layout.ids["number of rotary encoders"].disabled = True

    @staticmethod
    def split_keyboard_side_toggle_state_callback(toggle_button: ToggleButton):
        """
        Flipflops the text on the toggle button between "Left" and "Right"
        """
        if toggle_button.state == "down":
            toggle_button.text = "Right"
        else:
            toggle_button.text = "Left"

    @staticmethod
    def on_button_callback(button: Button):
        """
        on_button_callback is called when a button is pressed. This method is planned to be deprecated.
        """
        main_window: MainWindow = App.get_running_app().root
        main_window.event_callback(button.method, value=button.state == "down")

    def on_text_intput_focus(self, text_input: TextInput, focus: bool) -> None:
        """
        on_text_intput_focus is called when a text input focus changes, it is used to change the configuration option
        once the user clicks away from the text input, so that the configuration can be updated then instead of on every
        key press. This method is planned to be deprecated.
        """
        if focus:
            return
        key = find_id(self.box_layout, text_input)
        main_window: MainWindow = App.get_running_app().root
        main_window.event_callback(key, value=text_input.text)


class KeyWidget(Scatter):
    """
    This class is a super class which will be used to create keys which will form the visual representation
    of the keyboard
    """

    def __init__(self, key_index: int, **kwargs):
        """
        The constructor for the KeyWidget class, key_index is taken so that it can fetch the key from the kle data. Then
        along with maths it will render the key with the correct size and position, and rotation if needed.

        @param key_index: the index of the key in from the pykle.KeyBoard.keys list
        """
        main_window: MainWindow = App.get_running_app().root
        key: pykle.Key = main_window.kle_json.keys[key_index]
        super().__init__(**kwargs)
        self.kivy_y = 0
        self.key_index = key_index
        self.size_hint = (None, None)
        self.size = key.width * std.STD_KEY_UNIT, key.height * std.STD_KEY_UNIT
        self.do_translation = False

        # if there is rotation in the key, then the maths needs to be figured out to render the key correctly
        if key.rotation_angle != 0:
            # calculate the centre of the key so that the rotation can be done around the centre of the key
            key_center = (key.x + key.width / 2, key.y + key.height / 2)
            # storing the point of rotation as a tuple as its easier to work with
            point_of_rotation = (key.rotation_x, key.rotation_y)
            # calculate the position vector of the centre of the key relative to the point of rotation
            rel_position_vector = func.subtract_vectors(key_center, point_of_rotation)
            # calculate the magnitude of the position vector
            magnitude = func.magnitude(rel_position_vector)
            # calculating the new centre position relative to the point of rotation
            theta = func.calculate_angle(rel_position_vector)
            new_theta = theta - math.radians(key.rotation_angle)
            new_rel_position_vector = (magnitude * math.sin(new_theta), magnitude * math.cos(new_theta))
            # calculating the position of the bottom left corner of the key relative to the point of rotation
            new_rel_bl_pos_vector = (new_rel_position_vector[0] - key.width / 2,
                                     new_rel_position_vector[1] + key.height / 2)
            # calculating the new position of the bottom left corner of the key
            new_bl_pos_vector = func.add_vectors(point_of_rotation, new_rel_bl_pos_vector)
            # calculating the new position of the key for kivy
            self.kivy_y = new_bl_pos_vector[1] * std.STD_KEY_UNIT
            self.pos = (new_bl_pos_vector[0] * std.STD_KEY_UNIT, main_window.screen_manager.height - self.kivy_y)
            self.do_rotation = True
            self.rotation = -key.rotation_angle
        else:
            self.do_rotation = False
            self.rotation = 0
            self.kivy_y = (key.y + key.height) * std.STD_KEY_UNIT
            self.pos = (key.x * std.STD_KEY_UNIT, main_window.screen_manager.height - self.kivy_y)

        with self.canvas:
            Color(1, 1, 1, 0.5)
            Rectangle(pos_hint={"center_x": 0.5, "center_y": 0.5},
                      size=(key.width * std.STD_KEY_UNIT - std.STD_KEY_GAP,
                            key.height * std.STD_KEY_UNIT - std.STD_KEY_GAP))

        main_window.screen_manager.bind(height=self.on_height)

    # noinspection PyUnusedLocal
    def on_height(self, screen_manager: ScreenManager, height):
        """
        on_height is called when the height of the window changes, this is used to update the position of the key
        to ensure that it stays at the top of the window

        @param screen_manager: the screen manager which is bound to the event
        @param height: the new height of the screen_manager widget
        """
        self.y = height - self.kivy_y


class RowColumnScreen(Screen):
    """
    RowColumnScreen allows user to configure the rows and columns of the keyboard
    """




    class RowColumnWidget(KeyWidget):
        """
        Inherits the KeyWidget class and adds box layout to create a widget which can be used to configure the
        rows and columns for keys of the keyboard.
        """

        def __init__(self, index):
            """
            method adds a box layout which contains two text inputs, one for the row and one for the column

            @param index: refer to KeyWidget's constructor for the purpose of this parameter
            """
            super().__init__(index)
            # grabs the key object from the kle json
            main_window: MainWindow = App.get_running_app().root
            key: pykle.Key = main_window.kle_json.keys[index]
            # creates a box layout which will contain the text inputs
            box_layout = BoxLayout(orientation="horizontal", size_hint=(None, None), spacing=std.STD_KEY_GAP / 4)
            box_layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}
            box_layout.size = (key.width * std.STD_KEY_UNIT - std.STD_KEY_GAP,
                               key.height * std.STD_KEY_UNIT - std.STD_KEY_GAP)
            # creates the text inputs, self.row and self.column are used to store the values of the text inputs
            # as integers and are updated when the text of the text inputs are changed if both text inputs are
            # integers then the row and column objects in the transform object of the zmk_config object are updated
            self.row: int | None = None
            self.row_input = TextInput(hint_text="R", input_filter="int", size_hint=(1, 1), multiline=False,
                                       halign="center")
            self.column: int | None = None
            self.row_input.bind(text=self.on_text)
            self.col_input = TextInput(hint_text="C", input_filter="int", size_hint=(1, 1), multiline=False,
                                       halign="center")
            self.col_input.bind(text=self.on_text)
            box_layout.add_widget(self.row_input)
            box_layout.add_widget(self.col_input)
            self.add_widget(box_layout)

        def on_text(self, text_input: TextInput, value: str):
            """
            Method is called when the text of the text input is changed

            @param text_input: widget which called the method
            @param value: the new text from the text input
            """
            # if the text input is empty then the value is set to None
            if value == "":
                value = None

            # if the instance of the text input is the row_input
            # then the value is set provided that it is not None
            if text_input == self.row_input and value is not None:
                self.row = int(value)
            # otherwise it is safe to assume that the instance is the col_input
            # so the value is set provided that it is not None
            elif value is not None:
                self.column = int(value)

            # if both the row and column are integers then the row and column objects in the transform object
            if isinstance(self.row, int) and isinstance(self.column, int):
                main_window: MainWindow = App.get_running_app().root
                transform: ZMK.Transform.MatrixTransform = main_window.zmk_config.get_transform()
                # attempts to add the row and column to the transform object
                # if an error occurs, which shouldn't happen in the current implementation,
                # then the error is displayed to the user
                try:
                    transform.add_key(self.row, self.column, index=self.key_index)
                except Exception as error:
                    main_window.zmk_error(error)




    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = 1, 1
        self.float_layout = FloatLayout(size_hint=(1, 1))
        """Float layout is used as this allows for absolute positioning of KeyWidgets"""
        self.add_widget(self.float_layout)

    def on_parent(self, widget: RowColumnScreen, parent: ScreenManager):
        """
        on_parent is called when this widget is added to a parent widget

        @param widget: self
        @param parent: the parent widget, ScreenManager
        """
        print_debug(f"{self.__class__.__name__}: {widget} {parent}", info="ON PARENT")

    def redraw_keymap(self):
        """
        Method is called when the keymap needs to be redrawn
        """
        self.float_layout.clear_widgets()
        main_window: MainWindow = App.get_running_app().root
        for index in range(len(main_window.kle_json.keys)):
            self.float_layout.add_widget(self.RowColumnWidget(index=index))


class GpioScreen(Screen):
    """
    GpioScreen allows user to configure the GPIO pins of the keyboard
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.float_layout = FloatLayout(size_hint=(1, 1))
        """Float layout is used as place holder for the widgets, a boxlayout or something similar will be used later"""
        self.in_focus = False
        self.add_widget(self.float_layout)

    def on_parent(self, widget: GpioScreen, parent: ScreenManager):
        """
        on_parent is called when this widget is added to a parent widget

        @param widget: self
        @param parent: the parent widget, ScreenManager
        """
        print_debug(f"{self.__class__.__name__}: {widget} {parent}", info="ON PARENT")
        if not self.float_layout.children:
            # label placeholder
            self.float_layout.add_widget(Label(
                text="GpioScreen",
                font_size=std.STD_FONT_SIZE * 3
            ))
            self.ids["placeholder label"] = self.float_layout.children[0]


class KeymapScreen(Screen):
    """
    KeymapScreen allows user to configure the keymap of the keyboard
    """




    class KeyMapWidget(KeyWidget):
        """
        Inherits the KeyWidget class and adds box layout to create a widget which can be used to configure the
        Behaviours for the keymap of the keyboard.
        """

        def __init__(self, index):
            """
            Refer to the description of this class for the purpose of this method

            @param index: Refer to KeyWidget.__init__ for the purpose of this parameter
            """
            super().__init__(index)
            main_window: MainWindow = App.get_running_app().root
            key: pykle.Key = main_window.kle_json.keys[index]
            self.label = Label(text=f"{index}", font_size=std.STD_FONT_SIZE * 1.5, size_hint=(None, None))
            self.label.pos_hint = {"center_x": 0.5, "center_y": 0.5}
            self.label.size = (key.width * std.STD_KEY_UNIT - std.STD_KEY_GAP,
                               key.height * std.STD_KEY_UNIT - std.STD_KEY_GAP)
            self.add_widget(self.label)




    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.float_layout = FloatLayout(size_hint=(1, 1))
        """Float layout is used for absolute positioning of KeyWidgets"""
        self.in_focus = False
        self.add_widget(self.float_layout)

    def redraw_keymap(self):
        """
        Method is called when the keymap needs to be redrawn
        """
        self.float_layout.clear_widgets()
        main_window: MainWindow = App.get_running_app().root
        for index in range(len(main_window.kle_json.keys)):
            self.float_layout.add_widget(self.KeyMapWidget(index=index))


class ExportScreen(Screen):
    """
    ExportScreen allows user to export the ZMK config
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box_layout = BoxLayout(size_hint=(1, 1), orientation="vertical", spacing=std.STD_SPACING)
        """Box layout will be used for to create a vertical list of widgets which will form a menu to export"""
        self.in_focus = False
        self.add_widget(self.box_layout)

    def on_parent(self, widget: ExportScreen, parent: ScreenManager):
        """
        on_parent is called when this widget is added to a parent widget

        @param widget: self
        @param parent: the parent widget, ScreenManager
        """
        print_debug(f"{self.__class__.__name__}: {widget} {parent}", info="ON PARENT")
        if not self.box_layout.children:
            # label placeholder
            self.box_layout.add_widget(Label(
                text="ExportScreen",
                font_size=std.STD_FONT_SIZE * 3
            ))
            self.ids["placeholder label"] = self.box_layout.children[0]


class SettingsScreen(Screen):
    """
    SettingsScreen allows user to configure the settings of the application
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box_layout = BoxLayout(size_hint=(1, 1), orientation="vertical", spacing=std.STD_SPACING)
        self.in_focus = False
        self.add_widget(self.box_layout)

    def on_parent(self, widget: SettingsScreen, parent: ScreenManager):
        """
        on_parent is called when this widget is added to a parent widget#

        @param widget: self
        @param parent: the parent widget, ScreenManager
        """
        print_debug(f"{self.__class__.__name__}: {widget} {parent}", info="ON PARENT")
        if not self.box_layout.children:
            # label placeholder
            self.box_layout.add_widget(Label(
                text="SettingsScreen",
                font_size=std.STD_FONT_SIZE * 3
            ))
            self.ids["placeholder label"] = self.box_layout.children[0]


class ConsoleScreen(Screen):
    """
    ConsoleScreen allows user to view the console output
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True)
        self.in_focus = False
        self.console_history = []
        self.label: [Label, None] = None

    def on_parent(self, widget: ConsoleScreen, parent: ScreenManager):
        """
        on_parent is called when this widget is added to a parent widget

        @param widget: self
        @param parent: the parent widget, ScreenManager
        """
        print_debug(f"{self.__class__.__name__}: {widget} {parent}", info="ON PARENT")
        if self.parent and not self.scroll_view.children:
            # scroll view to hold the console
            self.label = Label(text="", font_size=std.STD_FONT_SIZE)
            self.label.size_hint_y = None
            self.label.size_hint_x = None
            self.label.bind(texture_size=self.label_setter)
            self.scroll_view.add_widget(self.label)
            self.add_widget(self.scroll_view)

    # noinspection PyIncorrectDocstring
    def label_setter(self, label: Label, size: tuple[int, int]):
        """
        label_setter sets the dynamic attributes of the label which is the console

        @param size: texture size of the label
        @param label: the label widget
        """
        label.width = self.width
        label.height = size[1]
        label.text_size = (self.width * 0.98, None)

    def update_console(self, console_history: str):
        """
        update_console updates the console history and the label text

        @param console_history: A string which is the latest message to be added to the console
        """
        self.console_history.append(console_history)
        self.label.text = "\n".join(self.console_history)
        self.scroll_view.scroll_y = 0


class MainWindow(BoxLayout):
    """
    Main window class which is the main window of the application
    """

    def __init__(self, **kwargs):
        """
        The constructor for the MainWindow class which is the application,
        """
        super().__init__(**kwargs)
        # variables to do with the program
        self.zmk_config: ZMK.Config.ZMKConfig = ZMK.Config.ZMKConfig()
        """ZMK config object which stores handles the ZMK config"""
        self.json_file_path = ""
        """Variable is used to store the path to the json file which contains the keyboard layout editor data"""
        self.kle_json: pykle.Keyboard | None = None
        """Variable is used to store the parsed kle data from the json file with the pykle library"""
        # parameters to do with the widget/ gui
        self.orientation = "vertical"
        self.spacing = std.STD_SPACING

        # Code to add the option bar
        # ========================================
        # initialize the option bar
        widget = BoxLayout(
            orientation="horizontal",
            spacing=std.STD_SPACING,
            size_hint_y=None,
            height=std.STD_BUTTON_HEIGHT
        )
        self.add_widget(widget)
        self.ids["option bar"] = widget

        # ====================
        # test button
        widget = Button(
            text="Test",
            size_hint_x=None,
            width=metrics.sp(60),
            font_size=std.STD_FONT_SIZE,
            on_press=self.on_test_button
        )
        self.ids["option bar"].add_widget(widget)
        self.ids["option bar"].ids["test button"] = widget

        # ====================
        # settings button
        widget = Button(
            text="Settings",
            size_hint_x=None,
            width=metrics.sp(80),
            font_size=std.STD_FONT_SIZE,
            on_press=self.on_settings_button
        )
        self.ids["option bar"].add_widget(widget)
        self.ids["option bar"].ids["settings button"] = widget

        # ====================
        # load/save dropdown
        self.load_save_dropdown = DropDown()
        # creates the option buttons
        for option in ("New Config", "Load Config", "Save Config", "Save Config As"):
            button = Button(text=option, size_hint_y=None, height=std.STD_BUTTON_HEIGHT)
            # using a list with two functions which are called because they have () at the end
            # I did this because I did not want to create a new method for, I think it is more readable this way
            button.bind(on_release=lambda lambda_button: [
                # first function calls the method to close the dropdown
                self.load_save_dropdown.select(lambda_button.text),
                # second function calls the method in the class to handle that action
                # this dictionary acts as a switch statement
                {
                    "New Config"    : self.on_new_config,
                    "Load Config"   : self.on_load_config,
                    "Save Config"   : self.on_save_config,
                    "Save Config As": self.on_save_config_as
                }[lambda_button.text]()
            ])
            # add button to dropdown
            self.load_save_dropdown.add_widget(button)

        # add the load/save button
        self.ids["option bar"].add_widget(Button(
            text="Load/Save",
            size_hint_x=None,
            width=metrics.sp(120),
            font_size=std.STD_FONT_SIZE,
            on_release=self.load_save_dropdown.open
        ))

        # ====================
        # program status bar
        widget = Label(
            text=f"",
            markup=True,
            font_size=std.STD_FONT_SIZE,
            halign="left",
            valign="center",
            padding_x=std.STD_SPACING * 4,
        )
        self.ids["option bar"].add_widget(widget)
        self.ids["option bar"].ids["program status"] = widget
        widget.bind(size=widget.setter("text_size"))
        # ====================
        # console button
        widget = Button(
            text="Console",
            size_hint_x=None,
            width=metrics.sp(120),
            font_size=std.STD_FONT_SIZE,
            halign="left",
            valign="center",
            on_press=self.on_console_button
        )
        self.ids["option bar"].add_widget(widget)
        self.ids["option bar"].ids["console button"] = widget

        # ========================================
        # navigation bar and screen manager
        # add the screen manager

        # initialize the navigation bar
        widget = BoxLayout(
            orientation="horizontal",
            spacing=std.STD_SPACING,
            size_hint_y=None,
            height=std.STD_BUTTON_HEIGHT * 1.4
        )
        self.add_widget(widget)
        self.ids["navigation bar"] = widget

        # this makes it easier to access the children of the screen manager
        # as otherwise you would have quite a nest of widgets
        self.screen_manager = ScreenManager(transition=NoTransition())
        self.add_widget(self.screen_manager)
        self.screen_names = {
            "MCU Selection": MCUSelectionScreen,
            "Properties"   : PropertiesScreen,
            "Row & Column" : RowColumnScreen,
            "GPIO"         : GpioScreen,
            "Keymap"       : KeymapScreen,
            "Export"       : ExportScreen,
            "Settings"     : SettingsScreen,
            "Console"      : ConsoleScreen
        }
        accessible_screen_names = ("Properties", "Row & Column", "GPIO", "Keymap", "Export")
        # adds the buttons for the different screens to the navigation bar
        # as well as the screen to the screen manager
        for screen_name in self.screen_names:
            # adds buttons for screen names that I want to be accessible in the navigation bar
            if screen_name in accessible_screen_names:
                button = Button(
                    text=screen_name,
                    font_size=std.STD_FONT_SIZE * 1.4,
                    on_release=self.on_nav_button
                )
                self.ids["navigation bar"].add_widget(button)
                self.ids["navigation bar"].ids[f"{screen_name} button"] = button
            # adds the screen to the screen manager
            self.screen_manager.add_widget(self.screen_names[screen_name](name=screen_name))
            self.screen_manager.current = screen_name
        self.screen_manager.current = "Properties"

        # after everything has been added and initialized, the program status is updated
        # this is also done here since if it was done at the top when
        self.update_console("Program started")

    def redraw_keymap(self):
        """
        This method is called when the keymap is changed and needs to be redrawn
        """
        row_column_screen: RowColumnScreen = self.screen_manager.get_screen("Row & Column")
        row_column_screen.redraw_keymap()
        key_map_screen: KeymapScreen = self.screen_manager.get_screen("Keymap")
        key_map_screen.redraw_keymap()

    def on_nav_button(self, instance: Button):
        """
        This method is called when a navigation button is pressed. The method will change the screen to the screen that
        is associated with the button.

        @param instance: required parameter for kivy
        """
        self.screen_manager.current = instance.text

    # noinspection PyUnusedLocal
    def on_test_button(self, instance):
        """
        This method is called when the test button is pressed. The test button is just used for testing and is not part
        of the application

        @param instance: required parameter for kivy
        """
        transform: ZMK.Transform.MatrixTransform = self.zmk_config.get_transform()
        print_debug(f"Transform matrix: {transform.get_matrix()}", info="Test Button")
        self.redraw_keymap()

    # noinspection PyUnusedLocal
    def on_settings_button(self, instance):
        """
        This method is called when the settings button is pressed. The settings button will open the settings Screen

        @param instance: required parameter for kivy
        """
        self.screen_manager.current = "Settings"

    # noinspection PyUnusedLocal
    def on_console_button(self, instance):
        """
        This method is called when the console button is pressed. The console button will open the console Screen

        @param instance: required parameter for kivy
        """
        self.screen_manager.current = "Console"

    @staticmethod
    def on_new_config():
        """
        Method is called when the user wants to create a new configuration, not yet implemented
        """
        print_debug("New Config button pressed")

    @staticmethod
    def on_load_config():
        """
        Method is called when the user wants to load a configuration, not yet implemented
        """
        print_debug("Load Config button pressed")

    @staticmethod
    def on_save_config():
        """
        Method is called when the user wants to save a configuration, not yet implemented
        """
        print_debug("Save Config button pressed")

    @staticmethod
    def on_save_config_as():
        """
        Method is called when the user wants to save a configuration as, not yet implemented
        """
        print_debug("Save Config As button pressed")

    def zmk_error(self, error: str | Exception):
        """
        The ZMK Package was created so that it could be used in other applications. Therefore, it is possible that
        the ZMK Package throw errors (purposefully), this program catches those errors and will display the error
        to the user at the top of the window as log it in the internal console. And revert the changes that caused the
        error.

        @param error: either a string or an exception, if it is an exception, the name of the exception will be added to
        the string
        """

        if isinstance(error, Exception):
            error = error.__class__.__name__ + ": " + str(error)
            print_debug(f"{error.__class__.__name__}, {error}", info="ZMK Error")
        else:
            print_debug(error, info="ZMK Error")
        self.update_console("ZMK Error: " + error)

    def update_console(self, console_str: str):
        """
        Main method to be called to update the console, it updates the console and the program status
        """
        console_screen: ConsoleScreen = self.screen_manager.get_screen("Console")
        console_screen.update_console(console_str)
        self.ids["option bar"].ids["program status"].text = f"[b]Program Status:[/b] [i]{console_str}[/i]"

    @staticmethod
    def event_callback(widget_id: str = "", **kwargs):
        """
        Method is called by the children held within the layout of the screens within the screen manager, this is a
        callback method which is called when the user changes a value in the configuration

        @param widget_id: key is id of the widget which has changed
        @param kwargs: a dictionary is used for potential arguments for methods that this method will call
        """
        # this method is deprecated
        print_debug(f"widget_id: {widget_id}, kwargs: {kwargs}", info="Event Callback")


class Application(App):
    """
    Main application class which runs the application
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "ZMK GUI Configurator"
        self.icon = "zmk_logo.svg"

    def build(self):
        """
        Method in kivy which is used to build the application on runtime
        """
        return MainWindow()


if __name__ == "__main__":
    Application().run()
