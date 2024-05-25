from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import FreeSimpleGUI
from FreeSimpleGUI import _change_ttk_theme
from FreeSimpleGUI import COLOR_SYSTEM_DEFAULT
from FreeSimpleGUI import ELEM_TYPE_PROGRESS_BAR
from FreeSimpleGUI import Element
from FreeSimpleGUI._utils import _error_popup_with_traceback
from FreeSimpleGUI.elements.helpers import _simplified_dual_color_to_tuple
from FreeSimpleGUI.window import Window


class TKProgressBar:
    uniqueness_counter = 0

    def __init__(
        self,
        root,
        max,
        length=400,
        width=FreeSimpleGUI.DEFAULT_PROGRESS_BAR_SIZE[1],
        ttk_theme=FreeSimpleGUI.DEFAULT_TTK_THEME,
        style_name='',
        relief=FreeSimpleGUI.DEFAULT_PROGRESS_BAR_RELIEF,
        border_width=FreeSimpleGUI.DEFAULT_PROGRESS_BAR_BORDER_WIDTH,
        orientation='horizontal',
        BarColor=(None, None),
        key=None,
    ):
        """
        :param root:         The root window bar is to be shown in
        :type root:          tk.Tk | tk.TopLevel
        :param max:          Maximum value the bar will be measuring
        :type max:           (int)
        :param length:       length in pixels of the bar
        :type length:        (int)
        :param width:        width in pixels of the bar
        :type width:         (int)
        :param style_name:   Progress bar style to use.  Set in the packer function
        :type style_name:    (str)
        :param ttk_theme:    Progress bar style defined as one of these 'default', 'winnative', 'clam', 'alt', 'classic', 'vista', 'xpnative'
        :type ttk_theme:     (str)
        :param relief:       relief style. Values are same as progress meter relief values.  Can be a constant or a string: `RELIEF_RAISED RELIEF_SUNKEN RELIEF_FLAT RELIEF_RIDGE RELIEF_GROOVE RELIEF_SOLID` (Default value = DEFAULT_PROGRESS_BAR_RELIEF)
        :type relief:        (str)
        :param border_width: The amount of pixels that go around the outside of the bar
        :type border_width:  (int)
        :param orientation:  'horizontal' or 'vertical' ('h' or 'v' work) (Default value = 'vertical')
        :type orientation:   (str)
        :param BarColor:     The 2 colors that make up a progress bar. One is the background, the other is the bar
        :type BarColor:      (str, str)
        :param key:          Used with window.find_element and with return values to uniquely identify this element to uniquely identify this element
        :type key:           str | int | tuple | object
        """

        self.Length = length
        self.Width = width
        self.Max = max
        self.Orientation = orientation
        self.Count = None
        self.PriorCount = 0
        self.style_name = style_name

        TKProgressBar.uniqueness_counter += 1

        if orientation.lower().startswith('h'):
            s = ttk.Style()
            _change_ttk_theme(s, ttk_theme)

            if BarColor != COLOR_SYSTEM_DEFAULT and BarColor[0] != COLOR_SYSTEM_DEFAULT:
                s.configure(
                    self.style_name,
                    background=BarColor[0],
                    troughcolor=BarColor[1],
                    troughrelief=relief,
                    borderwidth=border_width,
                    thickness=width,
                )
            else:
                s.configure(self.style_name, troughrelief=relief, borderwidth=border_width, thickness=width)

            self.TKProgressBarForReal = ttk.Progressbar(root, maximum=self.Max, style=self.style_name, length=length, orient=tk.HORIZONTAL, mode='determinate')
        else:
            s = ttk.Style()
            _change_ttk_theme(s, ttk_theme)
            if BarColor != COLOR_SYSTEM_DEFAULT and BarColor[0] != COLOR_SYSTEM_DEFAULT:

                s.configure(
                    self.style_name,
                    background=BarColor[0],
                    troughcolor=BarColor[1],
                    troughrelief=relief,
                    borderwidth=border_width,
                    thickness=width,
                )
            else:
                s.configure(self.style_name, troughrelief=relief, borderwidth=border_width, thickness=width)

            self.TKProgressBarForReal = ttk.Progressbar(root, maximum=self.Max, style=self.style_name, length=length, orient=tk.VERTICAL, mode='determinate')

    def Update(self, count=None, max=None):
        """
        Update the current value of the bar and/or update the maximum value the bar can reach
        :param count: current value
        :type count:  (int)
        :param max:   the maximum value
        :type max:    (int)
        """
        if max is not None:
            self.Max = max
            try:
                self.TKProgressBarForReal.config(maximum=max)
            except:
                return False
        if count is not None:
            try:
                self.TKProgressBarForReal['value'] = count
            except:
                return False
        return True


