"""This module contains the standard widgets as well as constants which are used throughout the application"""
from __future__ import annotations

from kivy import metrics as metrics
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton

# standard constants for the ui
STD_PAGE_FONT_SIZE = metrics.sp(20)
"""Standard font size for the text within the separate pages of the application"""
STD_SPACING = metrics.sp(2)
"""Standard spacing between widgets"""
STD_FONT_SIZE = metrics.sp(17.5)
"""Standard font size for the text within the application"""
STD_BUTTON_HEIGHT = metrics.sp(32.5)
"""Standard height for buttons"""
STD_ROW_HEIGHT = metrics.sp(45)
"""Standard height for rows"""
STD_KEY_UNIT = metrics.sp(60)
"""Standard for the keys which are used for the visual representation of the keyboard"""
STD_KEY_GAP = metrics.sp(5)
"""Standard gap between the keys"""


class ConfigPropertyLabel(Label):
    """
    Commonly used label for the Properties section of the application
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = kwargs["size_hint_x"] if "size_hint_x" in kwargs else None
        # self.width = kwargs["width"] if "width" in kwargs else metrics.dp(310)
        if "width" in kwargs:
            self.width = kwargs["width"]
        elif "size_hint_x" not in kwargs:
            self.width = metrics.dp(310)
        self.font_size = kwargs["font_size"] if "font_size" in kwargs else STD_PAGE_FONT_SIZE
        self.bind(size=self.setter("text_size"))
        self.halign = kwargs["halign"] if "halign" in kwargs else "center"
        self.valign = kwargs["valign"] if "valign" in kwargs else "center"


class ConfigPropertyToggle(ToggleButton):
    """
    Commonly used toggle button for the Properties section of the application
    """

    def __init__(self, on_state_text: str = "", off_state_text: str = "", **kwargs):
        """
        @param on_state_text: If this is not set then it will be set to the default text of this class
        @param off_state_text: If this is not set then it will be set to the default text of this class
        """
        super().__init__(**kwargs)
        self.font_size = kwargs["font_size"] if "font_size" in kwargs else STD_PAGE_FONT_SIZE
        self.bind(size=self.setter("text_size"))
        self.halign = kwargs["align"] if "halign" in kwargs else "center"
        self.valign = kwargs["valign"] if "valign" in kwargs else "center"
        self.on_state_text = on_state_text
        self.off_state_text = off_state_text
        self.on_state(self, "up")

    # noinspection PyUnusedLocal
    def on_state(self, instance: ConfigPropertyToggle, state: str):
        """
        Updates the text of the button when the state changes

        @param instance: self
        @param state: The state of the button either "up" or "down"
        """
        if self.disabled:
            self.text = "Disabled"
        elif state == "down":
            self.text = self.on_state_text
        else:
            self.text = self.off_state_text
