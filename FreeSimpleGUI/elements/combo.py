from __future__ import annotations

import tkinter as tk
import tkinter.font
from tkinter import ttk

import FreeSimpleGUI
from FreeSimpleGUI import COLOR_SYSTEM_DEFAULT
from FreeSimpleGUI import ELEM_TYPE_INPUT_COMBO
from FreeSimpleGUI import Element
from FreeSimpleGUI import theme_button_color
from FreeSimpleGUI._utils import _error_popup_with_traceback


class Combo(Element):
    """
    ComboBox Element - A combination of a single-line input and a drop-down menu. User can type in their own value or choose from list.
    """

    def __init__(
        self,
        values,
        default_value=None,
        size=(None, None),
        s=(None, None),
        auto_size_text=None,
        background_color=None,
        text_color=None,
        button_background_color=None,
        button_arrow_color=None,
        bind_return_key=False,
        change_submits=False,
        enable_events=False,
        enable_per_char_events=None,
        disabled=False,
        key=None,
        k=None,
        pad=None,
        p=None,
        expand_x=False,
        expand_y=False,
        tooltip=None,
        readonly=False,
        font=None,
        visible=True,
        metadata=None,
    ):
        """
        :param values:                  values to choose. While displayed as text, the items returned are what the caller supplied, not text
        :type values:                   List[Any] or Tuple[Any]
        :param default_value:           Choice to be displayed as initial value. Must match one of values variable contents
        :type default_value:            (Any)
        :param size:                    width, height. Width = characters-wide, height = NOTE it's the number of entries to show in the list. If an Int is passed rather than a tuple, then height is auto-set to 1 and width is value of the int
        :type size:                     (int, int)  | (None, None) | int
        :param s:                       Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                        (int, int)  | (None, None) | int
        :param auto_size_text:          True if element should be the same size as the contents
        :type auto_size_text:           (bool)
        :param background_color:        color of background
        :type background_color:         (str)
        :param text_color:              color of the text
        :type text_color:               (str)
        :param button_background_color: The color of the background of the button on the combo box
        :type button_background_color:  (str)
        :param button_arrow_color:      The color of the arrow on the button on the combo box
        :type button_arrow_color:       (str)
        :param bind_return_key:         If True, then the return key will cause a the Combo to generate an event when return key is pressed
        :type bind_return_key:          (bool)
        :param change_submits:          DEPRICATED DO NOT USE. Use `enable_events` instead
        :type change_submits:           (bool)
        :param enable_events:           Turns on the element specific events. Combo event is when a choice is made
        :type enable_events:            (bool)
        :param enable_per_char_events:  Enables generation of events for every character that's input. This is like the Input element's events
        :type enable_per_char_events:   (bool)
        :param disabled:                set disable state for element
        :type disabled:                 (bool)
        :param key:                     Used with window.find_element and with return values to uniquely identify this element
        :type key:                      str | int | tuple | object
        :param k:                       Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                        str | int | tuple | object
        :param pad:                     Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:                      (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                       Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                        (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param expand_x:                If True the element will automatically expand in the X direction to fill available space
        :type expand_x:                 (bool)
        :param expand_y:                If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:                 (bool)
        :param tooltip:                 text that will appear when mouse hovers over this element
        :type tooltip:                  (str)
        :param readonly:                make element readonly (user can't change). True means user cannot change
        :type readonly:                 (bool)
        :param font:                    specifies the font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:                     (str or (str, int[, str]) or None)
        :param visible:                 set visibility state of the element
        :type visible:                  (bool)
        :param metadata:                User metadata that can be set to ANYTHING
        :type metadata:                 (Any)
        """

        self.Values = values
        self.DefaultValue = default_value
        self.ChangeSubmits = change_submits or enable_events
        self.Widget = self.TKCombo = None  # type: ttk.Combobox
        self.Disabled = disabled
        self.Readonly = readonly
        self.BindReturnKey = bind_return_key
        bg = background_color if background_color else FreeSimpleGUI.DEFAULT_INPUT_ELEMENTS_COLOR
        fg = text_color if text_color is not None else FreeSimpleGUI.DEFAULT_INPUT_TEXT_COLOR
        key = key if key is not None else k
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y
        if button_background_color is None:
            self.button_background_color = theme_button_color()[1]
        else:
            self.button_background_color = button_background_color
        if button_arrow_color is None:
            self.button_arrow_color = theme_button_color()[0]
        else:
            self.button_arrow_color = button_arrow_color
        self.enable_per_char_events = enable_per_char_events

        super().__init__(
            ELEM_TYPE_INPUT_COMBO,
            size=sz,
            auto_size_text=auto_size_text,
            background_color=bg,
            text_color=fg,
            key=key,
            pad=pad,
            tooltip=tooltip,
            font=font or FreeSimpleGUI.DEFAULT_FONT,
            visible=visible,
            metadata=metadata,
        )

    def update(
        self,
        value=None,
        values=None,
        set_to_index=None,
        disabled=None,
        readonly=None,
        font=None,
        visible=None,
        size=(None, None),
        select=None,
        text_color=None,
        background_color=None,
    ):
        """
        Changes some of the settings for the Combo Element. Must call `Window.Read` or `Window.Finalize` prior.
        Note that the state can be in 3 states only.... enabled, disabled, readonly even
        though more combinations are available. The easy way to remember is that if you
        change the readonly parameter then you are enabling the element.

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param value:            change which value is current selected based on new list of previous list of choices
        :type value:             (Any)
        :param values:           change list of choices
        :type values:            List[Any]
        :param set_to_index:     change selection to a particular choice starting with index = 0
        :type set_to_index:      (int)
        :param disabled:         disable or enable state of the element
        :type disabled:          (bool)
        :param readonly:         if True make element readonly (user cannot change any choices). Enables the element if either choice are made.
        :type readonly:          (bool)
        :param font:             specifies the font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:              (str or (str, int[, str]) or None)
        :param visible:          control visibility of element
        :type visible:           (bool)
        :param size:             width, height. Width = characters-wide, height = NOTE it's the number of entries to show in the list
        :type size:              (int, int)
        :param select:           if True, then the text will be selected, if False then selection will be cleared
        :type select:            (bool)
        :param background_color: color of background
        :type background_color:  (str)
        :param text_color:       color of the text
        :type text_color:        (str)
        """

        if size != (None, None):
            if isinstance(size, int):
                size = (size, 1)
            if isinstance(size, tuple) and len(size) == 1:
                size = (size[0], 1)

        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Combo.update - The window was closed')
            return

        if values is not None:
            try:
                self.TKCombo['values'] = values
                # self.TKCombo.current(0)       # don't set any value if a new set of values was made
            except:
                pass
            self.Values = values
            if value is None:
                self.TKCombo.set('')
            if size == (None, None):
                max_line_len = max([len(str(line)) for line in self.Values]) if len(self.Values) else 0
                if self.AutoSizeText is False:
                    width = self.Size[0]
                else:
                    width = max_line_len + 1
                self.TKCombo.configure(width=width)
            else:
                self.TKCombo.configure(height=size[1])
                self.TKCombo.configure(width=size[0])
        if value is not None:
            if value not in self.Values:
                self.TKCombo.set(value)
            else:
                for index, v in enumerate(self.Values):
                    if v == value:
                        try:
                            self.TKCombo.current(index)
                        except:
                            pass
                        self.DefaultValue = value
                        break
        if set_to_index is not None:
            try:
                self.TKCombo.current(set_to_index)
                self.DefaultValue = self.Values[set_to_index]
            except:
                pass
        if readonly:
            self.Readonly = True
            self.TKCombo['state'] = 'readonly'
        elif readonly is False:
            self.Readonly = False
            self.TKCombo['state'] = 'enable'
        if disabled is True:
            self.TKCombo['state'] = 'disable'
        elif disabled is False and self.Readonly is True:
            self.TKCombo['state'] = 'readonly'
        elif disabled is False and self.Readonly is False:
            self.TKCombo['state'] = 'enable'
        self.Disabled = disabled if disabled is not None else self.Disabled

        combostyle = self.ttk_style
        style_name = self.ttk_style_name
        if text_color is not None:
            combostyle.configure(style_name, foreground=text_color)
            combostyle.configure(style_name, selectforeground=text_color)
            combostyle.configure(style_name, insertcolor=text_color)
            combostyle.map(style_name, fieldforeground=[('readonly', text_color)])
            self.TextColor = text_color
        if background_color is not None:
            combostyle.configure(style_name, selectbackground=background_color)
            combostyle.map(style_name, fieldbackground=[('readonly', background_color)])
            combostyle.configure(style_name, fieldbackground=background_color)
            self.BackgroundColor = background_color

        if self.Readonly is True:
            if text_color not in (None, COLOR_SYSTEM_DEFAULT):
                combostyle.configure(style_name, selectforeground=text_color)
            if background_color not in (None, COLOR_SYSTEM_DEFAULT):
                combostyle.configure(style_name, selectbackground=background_color)

        if font is not None:
            self.Font = font
            self.TKCombo.configure(font=font)
            self._dropdown_newfont = tkinter.font.Font(font=font)
            self.ParentRowFrame.option_add('*TCombobox*Listbox*Font', self._dropdown_newfont)

        # make tcl call to deal with colors for the drop-down formatting
        try:
            if self.BackgroundColor not in (None, COLOR_SYSTEM_DEFAULT) and self.TextColor not in (
                None,
                COLOR_SYSTEM_DEFAULT,
            ):
                self.Widget.tk.eval(
                    '[ttk::combobox::PopdownWindow {}].f.l configure -foreground {} -background {} -selectforeground {} -selectbackground {} -font {}'.format(
                        self.Widget,
                        self.TextColor,
                        self.BackgroundColor,
                        self.BackgroundColor,
                        self.TextColor,
                        self._dropdown_newfont,
                    )
                )
        except Exception:
            pass  # going to let this one slide

        if visible is False:
            self._pack_forget_save_settings()
            # self.TKCombo.pack_forget()
        elif visible is True:
            self._pack_restore_settings()
            # self.TKCombo.pack(padx=self.pad_used[0], pady=self.pad_used[1])
        if visible is not None:
            self._visible = visible
        if select is True:
            self.TKCombo.select_range(0, tk.END)
        elif select is False:
            self.TKCombo.select_clear()

    def get(self):
        """
        Returns the current (right now) value of the Combo.  DO NOT USE THIS AS THE NORMAL WAY OF READING A COMBO!
        You should be using values from your call to window.read instead.  Know what you're doing if you use it.

        :return: Returns the value of what is currently chosen
        :rtype:  Any | None
        """
        try:
            if self.TKCombo.current() == -1:  # if the current value was not in the original list
                value = self.TKCombo.get()  # then get the value typed in by user
            else:
                value = self.Values[self.TKCombo.current()]  # get value from original list given index
        except:
            value = None  # only would happen if user closes window
        return value

    Get = get
    Update = update