class ProgressBar(Element):
    """
    Progress Bar Element - Displays a colored bar that is shaded as progress of some operation is made
    """

    def __init__(
        self,
        max_value,
        orientation=None,
        size=(None, None),
        s=(None, None),
        size_px=(None, None),
        auto_size_text=None,
        bar_color=None,
        style=None,
        border_width=None,
        relief=None,
        key=None,
        k=None,
        pad=None,
        p=None,
        right_click_menu=None,
        expand_x=False,
        expand_y=False,
        visible=True,
        metadata=None,
    ):
        """
        :param max_value:        max value of progressbar
        :type max_value:         (int)
        :param orientation:      'horizontal' or 'vertical'
        :type orientation:       (str)
        :param size:             Size of the bar.  If horizontal (chars long, pixels wide), vert (chars high, pixels wide). Vert height measured using horizontal chars units.
        :type size:              (int, int) |  (int, None)
        :param s:                Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                 (int, int)  | (None, None)
        :param size_px:          Size in pixels (length, width). Will be used in place of size parm if specified
        :type size_px:           (int, int) | (None, None)
        :param auto_size_text:   Not sure why this is here
        :type auto_size_text:    (bool)
        :param bar_color:        The 2 colors that make up a progress bar. Either a tuple of 2 strings or a string. Tuple - (bar, background). A string with 1 color changes the background of the bar only. A string with 2 colors separated by "on" like "red on blue" specifies a red bar on a blue background.
        :type bar_color:         (str, str) or str
        :param style:            Progress bar style defined as one of these 'default', 'winnative', 'clam', 'alt', 'classic', 'vista', 'xpnative'
        :type style:             (str)
        :param border_width:     The amount of pixels that go around the outside of the bar
        :type border_width:      (int)
        :param relief:           relief style. Values are same as progress meter relief values.  Can be a constant or a string: `RELIEF_RAISED RELIEF_SUNKEN RELIEF_FLAT RELIEF_RIDGE RELIEF_GROOVE RELIEF_SOLID` (Default value = DEFAULT_PROGRESS_BAR_RELIEF)
        :type relief:            (str)
        :param key:              Used with window.find_element and with return values to uniquely identify this element to uniquely identify this element
        :type key:               str | int | tuple | object
        :param k:                Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                 str | int | tuple | object
        :param pad:              Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:               (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                 (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
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

        self.MaxValue = max_value
        self.TKProgressBar = None  # type: TKProgressBar
        self.Cancelled = False
        self.NotRunning = True
        self.Orientation = orientation if orientation else FreeSimpleGUI.DEFAULT_METER_ORIENTATION
        self.RightClickMenu = right_click_menu
        # Progress Bar colors can be a tuple (text, background) or a string with format "bar on background" - examples "red on white" or ("red", "white")
        if bar_color is None:
            bar_color = FreeSimpleGUI.DEFAULT_PROGRESS_BAR_COLOR
        else:
            bar_color = _simplified_dual_color_to_tuple(bar_color, default=FreeSimpleGUI.DEFAULT_PROGRESS_BAR_COLOR)

        self.BarColor = bar_color  # should be a tuple at this point
        self.BarStyle = style if style else FreeSimpleGUI.DEFAULT_TTK_THEME
        self.BorderWidth = border_width if border_width else FreeSimpleGUI.DEFAULT_PROGRESS_BAR_BORDER_WIDTH
        self.Relief = relief if relief else FreeSimpleGUI.DEFAULT_PROGRESS_BAR_RELIEF
        self.BarExpired = False
        key = key if key is not None else k
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y
        self.size_px = size_px

        super().__init__(
            ELEM_TYPE_PROGRESS_BAR,
            size=sz,
            auto_size_text=auto_size_text,
            key=key,
            pad=pad,
            visible=visible,
            metadata=metadata,
        )

    # returns False if update failed
    def update_bar(self, current_count, max=None):
        """
        DEPRECATED BUT STILL USABLE - has been combined with the normal ProgressBar.update method.
        Change what the bar shows by changing the current count and optionally the max count

        :param current_count: sets the current value
        :type current_count:  (int)
        :param max:           changes the max value
        :type max:            (int)
        """

        if self.ParentForm.TKrootDestroyed:
            return False
        self.TKProgressBar.Update(current_count, max=max)
        try:
            self.ParentForm.TKroot.update()
        except:
            Window._DecrementOpenCount()
            # _my_windows.Decrement()
            return False
        return True

    def update(self, current_count=None, max=None, bar_color=None, visible=None):
        """
        Changes some of the settings for the ProgressBar Element. Must call `Window.Read` or `Window.Finalize` prior
        Now has the ability to modify the count so that the update_bar method is not longer needed separately

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param current_count: sets the current value
        :type current_count:  (int)
        :param max:           changes the max value
        :type max:            (int)
        :param bar_color:     The 2 colors that make up a progress bar. Easy to remember which is which if you say "ON" between colors. "red" on "green".
        :type bar_color:      (str, str) or str
        :param visible:       control visibility of element
        :type visible:        (bool)
        :return:              Returns True if update was OK.  False means something wrong with window or it was closed
        :rtype:               (bool)
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return False

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in ProgressBar.update - The window was closed')
            return

        if self.ParentForm.TKrootDestroyed:
            return False

        if visible is False:
            self._pack_forget_save_settings()
        elif visible is True:
            self._pack_restore_settings()

        if visible is not None:
            self._visible = visible
        if bar_color is not None:
            bar_color = _simplified_dual_color_to_tuple(bar_color, default=FreeSimpleGUI.DEFAULT_PROGRESS_BAR_COLOR)
            self.BarColor = bar_color
            style = ttk.Style()
            style.configure(self.ttk_style_name, background=bar_color[0], troughcolor=bar_color[1])
        if current_count is not None:
            self.TKProgressBar.Update(current_count, max=max)

        try:
            self.ParentForm.TKroot.update()
        except:
            return False
        return True

    Update = update
    UpdateBar = update_bar
