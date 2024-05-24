from __future__ import annotations

import tkinter as tk

import FreeSimpleGUI
from FreeSimpleGUI import COLOR_SYSTEM_DEFAULT
from FreeSimpleGUI import ELEM_TYPE_INPUT_TEXT
from FreeSimpleGUI import Element
from FreeSimpleGUI._utils import _error_popup_with_traceback


class Input(Element):
    """
    Display a single text input field.  Based on the tkinter Widget `Entry`
    """

    def __init__(
        self,
        default_text='',
        size=(None, None),
        s=(None, None),
        disabled=False,
        password_char='',
        justification=None,
        background_color=None,
        text_color=None,
        font=None,
        tooltip=None,
        border_width=None,
        change_submits=False,
        enable_events=False,
        do_not_clear=True,
        key=None,
        k=None,
        focus=False,
        pad=None,
        p=None,
        use_readonly_for_disable=True,
        readonly=False,
        disabled_readonly_background_color=None,
        disabled_readonly_text_color=None,
        selected_text_color=None,
        selected_background_color=None,
        expand_x=False,
        expand_y=False,
        right_click_menu=None,
        visible=True,
        metadata=None,
    ):
        """
        :param default_text:                       Text initially shown in the input box as a default value(Default value = ''). Will automatically be converted to string
        :type default_text:                        (Any)
        :param size:                               w=characters-wide, h=rows-high. If an int is supplied rather than a tuple, then a tuple is created width=int supplied and heigh=1
        :type size:                                (int, int) |  (int, None) | int
        :param s:                                  Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                                   (int, int)  | (None, None) | int
        :param disabled:                           set disable state for element (Default = False)
        :type disabled:                            (bool)
        :param password_char:                      Password character if this is a password field (Default value = '')
        :type password_char:                       (char)
        :param justification:                      justification for data display. Valid choices - left, right, center
        :type justification:                       (str)
        :param background_color:                   color of background in one of the color formats
        :type background_color:                    (str)
        :param text_color:                         color of the text
        :type text_color:                          (str)
        :param font:                               specifies the font family, size. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:                                (str or (str, int[, str]) or None)
        :param tooltip:                            text, that will appear when mouse hovers over the element
        :type tooltip:                             (str)
        :param border_width:                       width of border around element in pixels
        :type border_width:                        (int)
        :param change_submits:                     * DEPRICATED DO NOT USE. Use `enable_events` instead
        :type change_submits:                      (bool)
        :param enable_events:                      If True then changes to this element are immediately reported as an event. Use this instead of change_submits (Default = False)
        :type enable_events:                       (bool)
        :param do_not_clear:                       If False then the field will be set to blank after ANY event (button, any event) (Default = True)
        :type do_not_clear:                        (bool)
        :param key:                                Value that uniquely identifies this element from all other elements. Used when Finding an element or in return values. Must be unique to the window
        :type key:                                 str | int | tuple | object
        :param k:                                  Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                                   str | int | tuple | object
        :param focus:                              Determines if initial focus should go to this element.
        :type focus:                               (bool)
        :param pad:                                Amount of padding to put around element. Normally (horizontal pixels, vertical pixels) but can be split apart further into ((horizontal left, horizontal right), (vertical above, vertical below)). If int is given, then converted to tuple (int, int) with the value provided duplicated
        :type pad:                                 (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                                  Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                                   (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param use_readonly_for_disable:           If True (the default) tkinter state set to 'readonly'. Otherwise state set to 'disabled'
        :type use_readonly_for_disable:            (bool)
        :param readonly:                           If True tkinter state set to 'readonly'.  Use this in place of use_readonly_for_disable as another way of achieving readonly.  Note cannot set BOTH readonly and disabled as tkinter only supplies a single flag
        :type readonly:                            (bool)
        :param disabled_readonly_background_color: If state is set to readonly or disabled, the color to use for the background
        :type disabled_readonly_background_color:  (str)
        :param disabled_readonly_text_color:       If state is set to readonly or disabled, the color to use for the text
        :type disabled_readonly_text_color:        (str)
        :param selected_text_color:                Color of text when it is selected (using mouse or control+A, etc)
        :type selected_text_color:                 (str)
        :param selected_background_color:          Color of background when it is selected (using mouse or control+A, etc)
        :type selected_background_color:           (str)
        :param expand_x:                           If True the element will automatically expand in the X direction to fill available space
        :type expand_x:                            (bool)
        :param expand_y:                           If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:                            (bool)
        :param right_click_menu:                   A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type right_click_menu:                    List[List[ List[str] | str ]]
        :param visible:                            set visibility state of the element (Default = True)
        :type visible:                             (bool)
        :param metadata:                           User metadata that can be set to ANYTHING
        :type metadata:                            (Any)
        """

        self.DefaultText = default_text if default_text is not None else ''
        self.PasswordCharacter = password_char
        bg = background_color if background_color is not None else FreeSimpleGUI.DEFAULT_INPUT_ELEMENTS_COLOR
        fg = text_color if text_color is not None else FreeSimpleGUI.DEFAULT_INPUT_TEXT_COLOR
        self.selected_text_color = selected_text_color
        self.selected_background_color = selected_background_color
        self.Focus = focus
        self.do_not_clear = do_not_clear
        self.Justification = justification
        self.Disabled = disabled
        self.ChangeSubmits = change_submits or enable_events
        self.RightClickMenu = right_click_menu
        self.UseReadonlyForDisable = use_readonly_for_disable
        self.disabled_readonly_background_color = disabled_readonly_background_color
        self.disabled_readonly_text_color = disabled_readonly_text_color
        self.ReadOnly = readonly
        self.BorderWidth = border_width if border_width is not None else FreeSimpleGUI.DEFAULT_BORDER_WIDTH
        self.TKEntry = self.Widget = None  # type: tk.Entry
        key = key if key is not None else k
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y

        super().__init__(
            ELEM_TYPE_INPUT_TEXT,
            size=sz,
            background_color=bg,
            text_color=fg,
            key=key,
            pad=pad,
            font=font,
            tooltip=tooltip,
            visible=visible,
            metadata=metadata,
        )

    def update(
        self,
        value=None,
        disabled=None,
        select=None,
        visible=None,
        text_color=None,
        background_color=None,
        font=None,
        move_cursor_to='end',
        password_char=None,
        paste=None,
        readonly=None,
    ):
        """
        Changes some of the settings for the Input Element. Must call `Window.Read` or `Window.Finalize` prior.
        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param value:            new text to display as default text in Input field
        :type value:             (str)
        :param disabled:         disable or enable state of the element (sets Entry Widget to readonly or normal)
        :type disabled:          (bool)
        :param select:           if True, then the text will be selected
        :type select:            (bool)
        :param visible:          change visibility of element
        :type visible:           (bool)
        :param text_color:       change color of text being typed
        :type text_color:        (str)
        :param background_color: change color of the background
        :type background_color:  (str)
        :param font:             specifies the font family, size. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:              (str or (str, int[, str]) or None)
        :param move_cursor_to:   Moves the cursor to a particular offset. Defaults to 'end'
        :type move_cursor_to:    int | str
        :param password_char:    Password character if this is a password field
        :type password_char:     str
        :param paste:            If True "Pastes" the value into the element rather than replacing the entire element. If anything is selected it is replaced. The text is inserted at the current cursor location.
        :type paste:             bool
        :param readonly:         if True make element readonly (user cannot change any choices). Enables the element if either choice are made.
        :type readonly:          (bool)
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Input.update - The window was closed')
            return

        if background_color not in (None, COLOR_SYSTEM_DEFAULT):
            self.TKEntry.configure(background=background_color)
            self.BackgroundColor = background_color
        if text_color not in (None, COLOR_SYSTEM_DEFAULT):
            self.TKEntry.configure(fg=text_color)
            self.TextColor = text_color

        if disabled is True:
            if self.UseReadonlyForDisable:
                if self.disabled_readonly_text_color not in (None, COLOR_SYSTEM_DEFAULT):
                    self.TKEntry.configure(fg=self.disabled_readonly_text_color)
                self.TKEntry['state'] = 'readonly'
            else:
                if self.TextColor not in (None, COLOR_SYSTEM_DEFAULT):
                    self.TKEntry.configure(fg=self.TextColor)
                self.TKEntry['state'] = 'disabled'
            self.Disabled = True
        elif disabled is False:
            self.TKEntry['state'] = 'normal'
            if self.TextColor not in (None, COLOR_SYSTEM_DEFAULT):
                self.TKEntry.configure(fg=self.TextColor)
            self.Disabled = False

        if readonly is True:
            self.TKEntry['state'] = 'readonly'
        elif readonly is False:
            self.TKEntry['state'] = 'normal'

        if value is not None:
            if paste is not True:
                try:
                    self.TKStringVar.set(value)
                except:
                    pass
            self.DefaultText = value
            if paste is True:
                try:
                    self.TKEntry.delete('sel.first', 'sel.last')
                except:
                    pass
                self.TKEntry.insert('insert', value)
            if move_cursor_to == 'end':
                self.TKEntry.icursor(tk.END)
            elif move_cursor_to is not None:
                self.TKEntry.icursor(move_cursor_to)
        if select:
            self.TKEntry.select_range(0, 'end')
        if visible is False:
            self._pack_forget_save_settings()
            # self.TKEntry.pack_forget()
        elif visible is True:
            self._pack_restore_settings()
            # self.TKEntry.pack(padx=self.pad_used[0], pady=self.pad_used[1])
            # self.TKEntry.pack(padx=self.pad_used[0], pady=self.pad_used[1], in_=self.ParentRowFrame)
        if visible is not None:
            self._visible = visible
        if password_char is not None:
            self.TKEntry.configure(show=password_char)
            self.PasswordCharacter = password_char
        if font is not None:
            self.TKEntry.configure(font=font)

    def set_ibeam_color(self, ibeam_color=None):
        """
        Sets the color of the I-Beam that is used to "insert" characters. This is oftens called a "Cursor" by
        many users.  To keep from being confused with tkinter's definition of cursor (the mouse pointer), the term
        ibeam is used in this case.
        :param ibeam_color: color to set the "I-Beam" used to indicate where characters will be inserted
        :type ibeam_color:  (str)
        """

        if not self._widget_was_created():
            return
        if ibeam_color is not None:
            try:
                self.Widget.config(insertbackground=ibeam_color)
            except Exception:
                _error_popup_with_traceback(
                    'Error setting I-Beam color in set_ibeam_color',
                    'The element has a key:',
                    self.Key,
                    'The color passed in was:',
                    ibeam_color,
                )

    def get(self):
        """
        Read and return the current value of the input element. Must call `Window.Read` or `Window.Finalize` prior

        :return: current value of Input field or '' if error encountered
        :rtype:  (str)
        """
        try:
            text = self.TKStringVar.get()
        except:
            text = ''
        return text

    Get = get
    Update = update
