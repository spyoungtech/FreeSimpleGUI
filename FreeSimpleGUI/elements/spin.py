from __future__ import annotations

import tkinter as tk

import FreeSimpleGUI
from FreeSimpleGUI import ELEM_TYPE_INPUT_SPIN
from FreeSimpleGUI import Element
from FreeSimpleGUI._utils import _error_popup_with_traceback
from FreeSimpleGUI._utils import _exit_mainloop


class Spin(Element):
    """
    A spinner with up/down buttons and a single line of text. Choose 1 values from list
    """

    def __init__(
        self,
        values,
        initial_value=None,
        disabled=False,
        change_submits=False,
        enable_events=False,
        readonly=False,
        size=(None, None),
        s=(None, None),
        auto_size_text=None,
        bind_return_key=None,
        font=None,
        background_color=None,
        text_color=None,
        key=None,
        k=None,
        pad=None,
        p=None,
        wrap=None,
        tooltip=None,
        right_click_menu=None,
        expand_x=False,
        expand_y=False,
        visible=True,
        metadata=None,
    ):
        """
        :param values:           List of valid values
        :type values:            Tuple[Any] or List[Any]
        :param initial_value:    Initial item to show in window. Choose from list of values supplied
        :type initial_value:     (Any)
        :param disabled:         set disable state
        :type disabled:          (bool)
        :param change_submits:   DO NOT USE. Only listed for backwards compat - Use enable_events instead
        :type change_submits:    (bool)
        :param enable_events:    Turns on the element specific events. Spin events happen when an item changes
        :type enable_events:     (bool)
        :param readonly:         If True, then users cannot type in values. Only values from the values list are allowed.
        :type readonly:          (bool)
        :param size:             (w, h) w=characters-wide, h=rows-high. If an int instead of a tuple is supplied, then height is auto-set to 1
        :type size:              (int, int)  | (None, None) | int
        :param s:                Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                 (int, int)  | (None, None) | int
        :param auto_size_text:   if True will size the element to match the length of the text
        :type auto_size_text:    (bool)
        :param bind_return_key:  If True, then the return key will cause a the element to generate an event when return key is pressed
        :type bind_return_key:   (bool)
        :param font:             specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:              (str or (str, int[, str]) or None)
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
        :param wrap:             Determines if the values should "Wrap". Default is False. If True, when reaching last value, will continue back to the first value.
        :type wrap:              (bool)
        :param tooltip:          text, that will appear when mouse hovers over the element
        :type tooltip:           (str)
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

        self.Values = values
        self.DefaultValue = initial_value
        self.ChangeSubmits = change_submits or enable_events
        self.TKSpinBox = self.Widget = None  # type: tk.Spinbox
        self.Disabled = disabled
        self.Readonly = readonly
        self.RightClickMenu = right_click_menu
        self.BindReturnKey = bind_return_key
        self.wrap = wrap

        bg = background_color if background_color else FreeSimpleGUI.DEFAULT_INPUT_ELEMENTS_COLOR
        fg = text_color if text_color is not None else FreeSimpleGUI.DEFAULT_INPUT_TEXT_COLOR
        key = key if key is not None else k
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y

        super().__init__(
            ELEM_TYPE_INPUT_SPIN,
            size=sz,
            auto_size_text=auto_size_text,
            font=font,
            background_color=bg,
            text_color=fg,
            key=key,
            pad=pad,
            tooltip=tooltip,
            visible=visible,
            metadata=metadata,
        )
        return

    def update(self, value=None, values=None, disabled=None, readonly=None, visible=None):
        """
        Changes some of the settings for the Spin Element. Must call `Window.Read` or `Window.Finalize` prior
        Note that the state can be in 3 states only.... enabled, disabled, readonly even
        though more combinations are available. The easy way to remember is that if you
        change the readonly parameter then you are enabling the element.

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param value:    set the current value from list of choices
        :type value:     (Any)
        :param values:   set available choices
        :type values:    List[Any]
        :param disabled: disable. Note disabled and readonly cannot be mixed. It must be one OR the other
        :type disabled:  (bool)
        :param readonly: make element readonly.  Note disabled and readonly cannot be mixed. It must be one OR the other
        :type readonly:  (bool)
        :param visible:  control visibility of element
        :type visible:   (bool)
        """

        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Spin.update - The window was closed')
            return

        if values is not None:
            old_value = self.TKStringVar.get()
            self.Values = values
            self.TKSpinBox.configure(values=values)
            self.TKStringVar.set(old_value)
        if value is not None:
            try:
                self.TKStringVar.set(value)
                self.DefaultValue = value
            except:
                pass

        if readonly is True:
            self.Readonly = True
            self.TKSpinBox['state'] = 'readonly'
        elif readonly is False:
            self.Readonly = False
            self.TKSpinBox['state'] = 'normal'
        if disabled is True:
            self.TKSpinBox['state'] = 'disable'
        elif disabled is False:
            if self.Readonly:
                self.TKSpinBox['state'] = 'readonly'
            else:
                self.TKSpinBox['state'] = 'normal'
        self.Disabled = disabled if disabled is not None else self.Disabled

        if visible is False:
            self._pack_forget_save_settings()
        elif visible is True:
            self._pack_restore_settings()
        if visible is not None:
            self._visible = visible

    def _SpinChangedHandler(self, event):
        """
        Callback function. Used internally only. Called by tkinter when Spinbox Widget changes.  Results in Window.Read() call returning

        :param event: passed in from tkinter
        :type event:
        """
        # first, get the results table built
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = ''
        self.ParentForm.FormRemainedOpen = True
        _exit_mainloop(self.ParentForm)
        # if self.ParentForm.CurrentlyRunningMainloop:
        #     Window._window_that_exited = self.ParentForm
        #     self.ParentForm.TKroot.quit()  # kick the users out of the mainloop

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
        Return the current chosen value showing in spinbox.
        This value will be the same as what was provided as list of choices.  If list items are ints, then the
        item returned will be an int (not a string)

        :return: The currently visible entry
        :rtype:  (Any)
        """
        value = self.TKStringVar.get()
        for v in self.Values:
            if str(v) == value:
                value = v
                break
        return value

    Get = get
    Update = update
