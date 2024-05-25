from __future__ import annotations

import tkinter as tk  # noqa

from FreeSimpleGUI import _hex_to_hsl
from FreeSimpleGUI import _hsl_to_rgb
from FreeSimpleGUI import COLOR_SYSTEM_DEFAULT
from FreeSimpleGUI import ELEM_TYPE_INPUT_RADIO
from FreeSimpleGUI import Element
from FreeSimpleGUI import rgb
from FreeSimpleGUI import theme_background_color
from FreeSimpleGUI import theme_text_color
from FreeSimpleGUI._utils import _error_popup_with_traceback


class Radio(Element):
    """
    Radio Button Element - Used in a group of other Radio Elements to provide user with ability to select only
    1 choice in a list of choices.
    """

    def __init__(
        self,
        text,
        group_id,
        default=False,
        disabled=False,
        size=(None, None),
        s=(None, None),
        auto_size_text=None,
        background_color=None,
        text_color=None,
        circle_color=None,
        font=None,
        key=None,
        k=None,
        pad=None,
        p=None,
        tooltip=None,
        change_submits=False,
        enable_events=False,
        right_click_menu=None,
        expand_x=False,
        expand_y=False,
        visible=True,
        metadata=None,
    ):
        """
        :param text:             Text to display next to button
        :type text:              (str)
        :param group_id:         Groups together multiple Radio Buttons. Any type works
        :type group_id:          (Any)
        :param default:          Set to True for the one element of the group you want initially selected
        :type default:           (bool)
        :param disabled:         set disable state
        :type disabled:          (bool)
        :param size:             (w, h) w=characters-wide, h=rows-high. If an int instead of a tuple is supplied, then height is auto-set to 1
        :type size:              (int, int)  | (None, None) | int
        :param s:                Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                 (int, int)  | (None, None) | int
        :param auto_size_text:   if True will size the element to match the length of the text
        :type auto_size_text:    (bool)
        :param background_color: color of background
        :type background_color:  (str)
        :param text_color:       color of the text
        :type text_color:        (str)
        :param circle_color:     color of background of the circle that has the dot selection indicator in it
        :type circle_color:      (str)
        :param font:             specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:              (str or (str, int[, str]) or None)
        :param key:              Used with window.find_element and with return values to uniquely identify this element
        :type key:               str | int | tuple | object
        :param k:                Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                 str | int | tuple | object
        :param pad:              Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:               (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                 (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param tooltip:          text, that will appear when mouse hovers over the element
        :type tooltip:           (str)
        :param change_submits:   DO NOT USE. Only listed for backwards compat - Use enable_events instead
        :type change_submits:    (bool)
        :param enable_events:    Turns on the element specific events. Radio Button events happen when an item is selected
        :type enable_events:     (bool)
        :param right_click_menu: A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type right_click_menu:  List[List[ List[str] | str ]]
        :param expand_x:         If True the element will automatically expand in the X direction to fill available space
        :type expand_x:          (bool)
        :param expand_y:         If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:          (bool)
        :param visible:          set visibility state of the element
        :type visible:           (bool)
        :param metadata:         User metadata that can be set to ANYTHING
        :type metadata:          (Any)
        """

        self.InitialState = default
        self.Text = text
        self.Widget = self.TKRadio = None  # type: tk.Radiobutton
        self.GroupID = group_id
        self.Value = None
        self.Disabled = disabled
        self.TextColor = text_color if text_color else theme_text_color()
        self.RightClickMenu = right_click_menu

        if circle_color is None:
            # ---- compute color of circle background ---
            try:  # something in here will fail if a color is not specified in Hex
                text_hsl = _hex_to_hsl(self.TextColor)
                background_hsl = _hex_to_hsl(background_color if background_color else theme_background_color())
                l_delta = abs(text_hsl[2] - background_hsl[2]) / 10
                if text_hsl[2] > background_hsl[2]:  # if the text is "lighter" than the background then make background darker
                    bg_rbg = _hsl_to_rgb(background_hsl[0], background_hsl[1], background_hsl[2] - l_delta)
                else:
                    bg_rbg = _hsl_to_rgb(background_hsl[0], background_hsl[1], background_hsl[2] + l_delta)
                self.CircleBackgroundColor = rgb(*bg_rbg)
            except:
                self.CircleBackgroundColor = background_color if background_color else theme_background_color()
        else:
            self.CircleBackgroundColor = circle_color
        self.ChangeSubmits = change_submits or enable_events
        self.EncodedRadioValue = None
        key = key if key is not None else k
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y

        super().__init__(
            ELEM_TYPE_INPUT_RADIO,
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

    def update(
        self,
        value=None,
        text=None,
        background_color=None,
        text_color=None,
        circle_color=None,
        disabled=None,
        visible=None,
    ):
        """
        Changes some of the settings for the Radio Button Element. Must call `Window.read` or `Window.finalize` prior

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param value:            if True change to selected and set others in group to unselected
        :type value:             (bool)
        :param text:             Text to display next to radio button
        :type text:              (str)
        :param background_color: color of background
        :type background_color:  (str)
        :param text_color:       color of the text. Note this also changes the color of the selection dot
        :type text_color:        (str)
        :param circle_color:     color of background of the circle that has the dot selection indicator in it
        :type circle_color:      (str)
        :param disabled:         disable or enable state of the element
        :type disabled:          (bool)
        :param visible:          control visibility of element
        :type visible:           (bool)
        """

        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Radio.update - The window was closed')
            return

        if value is not None:
            try:
                if value is True:
                    self.TKIntVar.set(self.EncodedRadioValue)
                elif value is False:
                    if self.TKIntVar.get() == self.EncodedRadioValue:
                        self.TKIntVar.set(0)
            except:
                print('Error updating Radio')
            self.InitialState = value
        if text is not None:
            self.Text = str(text)
            self.TKRadio.configure(text=self.Text)
        if background_color not in (None, COLOR_SYSTEM_DEFAULT):
            self.TKRadio.configure(background=background_color)
            self.BackgroundColor = background_color
        if text_color not in (None, COLOR_SYSTEM_DEFAULT):
            self.TKRadio.configure(fg=text_color)
            self.TextColor = text_color

        if circle_color not in (None, COLOR_SYSTEM_DEFAULT):
            self.CircleBackgroundColor = circle_color
            self.TKRadio.configure(selectcolor=self.CircleBackgroundColor)  # The background of the radio button
        elif text_color or background_color:
            if self.TextColor not in (None, COLOR_SYSTEM_DEFAULT) and self.BackgroundColor not in (None, COLOR_SYSTEM_DEFAULT) and self.TextColor.startswith('#') and self.BackgroundColor.startswith('#'):
                # ---- compute color of circle background ---
                text_hsl = _hex_to_hsl(self.TextColor)
                background_hsl = _hex_to_hsl(self.BackgroundColor if self.BackgroundColor else theme_background_color())
                l_delta = abs(text_hsl[2] - background_hsl[2]) / 10
                if text_hsl[2] > background_hsl[2]:  # if the text is "lighter" than the background then make background darker
                    bg_rbg = _hsl_to_rgb(background_hsl[0], background_hsl[1], background_hsl[2] - l_delta)
                else:
                    bg_rbg = _hsl_to_rgb(background_hsl[0], background_hsl[1], background_hsl[2] + l_delta)
                self.CircleBackgroundColor = rgb(*bg_rbg)
                self.TKRadio.configure(selectcolor=self.CircleBackgroundColor)  # The background of the checkbox

        if disabled is True:
            self.TKRadio['state'] = 'disabled'
        elif disabled is False:
            self.TKRadio['state'] = 'normal'
        self.Disabled = disabled if disabled is not None else self.Disabled

        if visible is False:
            self._pack_forget_save_settings()
        elif visible is True:
            self._pack_restore_settings()
        if visible is not None:
            self._visible = visible

    def reset_group(self):
        """
        Sets all Radio Buttons in the group to not selected
        """
        self.TKIntVar.set(0)

    def get(self):
        # type: (Radio) -> bool
        """
        A snapshot of the value of Radio Button -> (bool)

        :return: True if this radio button is selected
        :rtype:  (bool)
        """
        return self.TKIntVar.get() == self.EncodedRadioValue

    Get = get
    ResetGroup = reset_group
    Update = update
