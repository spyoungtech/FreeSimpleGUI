from __future__ import annotations

import tkinter as tk
import warnings
from typing import Any  # noqa
from typing import List  # noqa

import FreeSimpleGUI
from FreeSimpleGUI import ELEM_TYPE_INPUT_LISTBOX
from FreeSimpleGUI import Element
from FreeSimpleGUI import LISTBOX_SELECT_MODE_BROWSE
from FreeSimpleGUI import LISTBOX_SELECT_MODE_EXTENDED
from FreeSimpleGUI import LISTBOX_SELECT_MODE_MULTIPLE
from FreeSimpleGUI import LISTBOX_SELECT_MODE_SINGLE
from FreeSimpleGUI import SELECT_MODE_BROWSE
from FreeSimpleGUI import SELECT_MODE_EXTENDED
from FreeSimpleGUI import SELECT_MODE_MULTIPLE
from FreeSimpleGUI import SELECT_MODE_SINGLE
from FreeSimpleGUI import theme_input_background_color
from FreeSimpleGUI import theme_input_text_color
from FreeSimpleGUI._utils import _error_popup_with_traceback


class Listbox(Element):
    """
    A List Box.  Provide a list of values for the user to choose one or more of.   Returns a list of selected rows
    when a window.read() is executed.
    """

    def __init__(
        self,
        values,
        default_values=None,
        select_mode=None,
        change_submits=False,
        enable_events=False,
        bind_return_key=False,
        size=(None, None),
        s=(None, None),
        disabled=False,
        justification=None,
        auto_size_text=None,
        font=None,
        no_scrollbar=False,
        horizontal_scroll=False,
        background_color=None,
        text_color=None,
        highlight_background_color=None,
        highlight_text_color=None,
        sbar_trough_color=None,
        sbar_background_color=None,
        sbar_arrow_color=None,
        sbar_width=None,
        sbar_arrow_width=None,
        sbar_frame_color=None,
        sbar_relief=None,
        key=None,
        k=None,
        pad=None,
        p=None,
        tooltip=None,
        expand_x=False,
        expand_y=False,
        right_click_menu=None,
        visible=True,
        metadata=None,
    ):
        """
        :param values:                     list of values to display. Can be any type including mixed types as long as they have __str__ method
        :type values:                      List[Any] or Tuple[Any]
        :param default_values:             which values should be initially selected
        :type default_values:              List[Any]
        :param select_mode:                Select modes are used to determine if only 1 item can be selected or multiple and how they can be selected.   Valid choices begin with "LISTBOX_SELECT_MODE_" and include: LISTBOX_SELECT_MODE_SINGLE LISTBOX_SELECT_MODE_MULTIPLE LISTBOX_SELECT_MODE_BROWSE LISTBOX_SELECT_MODE_EXTENDED
        :type select_mode:                 [enum]
        :param change_submits:             DO NOT USE. Only listed for backwards compat - Use enable_events instead
        :type change_submits:              (bool)
        :param enable_events:              Turns on the element specific events. Listbox generates events when an item is clicked
        :type enable_events:               (bool)
        :param bind_return_key:            If True, then the return key will cause a the Listbox to generate an event when return key is pressed
        :type bind_return_key:             (bool)
        :param size:                       w=characters-wide, h=rows-high. If an int instead of a tuple is supplied, then height is auto-set to 1
        :type size:                        (int, int) |  (int, None) | int
        :param s:                          Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                           (int, int)  | (None, None) | int
        :param disabled:                   set disable state for element
        :type disabled:                    (bool)
        :param justification:              justification for items in listbox. Valid choices - left, right, center.  Default is left. NOTE - on some older versions of tkinter, not available
        :type justification:               (str)
        :param auto_size_text:             True if element should be the same size as the contents
        :type auto_size_text:              (bool)
        :param font:                       specifies the font family, size, etc.  Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:                        (str or (str, int[, str]) or None)
        :param no_scrollbar:               Controls if a scrollbar should be shown.  If True, no scrollbar will be shown
        :type no_scrollbar:                (bool)
        :param horizontal_scroll:          Controls if a horizontal scrollbar should be shown.  If True a horizontal scrollbar will be shown in addition to vertical
        :type horizontal_scroll:           (bool)
        :param background_color:           color of background
        :type background_color:            (str)
        :param text_color:                 color of the text
        :type text_color:                  (str)
        :param highlight_background_color: color of the background when an item is selected. Defaults to normal text color (a reverse look)
        :type highlight_background_color:  (str)
        :param highlight_text_color:       color of the text when an item is selected. Defaults to the normal background color (a rerverse look)
        :type highlight_text_color:        (str)
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
        :param key:                        Used with window.find_element and with return values to uniquely identify this element
        :type key:                         str | int | tuple | object
        :param k:                          Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                           str | int | tuple | object
        :param pad:                        Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:                         (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                          Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                           (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param tooltip:                    text, that will appear when mouse hovers over the element
        :type tooltip:                     (str)
        :param expand_x:                   If True the element will automatically expand in the X direction to fill available space
        :type expand_x:                    (bool)
        :param expand_y:                   If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:                    (bool)
        :param right_click_menu:           A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type right_click_menu:            List[List[ List[str] | str ]]
        :param visible:                    set visibility state of the element
        :type visible:                     (bool)
        :param metadata:                   User metadata that can be set to ANYTHING
        :type metadata:                    (Any)
        """

        if values is None:
            _error_popup_with_traceback(
                'Error in your Listbox definition - The values parameter cannot be None',
                'Use an empty list if you want no values in your Listbox',
            )

        self.Values = values
        self.DefaultValues = default_values
        self.TKListbox = None
        self.ChangeSubmits = change_submits or enable_events
        self.BindReturnKey = bind_return_key
        self.Disabled = disabled
        if select_mode == LISTBOX_SELECT_MODE_BROWSE:
            self.SelectMode = SELECT_MODE_BROWSE
        elif select_mode == LISTBOX_SELECT_MODE_EXTENDED:
            self.SelectMode = SELECT_MODE_EXTENDED
        elif select_mode == LISTBOX_SELECT_MODE_MULTIPLE:
            self.SelectMode = SELECT_MODE_MULTIPLE
        elif select_mode == LISTBOX_SELECT_MODE_SINGLE:
            self.SelectMode = SELECT_MODE_SINGLE
        else:
            self.SelectMode = FreeSimpleGUI.DEFAULT_LISTBOX_SELECT_MODE
        bg = background_color if background_color is not None else theme_input_background_color()
        fg = text_color if text_color is not None else theme_input_text_color()
        self.HighlightBackgroundColor = highlight_background_color if highlight_background_color is not None else fg
        self.HighlightTextColor = highlight_text_color if highlight_text_color is not None else bg
        self.RightClickMenu = right_click_menu
        self.vsb = None  # type: tk.Scrollbar or None
        self.hsb = None  # type: tk.Scrollbar | None
        self.TKListbox = self.Widget = None  # type: tk.Listbox
        self.element_frame = None  # type: tk.Frame
        self.NoScrollbar = no_scrollbar
        self.HorizontalScroll = horizontal_scroll
        key = key if key is not None else k
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y
        self.justification = justification

        super().__init__(
            ELEM_TYPE_INPUT_LISTBOX,
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
            sbar_trough_color=sbar_trough_color,
            sbar_background_color=sbar_background_color,
            sbar_arrow_color=sbar_arrow_color,
            sbar_width=sbar_width,
            sbar_arrow_width=sbar_arrow_width,
            sbar_frame_color=sbar_frame_color,
            sbar_relief=sbar_relief,
        )

    def update(self, values=None, disabled=None, set_to_index=None, scroll_to_index=None, select_mode=None, visible=None):
        """
        Changes some of the settings for the Listbox Element. Must call `Window.Read` or `Window.Finalize` prior
        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param values:          new list of choices to be shown to user
        :type values:           List[Any]
        :param disabled:        disable or enable state of the element
        :type disabled:         (bool)
        :param set_to_index:    highlights the item(s) indicated. If parm is an int one entry will be set. If is a list, then each entry in list is highlighted
        :type set_to_index:     int | list | tuple
        :param scroll_to_index: scroll the listbox so that this index is the first shown
        :type scroll_to_index:  (int)
        :param select_mode:     changes the select mode according to tkinter's listbox widget
        :type select_mode:      (str)
        :param visible:         control visibility of element
        :type visible:          (bool)
        """

        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Listbox.update - The window was closed')
            return

        if disabled is True:
            self.TKListbox.configure(state='disabled')
        elif disabled is False:
            self.TKListbox.configure(state='normal')
        self.Disabled = disabled if disabled is not None else self.Disabled

        if values is not None:
            self.TKListbox.delete(0, 'end')
            for item in list(values):
                self.TKListbox.insert(tk.END, item)
            # self.TKListbox.selection_set(0, 0)
            self.Values = list(values)
        if set_to_index is not None:
            self.TKListbox.selection_clear(0, len(self.Values))  # clear all listbox selections
            if type(set_to_index) in (tuple, list):
                for i in set_to_index:
                    try:
                        self.TKListbox.selection_set(i, i)
                    except:
                        warnings.warn(f'* Listbox Update selection_set failed with index {set_to_index}*')
            else:
                try:
                    self.TKListbox.selection_set(set_to_index, set_to_index)
                except:
                    warnings.warn(f'* Listbox Update selection_set failed with index {set_to_index}*')
        if visible is False:
            self._pack_forget_save_settings(self.element_frame)
        elif visible is True:
            self._pack_restore_settings(self.element_frame)
        if scroll_to_index is not None and len(self.Values):
            self.TKListbox.yview_moveto(scroll_to_index / len(self.Values))
        if select_mode is not None:
            try:
                self.TKListbox.config(selectmode=select_mode)
            except:
                print('Listbox.update error trying to change mode to: ', select_mode)
        if visible is not None:
            self._visible = visible

    def set_value(self, values):
        """
        Set listbox highlighted choices

        :param values: new values to choose based on previously set values
        :type values:  List[Any] | Tuple[Any]

        """
        for index, item in enumerate(self.Values):
            try:
                if item in values:
                    self.TKListbox.selection_set(index)
                else:
                    self.TKListbox.selection_clear(index)
            except:
                pass
        self.DefaultValues = values

    def get_list_values(self):
        # type: (Listbox) -> List[Any]
        """
        Returns list of Values provided by the user in the user's format

        :return: List of values. Can be any / mixed types -> []
        :rtype:  List[Any]
        """
        return self.Values

    def get_indexes(self):
        """
        Returns the items currently selected as a list of indexes

        :return: A list of offsets into values that is currently selected
        :rtype:  List[int]
        """
        return self.TKListbox.curselection()

    def get(self):
        """
        Returns the list of items currently selected in this listbox.  It should be identical
        to the value you would receive when performing a window.read() call.

        :return: The list of currently selected items. The actual items are returned, not the indexes
        :rtype:  List[Any]
        """
        try:
            items = self.TKListbox.curselection()
            value = [self.Values[int(item)] for item in items]
        except:
            value = []
        return value

    def select_index(self, index, highlight_text_color=None, highlight_background_color=None):
        """
        Selects an index while providing capability to setting the selected color for the index to specific text/background color

        :param index:                      specifies which item to change. index starts at 0 and goes to length of values list minus one
        :type  index:                      (int)
        :param highlight_text_color:       color of the text when this item is selected.
        :type  highlight_text_color:        (str)
        :param highlight_background_color: color of the background when this item is selected
        :type  highlight_background_color:  (str)
        """

        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Listbox.select_item - The window was closed')
            return

        if index >= len(self.Values):
            _error_popup_with_traceback('Index {} is out of range for Listbox.select_index. Max allowed index is {}.'.format(index, len(self.Values) - 1))
            return

        self.TKListbox.selection_set(index, index)

        if highlight_text_color is not None:
            self.widget.itemconfig(index, selectforeground=highlight_text_color)
        if highlight_background_color is not None:
            self.widget.itemconfig(index, selectbackground=highlight_background_color)

    def set_index_color(self, index, text_color=None, background_color=None, highlight_text_color=None, highlight_background_color=None):
        """
        Sets the color of a specific item without selecting it

        :param index:                      specifies which item to change. index starts at 0 and goes to length of values list minus one
        :type  index:                      (int)
        :param text_color:                 color of the text for this item
        :type  text_color:                 (str)
        :param background_color:           color of the background for this item
        :type  background_color:           (str)
        :param highlight_text_color:       color of the text when this item is selected.
        :type  highlight_text_color:       (str)
        :param highlight_background_color: color of the background when this item is selected
        :type  highlight_background_color: (str)
        """

        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Listbox.set_item_color - The window was closed')
            return

        if index >= len(self.Values):
            _error_popup_with_traceback('Index {} is out of range for Listbox.set_index_color. Max allowed index is {}.'.format(index, len(self.Values) - 1))
            return

        if text_color is not None:
            self.widget.itemconfig(index, fg=text_color)
        if background_color is not None:
            self.widget.itemconfig(index, bg=background_color)
        if highlight_text_color is not None:
            self.widget.itemconfig(index, selectforeground=highlight_text_color)
        if highlight_background_color is not None:
            self.widget.itemconfig(index, selectbackground=highlight_background_color)

    GetIndexes = get_indexes
    GetListValues = get_list_values
    SetValue = set_value
    Update = update
