from __future__ import annotations

import tkinter as tk

import FreeSimpleGUI
from FreeSimpleGUI import COLOR_SYSTEM_DEFAULT
from FreeSimpleGUI import ELEM_TYPE_STATUSBAR
from FreeSimpleGUI import Element
from FreeSimpleGUI import RELIEF_SUNKEN
from FreeSimpleGUI._utils import _error_popup_with_traceback


class StatusBar(Element):
    """
    A StatusBar Element creates the sunken text-filled strip at the bottom. Many Windows programs have this line
    """

    def __init__(
        self,
        text,
        size=(None, None),
        s=(None, None),
        auto_size_text=None,
        click_submits=None,
        enable_events=False,
        relief=RELIEF_SUNKEN,
        font=None,
        text_color=None,
        background_color=None,
        justification=None,
        pad=None,
        p=None,
        key=None,
        k=None,
        right_click_menu=None,
        expand_x=False,
        expand_y=False,
        tooltip=None,
        visible=True,
        metadata=None,
    ):
        """
        :param text:             Text that is to be displayed in the widget
        :type text:              (str)
        :param size:             (w, h) w=characters-wide, h=rows-high. If an int instead of a tuple is supplied, then height is auto-set to 1
        :type size:              (int, int) |  (int, None) | int
        :param s:                Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                 (int, int)  | (None, None) | int
        :param auto_size_text:   True if size should fit the text length
        :type auto_size_text:    (bool)
        :param click_submits:    DO NOT USE. Only listed for backwards compat - Use enable_events instead
        :type click_submits:     (bool)
        :param enable_events:    Turns on the element specific events. StatusBar events occur when the bar is clicked
        :type enable_events:     (bool)
        :param relief:           relief style. Values are same as progress meter relief values.  Can be a constant or a string: `RELIEF_RAISED RELIEF_SUNKEN RELIEF_FLAT RELIEF_RIDGE RELIEF_GROOVE RELIEF_SOLID`
        :type relief:            (enum)
        :param font:             specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:              (str or (str, int[, str]) or None)
        :param text_color:       color of the text
        :type text_color:        (str)
        :param background_color: color of background
        :type background_color:  (str)
        :param justification:    how string should be aligned within space provided by size. Valid choices = `left`, `right`, `center`
        :type justification:     (str)
        :param pad:              Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:               (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                 (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param key:              Used with window.find_element and with return values to uniquely identify this element to uniquely identify this element
        :type key:               str | int | tuple | object
        :param k:                Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                 str | int | tuple | object
        :param right_click_menu: A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type right_click_menu:  List[List[ List[str] | str ]]
        :param expand_x:         If True the element will automatically expand in the X direction to fill available space
        :type expand_x:          (bool)
        :param expand_y:         If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:          (bool)
        :param tooltip:          text, that will appear when mouse hovers over the element
        :type tooltip:           (str)
        :param visible:          set visibility state of the element
        :type visible:           (bool)
        :param metadata:         User metadata that can be set to ANYTHING
        :type metadata:          (Any)
        """

        self.DisplayText = text
        self.TextColor = text_color if text_color else FreeSimpleGUI.DEFAULT_TEXT_COLOR
        self.Justification = justification
        self.Relief = relief
        self.ClickSubmits = click_submits or enable_events
        if background_color is None:
            bg = FreeSimpleGUI.DEFAULT_TEXT_ELEMENT_BACKGROUND_COLOR
        else:
            bg = background_color
        self.TKText = self.Widget = None  # type: tk.Label
        key = key if key is not None else k
        self.RightClickMenu = right_click_menu
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y

        super().__init__(
            ELEM_TYPE_STATUSBAR,
            size=sz,
            auto_size_text=auto_size_text,
            background_color=bg,
            font=font or FreeSimpleGUI.DEFAULT_FONT,
            text_color=self.TextColor,
            pad=pad,
            key=key,
            tooltip=tooltip,
            visible=visible,
            metadata=metadata,
        )
        return

    def update(self, value=None, background_color=None, text_color=None, font=None, visible=None):
        """
        Changes some of the settings for the Status Bar Element. Must call `Window.Read` or `Window.Finalize` prior

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param value:            new text to show
        :type value:             (str)
        :param background_color: color of background
        :type background_color:  (str)
        :param text_color:       color of the text
        :type text_color:        (str)
        :param font:             specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:              (str or (str, int[, str]) or None)
        :param visible:          set visibility state of the element
        :type visible:           (bool)
        """

        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in StatusBar.update - The window was closed')
            return

        if value is not None:
            self.DisplayText = value
            stringvar = self.TKStringVar
            stringvar.set(value)
        if background_color not in (None, COLOR_SYSTEM_DEFAULT):
            self.TKText.configure(background=background_color)
        if text_color not in (None, COLOR_SYSTEM_DEFAULT):
            self.TKText.configure(fg=text_color)
        if font is not None:
            self.TKText.configure(font=font)
        if visible is False:
            self._pack_forget_save_settings()
        elif visible is True:
            self._pack_restore_settings()
        if visible is not None:
            self._visible = visible

    Update = update
