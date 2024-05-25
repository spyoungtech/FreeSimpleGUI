from __future__ import annotations

import os
import tkinter as tk
import warnings
from typing import Any  # noqa

import FreeSimpleGUI
from FreeSimpleGUI import COLOR_SYSTEM_DEFAULT
from FreeSimpleGUI import ELEM_TYPE_BUTTON
from FreeSimpleGUI import ELEM_TYPE_COLUMN
from FreeSimpleGUI import ELEM_TYPE_FRAME
from FreeSimpleGUI import ELEM_TYPE_GRAPH
from FreeSimpleGUI import ELEM_TYPE_PANE
from FreeSimpleGUI import ELEM_TYPE_TAB
from FreeSimpleGUI import ELEM_TYPE_TAB_GROUP
from FreeSimpleGUI import MENU_RIGHT_CLICK_DISABLED
from FreeSimpleGUI import popup_error_with_traceback
from FreeSimpleGUI import PSG_THEME_PART_BACKGROUND
from FreeSimpleGUI import PSG_THEME_PART_BUTTON_BACKGROUND
from FreeSimpleGUI import PSG_THEME_PART_BUTTON_TEXT
from FreeSimpleGUI import PSG_THEME_PART_INPUT_BACKGROUND
from FreeSimpleGUI import PSG_THEME_PART_INPUT_TEXT
from FreeSimpleGUI import PSG_THEME_PART_SLIDER
from FreeSimpleGUI import PSG_THEME_PART_TEXT
from FreeSimpleGUI import pysimplegui_user_settings
from FreeSimpleGUI import running_mac
from FreeSimpleGUI import theme_background_color
from FreeSimpleGUI import theme_button_color_background
from FreeSimpleGUI import theme_button_color_text
from FreeSimpleGUI import theme_input_background_color
from FreeSimpleGUI import theme_input_text_color
from FreeSimpleGUI import theme_slider_color
from FreeSimpleGUI import theme_text_color
from FreeSimpleGUI import TITLEBAR_CLOSE_KEY
from FreeSimpleGUI import TITLEBAR_MAXIMIZE_KEY
from FreeSimpleGUI import TITLEBAR_MINIMIZE_KEY
from FreeSimpleGUI import ToolTip
from FreeSimpleGUI import ttk_part_mapping_dict
from FreeSimpleGUI import TTK_SCROLLBAR_PART_ARROW_BUTTON_ARROW_COLOR
from FreeSimpleGUI import TTK_SCROLLBAR_PART_ARROW_WIDTH
from FreeSimpleGUI import TTK_SCROLLBAR_PART_BACKGROUND_COLOR
from FreeSimpleGUI import TTK_SCROLLBAR_PART_FRAME_COLOR
from FreeSimpleGUI import TTK_SCROLLBAR_PART_RELIEF
from FreeSimpleGUI import TTK_SCROLLBAR_PART_SCROLL_WIDTH
from FreeSimpleGUI import TTK_SCROLLBAR_PART_TROUGH_COLOR
from FreeSimpleGUI import TTKPartOverrides


