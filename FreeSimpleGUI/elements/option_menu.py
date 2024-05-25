from __future__ import annotations

import tkinter as tk

import FreeSimpleGUI
from FreeSimpleGUI import ELEM_TYPE_INPUT_OPTION_MENU
from FreeSimpleGUI import Element
from FreeSimpleGUI._utils import _error_popup_with_traceback


class OptionMenu(Element):
    """
    Option Menu is an Element available ONLY on the tkinter port of PySimpleGUI.  It is a widget that is unique
    to tkinter.  However, it looks much like a ComboBox.  Instead of an arrow to click to pull down the list of
    choices, another little graphic is shown on the widget to indicate where you click.  After clicking to activate,
    it looks like a Combo Box that you scroll to select a choice.
    """

    def __init__(
        self,
        values,
        default_value=None,
        size=(None, None),
        s=(None, None),
        disabled=False,
        auto_size_text=None,
        expand_x=False,
        expand_y=False,
        background_color=None,
        text_color=None,
        key=None,
        k=None,
        pad=None,
        p=None,
        tooltip=None,
        visible=True,
        metadata=None,
    ):
        """
        :param values:           Values to be displayed
        :type values:            List[Any] or Tuple[Any]
        :param default_value:    the value to choose by default
        :type default_value:     (Any)
        :param size:             (width, height) size in characters (wide), height is ignored and present to be consistent with other elements
        :type size:              (int, int) (width, UNUSED)
        :param s:                Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                 (int, int)  | (None, None) | int
        :param disabled:         control enabled / disabled
        :type disabled:          (bool)
        :param auto_size_text:   True if size of Element should match the contents of the items
        :type auto_size_text:    (bool)
        :param expand_x:         If True the element will automatically expand in the X direction to fill available space
        :type expand_x:          (bool)
        :param expand_y:         If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:          (bool)
        :param background_color: color of background
        :type background_color:  (str)
        :param text_color:       color of the text
        :type text_color:        (str)
        :param key:              Used with window.find_element and with return values to uniquely identify this element
        :type key:               str | int | tuple | object
        :param k:                Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                 str | int | tuple | object
        :param pad:              Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:               (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                 (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param tooltip:          text that will appear when mouse hovers over this element
        :type tooltip:           (str)
        :param visible:          set visibility state of the element
        :type visible:           (bool)
        :param metadata:         User metadata that can be set to ANYTHING
        :type metadata:          (Any)
        """

        self.Values = values
        self.DefaultValue = default_value
        self.Widget = self.TKOptionMenu = None  # type: tk.OptionMenu
        self.Disabled = disabled
        bg = background_color if background_color else FreeSimpleGUI.DEFAULT_INPUT_ELEMENTS_COLOR
        fg = text_color if text_color is not None else FreeSimpleGUI.DEFAULT_INPUT_TEXT_COLOR
        key = key if key is not None else k
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y

        super().__init__(
            ELEM_TYPE_INPUT_OPTION_MENU,
            size=sz,
            auto_size_text=auto_size_text,
            background_color=bg,
            text_color=fg,
            key=key,
            pad=pad,
            tooltip=tooltip,
            visible=visible,
            metadata=metadata,
        )

    def update(self, value=None, values=None, disabled=None, visible=None, size=(None, None)):
        """
        Changes some of the settings for the OptionMenu Element. Must call `Window.Read` or `Window.Finalize` prior

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param value:    the value to choose by default
        :type value:     (Any)
        :param values:   Values to be displayed
        :type values:    List[Any]
        :param disabled: disable or enable state of the element
        :type disabled:  (bool)
        :param visible:  control visibility of element
        :type visible:   (bool)
        :param size:     (width, height) size in characters (wide), height is ignored and present to be consistent with other elements
        :type size:      (int, int) (width, UNUSED)
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in OptionMenu.update - The window was closed')
            return

        if values is not None:
            self.Values = values
            self.TKOptionMenu['menu'].delete(0, 'end')

            # Insert list of new options (tk._setit hooks them up to var)
            # self.TKStringVar.set(self.Values[0])
            for new_value in self.Values:
                self.TKOptionMenu['menu'].add_command(label=new_value, command=tk._setit(self.TKStringVar, new_value))
            if value is None:
                self.TKStringVar.set('')

            if size == (None, None):
                max_line_len = max([len(str(line)) for line in self.Values]) if len(self.Values) else 0
                if self.AutoSizeText is False:
                    width = self.Size[0]
                else:
                    width = max_line_len + 1
                self.TKOptionMenu.configure(width=width)
            else:
                self.TKOptionMenu.configure(width=size[0])

        if value is not None:
            self.DefaultValue = value
            self.TKStringVar.set(value)

        if disabled is True:
            self.TKOptionMenu['state'] = 'disabled'
        elif disabled is False:
            self.TKOptionMenu['state'] = 'normal'
        self.Disabled = disabled if disabled is not None else self.Disabled
        if visible is False:
            self._pack_forget_save_settings()
            # self.TKOptionMenu.pack_forget()
        elif visible is True:
            self._pack_restore_settings()
            # self.TKOptionMenu.pack(padx=self.pad_used[0], pady=self.pad_used[1])
        if visible is not None:
            self._visible = visible

    Update = update
