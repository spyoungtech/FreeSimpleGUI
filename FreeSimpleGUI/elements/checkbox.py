from __future__ import annotations

import tkinter as tk  # noqa

from FreeSimpleGUI import _hex_to_hsl
from FreeSimpleGUI import _hsl_to_rgb
from FreeSimpleGUI import COLOR_SYSTEM_DEFAULT
from FreeSimpleGUI import ELEM_TYPE_INPUT_CHECKBOX
from FreeSimpleGUI import Element
from FreeSimpleGUI import rgb
from FreeSimpleGUI import theme_background_color
from FreeSimpleGUI import theme_text_color
from FreeSimpleGUI._utils import _error_popup_with_traceback


class Checkbox(Element):
    """
    Checkbox Element - Displays a checkbox and text next to it
    """

    def __init__(
        self,
        text,
        default=False,
        size=(None, None),
        s=(None, None),
        auto_size_text=None,
        font=None,
        background_color=None,
        text_color=None,
        checkbox_color=None,
        highlight_thickness=1,
        change_submits=False,
        enable_events=False,
        disabled=False,
        key=None,
        k=None,
        pad=None,
        p=None,
        tooltip=None,
        right_click_menu=None,
        expand_x=False,
        expand_y=False,
        visible=True,
        metadata=None,
    ):
        """
        :param text:                Text to display next to checkbox
        :type text:                 (str)
        :param default:             Set to True if you want this checkbox initially checked
        :type default:              (bool)
        :param size:                (w, h) w=characters-wide, h=rows-high. If an int instead of a tuple is supplied, then height is auto-set to 1
        :type size:                 (int, int)  | (None, None) | int
        :param s:                   Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                    (int, int)  | (None, None) | int
        :param auto_size_text:      if True will size the element to match the length of the text
        :type auto_size_text:       (bool)
        :param font:                specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:                 (str or (str, int[, str]) or None)
        :param background_color:    color of background
        :type background_color:     (str)
        :param text_color:          color of the text
        :type text_color:           (str)
        :param checkbox_color:      color of background of the box that has the check mark in it. The checkmark is the same color as the text
        :type checkbox_color:       (str)
        :param highlight_thickness: thickness of border around checkbox when gets focus
        :type highlight_thickness:  (int)
        :param change_submits:      DO NOT USE. Only listed for backwards compat - Use enable_events instead
        :type change_submits:       (bool)
        :param enable_events:       Turns on the element specific events. Checkbox events happen when an item changes
        :type enable_events:        (bool)
        :param disabled:            set disable state
        :type disabled:             (bool)
        :param key:                 Used with window.find_element and with return values to uniquely identify this element
        :type key:                  str | int | tuple | object
        :param k:                   Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                    str | int | tuple | object
        :param pad:                 Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:                  (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                   Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                    (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param tooltip:             text, that will appear when mouse hovers over the element
        :type tooltip:              (str)
        :param right_click_menu:    A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type right_click_menu:     List[List[ List[str] | str ]]
        :param expand_x:            If True the element will automatically expand in the X direction to fill available space
        :type expand_x:             (bool)
        :param expand_y:            If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:             (bool)
        :param visible:             set visibility state of the element
        :type visible:              (bool)
        :param metadata:            User metadata that can be set to ANYTHING
        :type metadata:             (Any)
        """

        self.Text = text
        self.InitialState = bool(default)
        self.Value = None
        self.TKCheckbutton = self.Widget = None  # type: tk.Checkbutton
        self.Disabled = disabled
        self.TextColor = text_color if text_color else theme_text_color()
        self.RightClickMenu = right_click_menu
        self.highlight_thickness = highlight_thickness

        # ---- compute color of circle background ---
        if checkbox_color is None:
            try:  # something in here will fail if a color is not specified in Hex
                text_hsl = _hex_to_hsl(self.TextColor)
                background_hsl = _hex_to_hsl(background_color if background_color else theme_background_color())
                l_delta = abs(text_hsl[2] - background_hsl[2]) / 10
                if text_hsl[2] > background_hsl[2]:  # if the text is "lighter" than the background then make background darker
                    bg_rbg = _hsl_to_rgb(background_hsl[0], background_hsl[1], background_hsl[2] - l_delta)
                else:
                    bg_rbg = _hsl_to_rgb(background_hsl[0], background_hsl[1], background_hsl[2] + l_delta)
                self.CheckboxBackgroundColor = rgb(*bg_rbg)
            except:
                self.CheckboxBackgroundColor = background_color if background_color else theme_background_color()
        else:
            self.CheckboxBackgroundColor = checkbox_color
        self.ChangeSubmits = change_submits or enable_events
        key = key if key is not None else k
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y

        super().__init__(
            ELEM_TYPE_INPUT_CHECKBOX,
            size=sz,
            auto_size_text=auto_size_text,
            font=font,
            background_color=background_color,
            text_color=self.TextColor,
            key=key,
            pad=pad,
            tooltip=tooltip,
            visible=visible,
            metadata=metadata,
        )

    def get(self):
        # type: (Checkbox) -> bool
        """
        Return the current state of this checkbox

        :return: Current state of checkbox
        :rtype:  (bool)
        """
        return self.TKIntVar.get() != 0

    def update(
        self,
        value=None,
        text=None,
        background_color=None,
        text_color=None,
        checkbox_color=None,
        disabled=None,
        visible=None,
    ):
        """
        Changes some of the settings for the Checkbox Element. Must call `Window.Read` or `Window.Finalize` prior.
        Note that changing visibility may cause element to change locations when made visible after invisible

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param value:            if True checks the checkbox, False clears it
        :type value:             (bool)
        :param text:             Text to display next to checkbox
        :type text:              (str)
        :param background_color: color of background
        :type background_color:  (str)
        :param text_color:       color of the text. Note this also changes the color of the checkmark
        :type text_color:        (str)
        :param disabled:         disable or enable element
        :type disabled:          (bool)
        :param visible:          control visibility of element
        :type visible:           (bool)
        """

        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Checkbox.update - The window was closed')
            return

        if value is not None:
            value = bool(value)
            try:
                self.TKIntVar.set(value)
                self.InitialState = value
            except:
                print('Checkbox update failed')
        if disabled is True:
            self.TKCheckbutton.configure(state='disabled')
        elif disabled is False:
            self.TKCheckbutton.configure(state='normal')
        self.Disabled = disabled if disabled is not None else self.Disabled

        if text is not None:
            self.Text = str(text)
            self.TKCheckbutton.configure(text=self.Text)
        if background_color not in (None, COLOR_SYSTEM_DEFAULT):
            self.TKCheckbutton.configure(background=background_color)
            self.BackgroundColor = background_color
        if text_color not in (None, COLOR_SYSTEM_DEFAULT):
            self.TKCheckbutton.configure(fg=text_color)
            self.TextColor = text_color
        # Color the checkbox itself
        if checkbox_color not in (None, COLOR_SYSTEM_DEFAULT):
            self.CheckboxBackgroundColor = checkbox_color
            self.TKCheckbutton.configure(selectcolor=self.CheckboxBackgroundColor)  # The background of the checkbox
        elif text_color or background_color:
            if self.CheckboxBackgroundColor is not None and self.TextColor is not None and self.BackgroundColor is not None and self.TextColor.startswith('#') and self.BackgroundColor.startswith('#'):
                # ---- compute color of checkbox background ---
                text_hsl = _hex_to_hsl(self.TextColor)
                background_hsl = _hex_to_hsl(self.BackgroundColor if self.BackgroundColor else theme_background_color())
                l_delta = abs(text_hsl[2] - background_hsl[2]) / 10
                if text_hsl[2] > background_hsl[2]:  # if the text is "lighter" than the background then make background darker
                    bg_rbg = _hsl_to_rgb(background_hsl[0], background_hsl[1], background_hsl[2] - l_delta)
                else:
                    bg_rbg = _hsl_to_rgb(background_hsl[0], background_hsl[1], background_hsl[2] + l_delta)
                self.CheckboxBackgroundColor = rgb(*bg_rbg)
                self.TKCheckbutton.configure(selectcolor=self.CheckboxBackgroundColor)  # The background of the checkbox

        if visible is False:
            self._pack_forget_save_settings()
        elif visible is True:
            self._pack_restore_settings()

        if visible is not None:
            self._visible = visible

    Get = get
    Update = update