class Element:
    """The base class for all Elements. Holds the basic description of an Element like size and colors"""

    def __init__(
        self,
        type,
        size=(None, None),
        auto_size_text=None,
        font=None,
        background_color=None,
        text_color=None,
        key=None,
        pad=None,
        tooltip=None,
        visible=True,
        metadata=None,
        sbar_trough_color=None,
        sbar_background_color=None,
        sbar_arrow_color=None,
        sbar_width=None,
        sbar_arrow_width=None,
        sbar_frame_color=None,
        sbar_relief=None,
    ):
        """
        Element base class. Only used internally.  User will not create an Element object by itself

        :param type:                        The type of element. These constants all start with "ELEM_TYPE_"
        :type type:                         (int) (could be enum)
        :param size:                        w=characters-wide, h=rows-high. If an int instead of a tuple is supplied, then height is auto-set to 1
        :type size:                         (int, int) | (None, None) | int
        :param auto_size_text:              True if the Widget should be shrunk to exactly fit the number of chars to show
        :type auto_size_text:               bool
        :param font:                        specifies the font family, size. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:                         (str or (str, int[, str]) or None)
        :param background_color:            color of background. Can be in #RRGGBB format or a color name "black"
        :type background_color:             (str)
        :param text_color:                  element's text color. Can be in #RRGGBB format or a color name "black"
        :type text_color:                   (str)
        :param key:                         Identifies an Element. Should be UNIQUE to this window.
        :type key:                          str | int | tuple | object
        :param pad:                         Amount of padding to put around element in pixels (left/right, top/bottom). If an int is given, then auto-converted to tuple (int, int)
        :type pad:                          (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param tooltip:                     text, that will appear when mouse hovers over the element
        :type tooltip:                      (str)
        :param visible:                     set visibility state of the element (Default = True)
        :type visible:                      (bool)
        :param metadata:                    User metadata that can be set to ANYTHING
        :type metadata:                     (Any)
        :param sbar_trough_color:           Scrollbar color of the trough
        :type sbar_trough_color:            (str)
        :param sbar_background_color:       Scrollbar color of the background of the arrow buttons at the ends AND the color of the "thumb" (the thing you grab and slide). Switches to arrow color when mouse is over
        :type sbar_background_color:        (str)
        :param sbar_arrow_color:            Scrollbar color of the arrow at the ends of the scrollbar (it looks like a button). Switches to background color when mouse is over
        :type sbar_arrow_color:             (str)
        :param sbar_width:                  Scrollbar width in pixels
        :type sbar_width:                   (int)
        :param sbar_arrow_width:            Scrollbar width of the arrow on the scrollbar. It will potentially impact the overall width of the scrollbar
        :type sbar_arrow_width:             (int)
        :param sbar_frame_color:            Scrollbar Color of frame around scrollbar (available only on some ttk themes)
        :type sbar_frame_color:             (str)
        :param sbar_relief:                 Scrollbar relief that will be used for the "thumb" of the scrollbar (the thing you grab that slides). Should be a constant that is defined at starting with "RELIEF_" - RELIEF_RAISED, RELIEF_SUNKEN, RELIEF_FLAT, RELIEF_RIDGE, RELIEF_GROOVE, RELIEF_SOLID
        :type sbar_relief:                  (str)
        """

        if size is not None and size != (None, None):
            if isinstance(size, int):
                size = (size, 1)
            if isinstance(size, tuple) and len(size) == 1:
                size = (size[0], 1)

        if pad is not None and pad != (None, None):
            if isinstance(pad, int):
                pad = (pad, pad)

        self.Size = size
        self.Type = type
        self.AutoSizeText = auto_size_text

        self.Pad = pad
        self.Font = font

        self.TKStringVar = None
        self.TKIntVar = None
        self.TKText = None
        self.TKEntry = None
        self.TKImage = None
        self.ttk_style_name = ''  # The ttk style name (if this is a ttk widget)
        self.ttk_style = None  # The ttk Style object (if this is a ttk widget)
        self._metadata = None  # type: Any

        self.ParentForm = None  # type: Window
        self.ParentContainer = None  # will be a Form, Column, or Frame element # UNBIND
        self.TextInputDefault = None
        self.Position = (0, 0)  # Default position Row 0, Col 0
        self.BackgroundColor = background_color if background_color is not None else FreeSimpleGUI.DEFAULT_ELEMENT_BACKGROUND_COLOR
        self.TextColor = text_color if text_color is not None else FreeSimpleGUI.DEFAULT_ELEMENT_TEXT_COLOR
        self.Key = key  # dictionary key for return values
        self.Tooltip = tooltip
        self.TooltipObject = None
        self._visible = visible
        self.TKRightClickMenu = None
        self.Widget = None  # Set when creating window. Has the main tkinter widget for element
        self.Tearoff = False  # needed because of right click menu code
        self.ParentRowFrame = None  # type tk.Frame
        self.metadata = metadata
        self.user_bind_dict = {}  # Used when user defines a tkinter binding using bind method - convert bind string to key modifier
        self.user_bind_event = None  # Used when user defines a tkinter binding using bind method - event data from tkinter
        # self.pad_used = (0, 0)  # the amount of pad used when was inserted into the layout
        self._popup_menu_location = (None, None)
        self.pack_settings = None
        self.vsb_style_name = None  # ttk style name used for the verical scrollbar if one is attached to element
        self.hsb_style_name = None  # ttk style name used for the horizontal scrollbar if one is attached to element
        self.vsb_style = None  # The ttk style used for the vertical scrollbar if one is attached to element
        self.hsb_style = None  # The ttk style used for the horizontal scrollbar if one is attached to element
        self.hsb = None  # The horizontal scrollbar if one is attached to element
        self.vsb = None  # The vertical scrollbar if one is attached to element
        ## TTK Scrollbar Settings
        self.ttk_part_overrides = TTKPartOverrides(
            sbar_trough_color=sbar_trough_color,
            sbar_background_color=sbar_background_color,
            sbar_arrow_color=sbar_arrow_color,
            sbar_width=sbar_width,
            sbar_arrow_width=sbar_arrow_width,
            sbar_frame_color=sbar_frame_color,
            sbar_relief=sbar_relief,
        )

        PSG_THEME_PART_FUNC_MAP = {
            PSG_THEME_PART_BACKGROUND: theme_background_color,
            PSG_THEME_PART_BUTTON_BACKGROUND: theme_button_color_background,
            PSG_THEME_PART_BUTTON_TEXT: theme_button_color_text,
            PSG_THEME_PART_INPUT_BACKGROUND: theme_input_background_color,
            PSG_THEME_PART_INPUT_TEXT: theme_input_text_color,
            PSG_THEME_PART_TEXT: theme_text_color,
            PSG_THEME_PART_SLIDER: theme_slider_color,
        }

        # class Theme_Parts():
        #     PSG_THEME_PART_FUNC_MAP = {PSG_THEME_PART_BACKGROUND: theme_background_color,
        if sbar_trough_color is not None:
            self.scroll_trough_color = sbar_trough_color
        else:
            self.scroll_trough_color = PSG_THEME_PART_FUNC_MAP.get(
                ttk_part_mapping_dict[TTK_SCROLLBAR_PART_TROUGH_COLOR],
                ttk_part_mapping_dict[TTK_SCROLLBAR_PART_TROUGH_COLOR],
            )
            if callable(self.scroll_trough_color):
                self.scroll_trough_color = self.scroll_trough_color()

        if sbar_background_color is not None:
            self.scroll_background_color = sbar_background_color
        else:
            self.scroll_background_color = PSG_THEME_PART_FUNC_MAP.get(
                ttk_part_mapping_dict[TTK_SCROLLBAR_PART_BACKGROUND_COLOR],
                ttk_part_mapping_dict[TTK_SCROLLBAR_PART_BACKGROUND_COLOR],
            )
            if callable(self.scroll_background_color):
                self.scroll_background_color = self.scroll_background_color()

        if sbar_arrow_color is not None:
            self.scroll_arrow_color = sbar_arrow_color
        else:
            self.scroll_arrow_color = PSG_THEME_PART_FUNC_MAP.get(
                ttk_part_mapping_dict[TTK_SCROLLBAR_PART_ARROW_BUTTON_ARROW_COLOR],
                ttk_part_mapping_dict[TTK_SCROLLBAR_PART_ARROW_BUTTON_ARROW_COLOR],
            )
            if callable(self.scroll_arrow_color):
                self.scroll_arrow_color = self.scroll_arrow_color()

        if sbar_frame_color is not None:
            self.scroll_frame_color = sbar_frame_color
        else:
            self.scroll_frame_color = PSG_THEME_PART_FUNC_MAP.get(
                ttk_part_mapping_dict[TTK_SCROLLBAR_PART_FRAME_COLOR],
                ttk_part_mapping_dict[TTK_SCROLLBAR_PART_FRAME_COLOR],
            )
            if callable(self.scroll_frame_color):
                self.scroll_frame_color = self.scroll_frame_color()

        if sbar_relief is not None:
            self.scroll_relief = sbar_relief
        else:
            self.scroll_relief = ttk_part_mapping_dict[TTK_SCROLLBAR_PART_RELIEF]

        if sbar_width is not None:
            self.scroll_width = sbar_width
        else:
            self.scroll_width = ttk_part_mapping_dict[TTK_SCROLLBAR_PART_SCROLL_WIDTH]

        if sbar_arrow_width is not None:
            self.scroll_arrow_width = sbar_arrow_width
        else:
            self.scroll_arrow_width = ttk_part_mapping_dict[TTK_SCROLLBAR_PART_ARROW_WIDTH]

        if not hasattr(self, 'DisabledTextColor'):
            self.DisabledTextColor = None
        if not hasattr(self, 'ItemFont'):
            self.ItemFont = None
        if not hasattr(self, 'RightClickMenu'):
            self.RightClickMenu = None
        if not hasattr(self, 'Disabled'):
            self.Disabled = None  # in case the element hasn't defined this, add it here

    @property
    def visible(self):
        """
        Returns visibility state for the element.  This is a READONLY property
        :return: Visibility state for element
        :rtype:  (bool)
        """
        return self._visible

    @property
    def metadata(self):
        """
        Metadata is an Element property that you can use at any time to hold any value
        :return: the current metadata value
        :rtype:  (Any)
        """
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        """
         Metadata is an Element property that you can use at any time to hold any value
        :param value: Anything you want it to be
        :type value:  (Any)
        """
        self._metadata = value

    @property
    def key(self):
        """
        Returns key for the element.  This is a READONLY property.
        Keys can be any hashable object (basically anything except a list... tuples are ok, but not lists)
        :return: The window's Key
        :rtype:  (Any)
        """
        return self.Key

    @property
    def widget(self):
        """
        Returns tkinter widget for the element.  This is a READONLY property.
        The implementation is that the Widget member variable is returned. This is a backward compatible addition
        :return:    The element's underlying tkinter widget
        :rtype:     (tkinter.Widget)
        """
        return self.Widget

    def _RightClickMenuCallback(self, event):
        """
        Callback function that's called when a right click happens. Shows right click menu as result

        :param event: information provided by tkinter about the event including x,y location of click
        :type event:

        """
        if self.Type == ELEM_TYPE_TAB_GROUP:
            try:
                index = self.Widget.index(f'@{event.x},{event.y}')
                tab = self.Widget.tab(index, 'text')
                key = self.find_key_from_tab_name(tab)
                tab_element = self.ParentForm.key_dict[key]
                if tab_element.RightClickMenu is None:  # if this tab didn't explicitly have a menu, then don't show anything
                    return
                tab_element.TKRightClickMenu.tk_popup(event.x_root, event.y_root, 0)
                self.TKRightClickMenu.grab_release()
            except:
                pass
            return
        self.TKRightClickMenu.tk_popup(event.x_root, event.y_root, 0)
        self.TKRightClickMenu.grab_release()
        if self.Type == ELEM_TYPE_GRAPH:
            self._update_position_for_returned_values(event)

    def _tearoff_menu_callback(self, parent, menu):
        """
        Callback function that's called when a right click menu is torn off.
        The reason for this function is to relocate the torn-off menu. It will default to 0,0 otherwise
        This callback moves the right click menu window to the location of the current window

        :param parent: information provided by tkinter - the parent of the Meny
        :type parent:
        :param menu:   information provided by tkinter - the menu window
        :type menu:

        """
        if self._popup_menu_location == (None, None):
            winx, winy = self.ParentForm.current_location()
        else:
            winx, winy = self._popup_menu_location
        # self.ParentForm.TKroot.update()
        self.ParentForm.TKroot.tk.call('wm', 'geometry', menu, f'+{winx}+{winy}')

    def _MenuItemChosenCallback(self, item_chosen):  # TEXT Menu item callback
        """
        Callback function called when user chooses a menu item from menubar, Button Menu or right click menu

        :param item_chosen: String holding the value chosen.
        :type item_chosen:  str

        """
        # print('IN MENU ITEM CALLBACK', item_chosen)
        self.MenuItemChosen = item_chosen
        self.ParentForm.LastButtonClicked = self.MenuItemChosen
        self.ParentForm.FormRemainedOpen = True
        _exit_mainloop(self.ParentForm)
        # Window._window_that_exited = self.ParentForm
        # self.ParentForm.TKroot.quit()  # kick the users out of the mainloop

    def _FindReturnKeyBoundButton(self, form):
        """
        Searches for which Button has the flag Button.BindReturnKey set.  It is called recursively when a
        "Container Element" is encountered. Func has to walk entire window including these "sub-forms"

        :param form: the Window object to search
        :type form:
        :return:     Button Object if a button is found, else None
        :rtype:      Button | None
        """
        for row in form.Rows:
            for element in row:
                if element.Type == ELEM_TYPE_BUTTON:
                    if element.BindReturnKey:
                        return element
                if element.Type == ELEM_TYPE_COLUMN:
                    rc = self._FindReturnKeyBoundButton(element)
                    if rc is not None:
                        return rc
                if element.Type == ELEM_TYPE_FRAME:
                    rc = self._FindReturnKeyBoundButton(element)
                    if rc is not None:
                        return rc
                if element.Type == ELEM_TYPE_TAB_GROUP:
                    rc = self._FindReturnKeyBoundButton(element)
                    if rc is not None:
                        return rc
                if element.Type == ELEM_TYPE_TAB:
                    rc = self._FindReturnKeyBoundButton(element)
                    if rc is not None:
                        return rc
                if element.Type == ELEM_TYPE_PANE:
                    rc = self._FindReturnKeyBoundButton(element)
                    if rc is not None:
                        return rc
        return None

    def _TextClickedHandler(self, event):
        """
        Callback that's called when a text element is clicked on with events enabled on the Text Element.
        Result is that control is returned back to user (quits mainloop).

        :param event:
        :type event:

        """
        # If this is a minimize button for a custom titlebar, then minimize the window
        if self.Key in (TITLEBAR_MINIMIZE_KEY, TITLEBAR_MAXIMIZE_KEY, TITLEBAR_CLOSE_KEY):
            self.ParentForm._custom_titlebar_callback(self.Key)
        self._generic_callback_handler(self.DisplayText)
        return

    def _ReturnKeyHandler(self, event):
        """
        Internal callback for the ENTER / RETURN key. Results in calling the ButtonCallBack for element that has the return key bound to it, just as if button was clicked.

        :param event:
        :type event:

        """
        # if the element is disabled, ignore the event
        if self.Disabled:
            return

        MyForm = self.ParentForm
        button_element = self._FindReturnKeyBoundButton(MyForm)
        if button_element is not None:
            # if the Button has been disabled, then don't perform the callback
            if button_element.Disabled:
                return
            button_element.ButtonCallBack()

    def _generic_callback_handler(self, alternative_to_key=None, force_key_to_be=None):
        """
        Peforms the actions that were in many of the callback functions previously.  Combined so that it's
        easier to modify and is in 1 place now

        :param event:            From tkinter and is not used
        :type event:             Any
        :param alternate_to_key: If key is None, then use this value instead
        :type alternate_to_key:  Any
        """
        if force_key_to_be is not None:
            self.ParentForm.LastButtonClicked = force_key_to_be
        elif self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = alternative_to_key
        self.ParentForm.FormRemainedOpen = True

        _exit_mainloop(self.ParentForm)
        # if self.ParentForm.CurrentlyRunningMainloop:
        #     Window._window_that_exited = self.ParentForm
        #     self.ParentForm.TKroot.quit()  # kick the users out of the mainloop

    def _ListboxSelectHandler(self, event):
        """
        Internal callback function for when a listbox item is selected

        :param event: Information from tkinter about the callback
        :type event:

        """
        self._generic_callback_handler('')

    def _ComboboxSelectHandler(self, event):
        """
        Internal callback function for when an entry is selected in a Combobox.
        :param event: Event data from tkinter (not used)
        :type event:

        """
        self._generic_callback_handler('')

    def _SpinboxSelectHandler(self, event=None):
        """
        Internal callback function for when an entry is selected in a Spinbox.
        Note that the parm is optional because it's not used if arrows are used to change the value
        but if the return key is pressed, it will include the event parm
        :param event: Event data passed in by tkinter (not used)
        :type event:
        """
        self._generic_callback_handler('')

    def _RadioHandler(self):
        """
        Internal callback for when a radio button is selected and enable events was set for radio
        """
        self._generic_callback_handler('')

    def _CheckboxHandler(self):
        """
        Internal callback for when a checkbnox is selected and enable events was set for checkbox
        """
        self._generic_callback_handler('')

    def _TabGroupSelectHandler(self, event):
        """
        Internal callback for when a Tab is selected and enable events was set for TabGroup

        :param event: Event data passed in by tkinter (not used)
        :type event:
        """
        self._generic_callback_handler('')

    def _KeyboardHandler(self, event):
        """
        Internal callback for when a key is pressed andd return keyboard events was set for window

        :param event: Event data passed in by tkinter (not used)
        :type event:
        """

        # if the element is disabled, ignore the event
        if self.Disabled:
            return
        self._generic_callback_handler('')

    def _ClickHandler(self, event):
        """
        Internal callback for when a mouse was clicked... I think.

        :param event: Event data passed in by tkinter (not used)
        :type event:
        """
        self._generic_callback_handler('')

    def _this_elements_window_closed(self, quick_check=True):
        if self.ParentForm is not None:
            return self.ParentForm.is_closed(quick_check=quick_check)

        return True

    def _user_bind_callback(self, bind_string, event, propagate=True):
        """
        Used when user binds a tkinter event directly to an element

        :param bind_string: The event that was bound so can lookup the key modifier
        :type bind_string:  (str)
        :param event:       Event data passed in by tkinter (not used)
        :type event:        (Any)
        :param propagate:   If True then tkinter will be told to propagate the event to the element
        :type propagate:    (bool)
        """
        key_suffix = self.user_bind_dict.get(bind_string, '')
        self.user_bind_event = event
        if self.Type == ELEM_TYPE_GRAPH:
            self._update_position_for_returned_values(event)
        if self.Key is not None:
            if isinstance(self.Key, str):
                key = self.Key + str(key_suffix)
            else:
                key = (self.Key, key_suffix)  # old way (pre 2021) was to make a brand new tuple
                # key = self.Key + (key_suffix,)   # in 2021 tried this. It will break existing applications though - if key is a tuple, add one more item
        else:
            key = bind_string

        self._generic_callback_handler(force_key_to_be=key)

        return 'break' if propagate is not True else None

    def bind(self, bind_string, key_modifier, propagate=True):
        """
        Used to add tkinter events to an Element.
        The tkinter specific data is in the Element's member variable user_bind_event
        :param bind_string:  The string tkinter expected in its bind function
        :type bind_string:   (str)
        :param key_modifier: Additional data to be added to the element's key when event is returned
        :type key_modifier:  (str)
        :param propagate:    If True then tkinter will be told to propagate the event to the element
        :type propagate:     (bool)
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        try:
            self.Widget.bind(bind_string, lambda evt: self._user_bind_callback(bind_string, evt, propagate))
        except Exception:
            self.Widget.unbind_all(bind_string)
            return

        self.user_bind_dict[bind_string] = key_modifier

    def unbind(self, bind_string):
        """
        Removes a previously bound tkinter event from an Element.
        :param bind_string: The string tkinter expected in its bind function
        :type bind_string:  (str)
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return
        self.Widget.unbind(bind_string)
        self.user_bind_dict.pop(bind_string, None)

    def set_tooltip(self, tooltip_text):
        """
        Called by application to change the tooltip text for an Element.  Normally invoked using the Element Object such as: window.Element('key').SetToolTip('New tip').

        :param tooltip_text: the text to show in tooltip.
        :type tooltip_text:  (str)
        """

        if self.TooltipObject:
            try:
                self.TooltipObject.leave()
            except:
                pass

        self.TooltipObject = ToolTip(self.Widget, text=tooltip_text, timeout=FreeSimpleGUI.DEFAULT_TOOLTIP_TIME)

    def set_focus(self, force=False):
        """
        Sets the current focus to be on this element

        :param force: if True will call focus_force otherwise calls focus_set
        :type force:  bool
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return
        try:
            if force:
                self.Widget.focus_force()
            else:
                self.Widget.focus_set()
        except Exception as e:
            _error_popup_with_traceback("Exception blocking focus. Check your element's Widget", e)

    def block_focus(self, block=True):
        """
        Enable or disable the element from getting focus by using the keyboard.
        If the block parameter is True, then this element will not be given focus by using
        the keyboard to go from one element to another.
        You CAN click on the element and utilize it.

        :param block: if True the element will not get focus via the keyboard
        :type block:  bool
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return
        try:
            self.ParentForm.TKroot.focus_force()
            if block:
                self.Widget.configure(takefocus=0)
            else:
                self.Widget.configure(takefocus=1)
        except Exception as e:
            _error_popup_with_traceback("Exception blocking focus. Check your element's Widget", e)

    def get_next_focus(self):
        """
        Gets the next element that should get focus after this element.

        :return:    Element that will get focus after this one
        :rtype:     (Element)
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return None

        try:
            next_widget_focus = self.widget.tk_focusNext()
            return self.ParentForm.widget_to_element(next_widget_focus)
        except Exception as e:
            _error_popup_with_traceback("Exception getting next focus. Check your element's Widget", e)

    def get_previous_focus(self):
        """
        Gets the element that should get focus previous to this element.

        :return:    Element that should get the focus before this one
        :rtype:     (Element)
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return None
        try:
            next_widget_focus = self.widget.tk_focusPrev()  # tkinter.Widget
            return self.ParentForm.widget_to_element(next_widget_focus)
        except Exception as e:
            _error_popup_with_traceback("Exception getting previous focus. Check your element's Widget", e)

    def set_size(self, size=(None, None)):
        """
        Changes the size of an element to a specific size.
        It's possible to specify None for one of sizes so that only 1 of the element's dimensions are changed.

        :param size: The size in characters, rows typically. In some cases they are pixels
        :type size:  (int, int)
        """
        try:
            if size[0] is not None:
                self.Widget.config(width=size[0])
        except:
            print('Warning, error setting width on element with key=', self.Key)
        try:
            if size[1] is not None:
                self.Widget.config(height=size[1])
        except:
            try:
                self.Widget.config(length=size[1])
            except:
                print('Warning, error setting height on element with key=', self.Key)

        if self.Type == ELEM_TYPE_GRAPH:
            self.CanvasSize = size

    def get_size(self):
        """
        Return the size of an element in Pixels.  Care must be taken as some elements use characters to specify their size but will return pixels when calling this get_size method.
        :return: width and height of the element
        :rtype:  (int, int)
        """
        try:
            w = self.Widget.winfo_width()
            h = self.Widget.winfo_height()
        except:
            print('Warning, error getting size of element', self.Key)
            w = h = None
        return w, h

    def hide_row(self):
        """
        Hide the entire row an Element is located on.
        Use this if you must have all space removed when you are hiding an element, including the row container
        """
        try:
            self.ParentRowFrame.pack_forget()
        except:
            print('Warning, error hiding element row for key =', self.Key)

    def unhide_row(self):
        """
        Unhides (makes visible again) the row container that the Element is located on.
        Note that it will re-appear at the bottom of the window / container, most likely.
        """
        try:
            self.ParentRowFrame.pack()
        except:
            print('Warning, error hiding element row for key =', self.Key)

    def expand(self, expand_x=False, expand_y=False, expand_row=True):
        """
        Causes the Element to expand to fill available space in the X and Y directions.  Can specify which or both directions

        :param expand_x:   If True Element will expand in the Horizontal directions
        :type expand_x:    (bool)
        :param expand_y:   If True Element will expand in the Vertical directions
        :type expand_y:    (bool)
        :param expand_row: If True the row containing the element will also expand. Without this your element is "trapped" within the row
        :type expand_row:  (bool)
        """
        if expand_x and expand_y:
            fill = tk.BOTH
        elif expand_x:
            fill = tk.X
        elif expand_y:
            fill = tk.Y
        else:
            return

        if not self._widget_was_created():
            return
        self.Widget.pack(expand=True, fill=fill)
        self.ParentRowFrame.pack(expand=expand_row, fill=fill)
        if self.element_frame is not None:
            self.element_frame.pack(expand=True, fill=fill)

    def set_cursor(self, cursor=None, cursor_color=None):
        """
        Sets the cursor for the current Element.
        "Cursor" is used in 2 different ways in this call.
        For the parameter "cursor" it's actually the mouse pointer.
        If you do not want any mouse pointer, then use the string "none"
        For the parameter "cursor_color" it's the color of the beam used when typing into an input element

        :param cursor:       The tkinter cursor name
        :type cursor:        (str)
        :param cursor_color: color to set the "cursor" to
        :type cursor_color:  (str)
        """
        if not self._widget_was_created():
            return
        if cursor is not None:
            try:
                self.Widget.config(cursor=cursor)
            except Exception as e:
                print('Warning bad cursor specified ', cursor)
                print(e)
        if cursor_color is not None:
            try:
                self.Widget.config(insertbackground=cursor_color)
            except Exception as e:
                print('Warning bad cursor color', cursor_color)
                print(e)

    def set_vscroll_position(self, percent_from_top):
        """
        Attempts to set the vertical scroll postition for an element's Widget
        :param percent_from_top: From 0 to 1.0, the percentage from the top to move scrollbar to
        :type percent_from_top:  (float)
        """
        if self.Type == ELEM_TYPE_COLUMN and self.Scrollable:
            widget = self.widget.canvas  # scrollable column is a special case
        else:
            widget = self.widget

        try:
            widget.yview_moveto(percent_from_top)
        except Exception as e:
            print('Warning setting the vertical scroll (yview_moveto failed)')
            print(e)

    def _widget_was_created(self):
        """
        Determines if a Widget was created for this element.

        :return: True if a Widget has been created previously (Widget is not None)
        :rtype:  (bool)
        """
        if self.Widget is not None:
            return True
        else:
            if FreeSimpleGUI.SUPPRESS_WIDGET_NOT_FINALIZED_WARNINGS:
                return False

            warnings.warn(
                'You cannot Update element with key = {} until the window.read() is called or set finalize=True when creating window'.format(self.Key),
                UserWarning,
            )
            if not FreeSimpleGUI.SUPPRESS_ERROR_POPUPS:
                _error_popup_with_traceback(
                    f'Unable to complete operation on element with key {self.Key}',
                    'You cannot perform operations (such as calling update) on an Element until:',
                    ' window.read() is called or finalize=True when Window created.',
                    'Adding a "finalize=True" parameter to your Window creation will likely fix this.',
                    _create_error_message(),
                )
            return False

    def _grab_anywhere_on_using_control_key(self):
        """
        Turns on Grab Anywhere functionality AFTER a window has been created.  Don't try on a window that's not yet
        been Finalized or Read.
        """
        self.Widget.bind('<Control-Button-1>', self.ParentForm._StartMove)
        self.Widget.bind('<Control-ButtonRelease-1>', self.ParentForm._StopMove)
        self.Widget.bind('<Control-B1-Motion>', self.ParentForm._OnMotion)

    def _grab_anywhere_on(self):
        """
        Turns on Grab Anywhere functionality AFTER a window has been created.  Don't try on a window that's not yet
        been Finalized or Read.
        """
        self.Widget.bind('<ButtonPress-1>', self.ParentForm._StartMove)
        self.Widget.bind('<ButtonRelease-1>', self.ParentForm._StopMove)
        self.Widget.bind('<B1-Motion>', self.ParentForm._OnMotion)

    def _grab_anywhere_off(self):
        """
        Turns off Grab Anywhere functionality AFTER a window has been created.  Don't try on a window that's not yet
        been Finalized or Read.
        """
        self.Widget.unbind('<ButtonPress-1>')
        self.Widget.unbind('<ButtonRelease-1>')
        self.Widget.unbind('<B1-Motion>')

    def grab_anywhere_exclude(self):
        """
        Excludes this element from being used by the grab_anywhere feature
        Handy for elements like a Graph element when dragging is enabled. You want the Graph element to get the drag events instead of the window dragging.
        """
        self.ParentForm._grab_anywhere_ignore_these_list.append(self.Widget)

    def grab_anywhere_include(self):
        """
        Includes this element in the grab_anywhere feature
        This will allow you to make a Multline element drag a window for example
        """
        self.ParentForm._grab_anywhere_include_these_list.append(self.Widget)

    def set_right_click_menu(self, menu=None):
        """
        Sets a right click menu for an element.
        If a menu is already set for the element, it will call the tkinter destroy method to remove it
        :param menu:                   A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type menu:                    List[List[ List[str] | str ]]
        """
        if menu == MENU_RIGHT_CLICK_DISABLED:
            return
        if menu is None:
            menu = self.ParentForm.RightClickMenu
            if menu is None:
                return
        if menu:
            # If previously had a menu destroy it
            if self.TKRightClickMenu:
                try:
                    self.TKRightClickMenu.destroy()
                except:
                    pass
            top_menu = tk.Menu(
                self.ParentForm.TKroot,
                tearoff=self.ParentForm.right_click_menu_tearoff,
                tearoffcommand=self._tearoff_menu_callback,
            )

            if self.ParentForm.right_click_menu_background_color not in (COLOR_SYSTEM_DEFAULT, None):
                top_menu.config(bg=self.ParentForm.right_click_menu_background_color)
            if self.ParentForm.right_click_menu_text_color not in (COLOR_SYSTEM_DEFAULT, None):
                top_menu.config(fg=self.ParentForm.right_click_menu_text_color)
            if self.ParentForm.right_click_menu_disabled_text_color not in (COLOR_SYSTEM_DEFAULT, None):
                top_menu.config(disabledforeground=self.ParentForm.right_click_menu_disabled_text_color)
            if self.ParentForm.right_click_menu_font is not None:
                top_menu.config(font=self.ParentForm.right_click_menu_font)

            if self.ParentForm.right_click_menu_selected_colors[0] not in (COLOR_SYSTEM_DEFAULT, None):
                top_menu.config(activeforeground=self.ParentForm.right_click_menu_selected_colors[0])
            if self.ParentForm.right_click_menu_selected_colors[1] not in (COLOR_SYSTEM_DEFAULT, None):
                top_menu.config(activebackground=self.ParentForm.right_click_menu_selected_colors[1])
            AddMenuItem(top_menu, menu[1], self, right_click_menu=True)
            self.TKRightClickMenu = top_menu
            if self.ParentForm.RightClickMenu:  # if the top level has a right click menu, then setup a callback for the Window itself
                if self.ParentForm.TKRightClickMenu is None:
                    self.ParentForm.TKRightClickMenu = top_menu
                    if running_mac():
                        self.ParentForm.TKroot.bind('<ButtonRelease-2>', self.ParentForm._RightClickMenuCallback)
                    else:
                        self.ParentForm.TKroot.bind('<ButtonRelease-3>', self.ParentForm._RightClickMenuCallback)
            if running_mac():
                self.Widget.bind('<ButtonRelease-2>', self._RightClickMenuCallback)
            else:
                self.Widget.bind('<ButtonRelease-3>', self._RightClickMenuCallback)

    def save_element_screenshot_to_disk(self, filename=None):
        """
        Saves an image of the PySimpleGUI window provided into the filename provided

        :param filename:        Optional filename to save screenshot to. If not included, the User Settinds are used to get the filename
        :return:                A PIL ImageGrab object that can be saved or manipulated
        :rtype:                 (PIL.ImageGrab | None)
        """

        try:
            from PIL import ImageGrab
        except:
            warnings.warn('Failed to import PIL. In a future version, this will raise an ImportError instead of returning None', DeprecationWarning, stacklevel=2)
            return None
        try:
            # Add a little to the X direction if window has a titlebar
            rect = (
                self.widget.winfo_rootx(),
                self.widget.winfo_rooty(),
                self.widget.winfo_rootx() + self.widget.winfo_width(),
                self.widget.winfo_rooty() + self.widget.winfo_height(),
            )

            grab = ImageGrab.grab(bbox=rect)
            # Save the grabbed image to disk
        except Exception as e:
            # print(e)
            popup_error_with_traceback('Screen capture failure', 'Error happened while trying to save screencapture of an element', e)
            return None

        # return grab
        if filename is None:
            folder = pysimplegui_user_settings.get('-screenshots folder-', '')
            filename = pysimplegui_user_settings.get('-screenshots filename-', '')
            full_filename = os.path.join(folder, filename)
        else:
            full_filename = filename
        if full_filename:
            try:
                grab.save(full_filename)
            except Exception as e:
                popup_error_with_traceback('Screen capture failure', 'Error happened while trying to save screencapture', e)
        else:
            popup_error_with_traceback(
                'Screen capture failure',
                'You have attempted a screen capture but have not set up a good filename to save to',
            )
        return grab

    def _pack_forget_save_settings(self, alternate_widget=None):
        """
        Performs a pack_forget which will make a widget invisible.
        This method saves the pack settings so that they can be restored if the element is made visible again

        :param alternate_widget:   Widget to use that's different than the one defined in Element.Widget. These are usually Frame widgets
        :type alternate_widget:    (tk.Widget)
        """

        if alternate_widget is not None and self.Widget is None:
            return

        widget = alternate_widget if alternate_widget is not None else self.Widget
        # if the widget is already invisible (i.e. not packed) then will get an error
        try:
            pack_settings = widget.pack_info()
            self.pack_settings = pack_settings
            widget.pack_forget()
        except:
            pass

    def _pack_restore_settings(self, alternate_widget=None):
        """
        Restores a previously packated widget which will make it visible again.
        If no settings were saved, then the widget is assumed to have not been unpacked and will not try to pack it again

        :param alternate_widget:   Widget to use that's different than the one defined in Element.Widget. These are usually Frame widgets
        :type alternate_widget:    (tk.Widget)
        """

        # if there are no saved pack settings, then assume it hasnb't been packaed before. The request will be ignored
        if self.pack_settings is None:
            return

        widget = alternate_widget if alternate_widget is not None else self.Widget
        if widget is not None:
            widget.pack(**self.pack_settings)

    def update(self, *args, **kwargs):
        """
        A dummy update call.  This will only be called if an element hasn't implemented an update method
        It is provided here for docstring purposes.  If you got here by browing code via PyCharm, know
        that this is not the function that will be called.  Your actual element's update method will be called.

        If you call update, you must call window.refresh if you want the change to happen prior to your next
        window.read() call. Normally uou don't do this as the window.read call is likely going to happen next.
        """
        print('* Base Element Class update was called. Your element does not seem to have an update method')

    def __call__(self, *args, **kwargs):
        """
        Makes it possible to "call" an already existing element.  When you do make the "call", it actually calls
        the Update method for the element.
        Example:    If this text element was in yoiur layout:
                    sg.Text('foo', key='T')
                    Then you can call the Update method for that element by writing:
                    window.find_element('T')('new text value')
        """
        return self.update(*args, **kwargs)

    SetTooltip = set_tooltip
    SetFocus = set_focus


from FreeSimpleGUI.elements.helpers import AddMenuItem

from FreeSimpleGUI._utils import _create_error_message
from FreeSimpleGUI._utils import _exit_mainloop

from FreeSimpleGUI._utils import _error_popup_with_traceback
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from FreeSimpleGUI.window import Window
