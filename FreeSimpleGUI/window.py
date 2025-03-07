from __future__ import annotations

import calendar
import datetime
import difflib
import os
import pickle
import queue
import sys
import threading
import tkinter
import tkinter as tk
import warnings
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

import FreeSimpleGUI
from FreeSimpleGUI import _BuildResults
from FreeSimpleGUI import _Debugger
from FreeSimpleGUI import _debugger_window_is_open
from FreeSimpleGUI import _FindElementWithFocusInSubForm
from FreeSimpleGUI import _get_hidden_master_root
from FreeSimpleGUI import _global_settings_get_watermark_info
from FreeSimpleGUI import _long_func_thread
from FreeSimpleGUI import _refresh_debugger
from FreeSimpleGUI import _TimerPeriodic
from FreeSimpleGUI import BUTTON_TYPE_CALENDAR_CHOOSER
from FreeSimpleGUI import COLOR_SYSTEM_DEFAULT
from FreeSimpleGUI import ELEM_TYPE_BUTTON
from FreeSimpleGUI import ELEM_TYPE_BUTTONMENU
from FreeSimpleGUI import ELEM_TYPE_COLUMN
from FreeSimpleGUI import ELEM_TYPE_FRAME
from FreeSimpleGUI import ELEM_TYPE_GRAPH
from FreeSimpleGUI import ELEM_TYPE_IMAGE
from FreeSimpleGUI import ELEM_TYPE_INPUT_CHECKBOX
from FreeSimpleGUI import ELEM_TYPE_INPUT_COMBO
from FreeSimpleGUI import ELEM_TYPE_INPUT_LISTBOX
from FreeSimpleGUI import ELEM_TYPE_INPUT_MULTILINE
from FreeSimpleGUI import ELEM_TYPE_INPUT_OPTION_MENU
from FreeSimpleGUI import ELEM_TYPE_INPUT_RADIO
from FreeSimpleGUI import ELEM_TYPE_INPUT_SLIDER
from FreeSimpleGUI import ELEM_TYPE_INPUT_SPIN
from FreeSimpleGUI import ELEM_TYPE_INPUT_TEXT
from FreeSimpleGUI import ELEM_TYPE_MENUBAR
from FreeSimpleGUI import ELEM_TYPE_PANE
from FreeSimpleGUI import ELEM_TYPE_PROGRESS_BAR
from FreeSimpleGUI import ELEM_TYPE_SEPARATOR
from FreeSimpleGUI import ELEM_TYPE_TAB
from FreeSimpleGUI import ELEM_TYPE_TAB_GROUP
from FreeSimpleGUI import ELEM_TYPE_TABLE
from FreeSimpleGUI import ELEM_TYPE_TREE
from FreeSimpleGUI import EMOJI_BASE64_KEY
from FreeSimpleGUI import EVENT_TIMER
from FreeSimpleGUI import fill_form_with_values
from FreeSimpleGUI import GRAB_ANYWHERE_IGNORE_THESE_WIDGETS
from FreeSimpleGUI import InitializeResults
from FreeSimpleGUI import PackFormIntoFrame
from FreeSimpleGUI import popup_error_with_traceback
from FreeSimpleGUI import popup_get_date
from FreeSimpleGUI import popup_quick_message
from FreeSimpleGUI import pysimplegui_user_settings
from FreeSimpleGUI import running_linux
from FreeSimpleGUI import running_mac
from FreeSimpleGUI import running_windows
from FreeSimpleGUI import StartupTK
from FreeSimpleGUI import theme_input_background_color
from FreeSimpleGUI import theme_input_text_color
from FreeSimpleGUI import theme_use_custom_titlebar
from FreeSimpleGUI import TIMEOUT_KEY
from FreeSimpleGUI import Titlebar
from FreeSimpleGUI import TITLEBAR_CLOSE_KEY
from FreeSimpleGUI import TITLEBAR_IMAGE_KEY
from FreeSimpleGUI import TITLEBAR_MAXIMIZE_KEY
from FreeSimpleGUI import TITLEBAR_METADATA_MARKER
from FreeSimpleGUI import TITLEBAR_MINIMIZE_KEY
from FreeSimpleGUI import TITLEBAR_TEXT_KEY
from FreeSimpleGUI import TTKPartOverrides
from FreeSimpleGUI import WINDOW_CLOSE_ATTEMPTED_EVENT
from FreeSimpleGUI import WINDOW_CONFIG_EVENT
from FreeSimpleGUI._utils import _error_popup_with_traceback
from FreeSimpleGUI._utils import _exit_mainloop
from FreeSimpleGUI.elements.base import Element
from FreeSimpleGUI.elements.helpers import _simplified_dual_color_to_tuple
from FreeSimpleGUI.elements.helpers import button_color_to_tuple


class Window:
    """
    Represents a single Window
    """

    NumOpenWindows = 0
    _user_defined_icon = None
    hidden_master_root = None  # type: tk.Tk
    _animated_popup_dict = {}  # type: Dict
    _active_windows = {}  # type: Dict[Window, tk.Tk()]
    _move_all_windows = False  # if one window moved, they will move
    _window_that_exited = None  # type: Window
    _root_running_mainloop = None  # type: tk.Tk()    # (may be the hidden root or a window's root)
    _timeout_key = None
    _TKAfterID = None  # timer that is used to run reads with timeouts
    _window_running_mainloop = None  # The window that is running the mainloop
    _container_element_counter = 0  # used to get a number of Container Elements (Frame, Column, Tab)
    _read_call_from_debugger = False
    _timeout_0_counter = 0  # when timeout=0 then go through each window one at a time
    _counter_for_ttk_widgets = 0
    _floating_debug_window_build_needed = False
    _main_debug_window_build_needed = False
    # rereouted stdout info. List of tuples (window, element, previous destination)
    _rerouted_stdout_stack = []  # type: List[Tuple[Window, Element]]
    _rerouted_stderr_stack = []  # type: List[Tuple[Window, Element]]
    _original_stdout = None
    _original_stderr = None
    _watermark = None
    _watermark_temp_forced = False
    _watermark_user_text = ''

    def __init__(
        self,
        title,
        layout=None,
        default_element_size=None,
        default_button_element_size=(None, None),
        auto_size_text=None,
        auto_size_buttons=None,
        location=(None, None),
        relative_location=(None, None),
        size=(None, None),
        element_padding=None,
        margins=(None, None),
        button_color=None,
        font=None,
        progress_bar_color=(None, None),
        background_color=None,
        border_depth=None,
        auto_close=False,
        auto_close_duration=FreeSimpleGUI.DEFAULT_AUTOCLOSE_TIME,
        icon=None,
        force_toplevel=False,
        alpha_channel=None,
        return_keyboard_events=False,
        use_default_focus=True,
        text_justification=None,
        no_titlebar=False,
        grab_anywhere=False,
        grab_anywhere_using_control=True,
        keep_on_top=None,
        resizable=False,
        disable_close=False,
        disable_minimize=False,
        right_click_menu=None,
        transparent_color=None,
        debugger_enabled=True,
        right_click_menu_background_color=None,
        right_click_menu_text_color=None,
        right_click_menu_disabled_text_color=None,
        right_click_menu_selected_colors=(None, None),
        right_click_menu_font=None,
        right_click_menu_tearoff=False,
        finalize=False,
        element_justification='left',
        ttk_theme=None,
        use_ttk_buttons=None,
        modal=False,
        enable_close_attempted_event=False,
        enable_window_config_events=False,
        titlebar_background_color=None,
        titlebar_text_color=None,
        titlebar_font=None,
        titlebar_icon=None,
        use_custom_titlebar=None,
        scaling=None,
        sbar_trough_color=None,
        sbar_background_color=None,
        sbar_arrow_color=None,
        sbar_width=None,
        sbar_arrow_width=None,
        sbar_frame_color=None,
        sbar_relief=None,
        watermark=None,
        metadata=None,
    ):
        """
        :param title:                                The title that will be displayed in the Titlebar and on the Taskbar
        :type title:                                 (str)
        :param layout:                               The layout for the window. Can also be specified in the Layout method
        :type layout:                                List[List[Element]] | Tuple[Tuple[Element]]
        :param default_element_size:                 size in characters (wide) and rows (high) for all elements in this window
        :type default_element_size:                  (int, int) - (width, height)
        :param default_button_element_size:          (width, height) size in characters (wide) and rows (high) for all Button elements in this window
        :type default_button_element_size:           (int, int)
        :param auto_size_text:                       True if Elements in Window should be sized to exactly fir the length of text
        :type auto_size_text:                        (bool)
        :param auto_size_buttons:                    True if Buttons in this Window should be sized to exactly fit the text on this.
        :type auto_size_buttons:                     (bool)
        :param relative_location:                    (x,y) location relative to the default location of the window, in pixels. Normally the window centers.  This location is relative to the location the window would be created. Note they can be negative.
        :type relative_location:                     (int, int)
        :param location:                             (x,y) location, in pixels, to locate the upper left corner of the window on the screen. Default is to center on screen. None will not set any location meaning the OS will decide
        :type location:                              (int, int) or (None, None) or None
        :param size:                                 (width, height) size in pixels for this window. Normally the window is autosized to fit contents, not set to an absolute size by the user. Try not to set this value. You risk, the contents being cut off, etc. Let the layout determine the window size instead
        :type size:                                  (int, int)
        :param element_padding:                      Default amount of padding to put around elements in window (left/right, top/bottom) or ((left, right), (top, bottom)), or an int. If an int, then it's converted into a tuple (int, int)
        :type element_padding:                       (int, int) or ((int, int),(int,int)) or int
        :param margins:                              (left/right, top/bottom) Amount of pixels to leave inside the window's frame around the edges before your elements are shown.
        :type margins:                               (int, int)
        :param button_color:                         Default button colors for all buttons in the window
        :type button_color:                          (str, str) | str
        :param font:                                 specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:                                  (str or (str, int[, str]) or None)
        :param progress_bar_color:                   (bar color, background color) Sets the default colors for all progress bars in the window
        :type progress_bar_color:                    (str, str)
        :param background_color:                     color of background
        :type background_color:                      (str)
        :param border_depth:                         Default border depth (width) for all elements in the window
        :type border_depth:                          (int)
        :param auto_close:                           If True, the window will automatically close itself
        :type auto_close:                            (bool)
        :param auto_close_duration:                  Number of seconds to wait before closing the window
        :type auto_close_duration:                   (int)
        :param icon:                                 Can be either a filename or Base64 value. For Windows if filename, it MUST be ICO format. For Linux, must NOT be ICO. Most portable is to use a Base64 of a PNG file. This works universally across all OS's
        :type icon:                                  (str | bytes)
        :param force_toplevel:                       If True will cause this window to skip the normal use of a hidden master window
        :type force_toplevel:                        (bool)
        :param alpha_channel:                        Sets the opacity of the window. 0 = invisible 1 = completely visible. Values bewteen 0 & 1 will produce semi-transparent windows in SOME environments (The Raspberry Pi always has this value at 1 and cannot change.
        :type alpha_channel:                         (float)
        :param return_keyboard_events:               if True key presses on the keyboard will be returned as Events from Read calls
        :type return_keyboard_events:                (bool)
        :param use_default_focus:                    If True will use the default focus algorithm to set the focus to the "Correct" element
        :type use_default_focus:                     (bool)
        :param text_justification:                   Default text justification for all Text Elements in window
        :type text_justification:                    'left' | 'right' | 'center'
        :param no_titlebar:                          If true, no titlebar nor frame will be shown on window. This means you cannot minimize the window and it will not show up on the taskbar
        :type no_titlebar:                           (bool)
        :param grab_anywhere:                        If True can use mouse to click and drag to move the window. Almost every location of the window will work except input fields on some systems
        :type grab_anywhere:                         (bool)
        :param grab_anywhere_using_control:          If True can use CONTROL key + left mouse mouse to click and drag to move the window. DEFAULT is TRUE. Unlike normal grab anywhere, it works on all elements.
        :type grab_anywhere_using_control:           (bool)
        :param keep_on_top:                          If True, window will be created on top of all other windows on screen. It can be bumped down if another window created with this parm
        :type keep_on_top:                           (bool)
        :param resizable:                            If True, allows the user to resize the window. Note the not all Elements will change size or location when resizing.
        :type resizable:                             (bool)
        :param disable_close:                        If True, the X button in the top right corner of the window will no work.  Use with caution and always give a way out toyour users
        :type disable_close:                         (bool)
        :param disable_minimize:                     if True the user won't be able to minimize window.  Good for taking over entire screen and staying that way.
        :type disable_minimize:                      (bool)
        :param right_click_menu:                     A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type right_click_menu:                      List[List[ List[str] | str ]]
        :param transparent_color:                    Any portion of the window that has this color will be completely transparent. You can even click through these spots to the window under this window.
        :type transparent_color:                     (str)
        :param debugger_enabled:                     If True then the internal debugger will be enabled
        :type debugger_enabled:                      (bool)
        :param right_click_menu_background_color:    Background color for right click menus
        :type right_click_menu_background_color:     (str)
        :param right_click_menu_text_color:          Text color for right click menus
        :type right_click_menu_text_color:           (str)
        :param right_click_menu_disabled_text_color: Text color for disabled right click menu items
        :type right_click_menu_disabled_text_color:  (str)
        :param right_click_menu_selected_colors:     Text AND background colors for a selected item. Can be a Tuple OR a color string. simplified-button-color-string "foreground on background". Can be a single color if want to set only the background. Normally a tuple, but can be a simplified-dual-color-string "foreground on background". Can be a single color if want to set only the background.
        :type right_click_menu_selected_colors:      (str, str) | str | Tuple
        :param right_click_menu_font:                Font for right click menus
        :type right_click_menu_font:                 (str or (str, int[, str]) or None)
        :param right_click_menu_tearoff:             If True then all right click menus can be torn off
        :type right_click_menu_tearoff:              bool
        :param finalize:                             If True then the Finalize method will be called. Use this rather than chaining .Finalize for cleaner code
        :type finalize:                              (bool)
        :param element_justification:                All elements in the Window itself will have this justification 'left', 'right', 'center' are valid values
        :type element_justification:                 (str)
        :param ttk_theme:                            Set the tkinter ttk "theme" of the window.  Default = DEFAULT_TTK_THEME.  Sets all ttk widgets to this theme as their default
        :type ttk_theme:                             (str)
        :param use_ttk_buttons:                      Affects all buttons in window. True = use ttk buttons. False = do not use ttk buttons.  None = use ttk buttons only if on a Mac
        :type use_ttk_buttons:                       (bool)
        :param modal:                                If True then this window will be the only window a user can interact with until it is closed
        :type modal:                                 (bool)
        :param enable_close_attempted_event:         If True then the window will not close when "X" clicked. Instead an event WINDOW_CLOSE_ATTEMPTED_EVENT if returned from window.read
        :type enable_close_attempted_event:          (bool)
        :param enable_window_config_events:          If True then window configuration events (resizing or moving the window) will return WINDOW_CONFIG_EVENT from window.read. Note you will get several when Window is created.
        :type enable_window_config_events:           (bool)
        :param titlebar_background_color:            If custom titlebar indicated by use_custom_titlebar, then use this as background color
        :type titlebar_background_color:             (str | None)
        :param titlebar_text_color:                  If custom titlebar indicated by use_custom_titlebar, then use this as text color
        :type titlebar_text_color:                   (str | None)
        :param titlebar_font:                        If custom titlebar indicated by use_custom_titlebar, then use this as title font
        :type titlebar_font:                         (str or (str, int[, str]) or None)
        :param titlebar_icon:                        If custom titlebar indicated by use_custom_titlebar, then use this as the icon (file or base64 bytes)
        :type titlebar_icon:                         (bytes | str)
        :param use_custom_titlebar:                  If True, then a custom titlebar will be used instead of the normal titlebar
        :type use_custom_titlebar:                   bool
        :param scaling:                              Apply scaling to the elements in the window. Can be set on a global basis using set_options
        :type scaling:                               float
        :param sbar_trough_color:                    Scrollbar color of the trough
        :type sbar_trough_color:                     (str)
        :param sbar_background_color:                Scrollbar color of the background of the arrow buttons at the ends AND the color of the "thumb" (the thing you grab and slide). Switches to arrow color when mouse is over
        :type sbar_background_color:                 (str)
        :param sbar_arrow_color:                     Scrollbar color of the arrow at the ends of the scrollbar (it looks like a button). Switches to background color when mouse is over
        :type sbar_arrow_color:                      (str)
        :param sbar_width:                           Scrollbar width in pixels
        :type sbar_width:                            (int)
        :param sbar_arrow_width:                     Scrollbar width of the arrow on the scrollbar. It will potentially impact the overall width of the scrollbar
        :type sbar_arrow_width:                      (int)
        :param sbar_frame_color:                     Scrollbar Color of frame around scrollbar (available only on some ttk themes)
        :type sbar_frame_color:                      (str)
        :param sbar_relief:                          Scrollbar relief that will be used for the "thumb" of the scrollbar (the thing you grab that slides). Should be a constant that is defined at starting with "RELIEF_" - RELIEF_RAISED, RELIEF_SUNKEN, RELIEF_FLAT, RELIEF_RIDGE, RELIEF_GROOVE, RELIEF_SOLID
        :type sbar_relief:                           (str)
        :param watermark:                            If True, then turns on watermarking temporarily for ALL windows created from this point forward. See global settings doc for more info
        :type watermark:                             bool
        :param metadata:                             User metadata that can be set to ANYTHING
        :type metadata:                              (Any)
        """

        self._metadata = None  # type: Any
        self.AutoSizeText = auto_size_text if auto_size_text is not None else FreeSimpleGUI.DEFAULT_AUTOSIZE_TEXT
        self.AutoSizeButtons = auto_size_buttons if auto_size_buttons is not None else FreeSimpleGUI.DEFAULT_AUTOSIZE_BUTTONS
        self.Title = str(title)
        self.Rows = []  # a list of ELEMENTS for this row
        self.DefaultElementSize = default_element_size if default_element_size is not None else FreeSimpleGUI.DEFAULT_ELEMENT_SIZE
        self.DefaultButtonElementSize = default_button_element_size if default_button_element_size != (None, None) else FreeSimpleGUI.DEFAULT_BUTTON_ELEMENT_SIZE
        if FreeSimpleGUI.DEFAULT_WINDOW_LOCATION != (None, None) and location == (None, None):
            self.Location = FreeSimpleGUI.DEFAULT_WINDOW_LOCATION
        else:
            self.Location = location
        self.RelativeLoction = relative_location
        self.ButtonColor = button_color_to_tuple(button_color)
        self.BackgroundColor = background_color if background_color else FreeSimpleGUI.DEFAULT_BACKGROUND_COLOR
        self.ParentWindow = None
        self.Font = font if font else FreeSimpleGUI.DEFAULT_FONT
        self.RadioDict = {}
        self.BorderDepth = border_depth
        if icon:
            self.WindowIcon = icon
        elif Window._user_defined_icon is not None:
            self.WindowIcon = Window._user_defined_icon
        else:
            self.WindowIcon = FreeSimpleGUI.DEFAULT_WINDOW_ICON
        self.AutoClose = auto_close
        self.NonBlocking = False
        self.TKroot = None  # type: tk.Tk
        self.TKrootDestroyed = False
        self.CurrentlyRunningMainloop = False
        self.FormRemainedOpen = False
        self.TKAfterID = None
        self.ProgressBarColor = progress_bar_color
        self.AutoCloseDuration = auto_close_duration
        self.RootNeedsDestroying = False
        self.Shown = False
        self.ReturnValues = None
        self.ReturnValuesList = []
        self.ReturnValuesDictionary = {}
        self.DictionaryKeyCounter = 0
        self.LastButtonClicked = None
        self.LastButtonClickedWasRealtime = False
        self.UseDictionary = False
        self.UseDefaultFocus = use_default_focus
        self.ReturnKeyboardEvents = return_keyboard_events
        self.LastKeyboardEvent = None
        self.TextJustification = text_justification
        self.NoTitleBar = no_titlebar
        self.Grab = grab_anywhere
        self.GrabAnywhere = grab_anywhere
        self.GrabAnywhereUsingControlKey = grab_anywhere_using_control
        if keep_on_top is None and FreeSimpleGUI.DEFAULT_KEEP_ON_TOP is not None:
            keep_on_top = FreeSimpleGUI.DEFAULT_KEEP_ON_TOP
        elif keep_on_top is None:
            keep_on_top = False
        self.KeepOnTop = keep_on_top
        self.ForceTopLevel = force_toplevel
        self.Resizable = resizable
        self._AlphaChannel = alpha_channel if alpha_channel is not None else FreeSimpleGUI.DEFAULT_ALPHA_CHANNEL
        self.Timeout = None
        self.TimeoutKey = TIMEOUT_KEY
        self.TimerCancelled = False
        self.DisableClose = disable_close
        self.DisableMinimize = disable_minimize
        self._Hidden = False
        self._Size = size
        self.XFound = False
        if element_padding is not None:
            if isinstance(element_padding, int):
                element_padding = (element_padding, element_padding)

        if element_padding is None:
            self.ElementPadding = FreeSimpleGUI.DEFAULT_ELEMENT_PADDING
        else:
            self.ElementPadding = element_padding
        self.RightClickMenu = right_click_menu
        self.Margins = margins if margins != (None, None) else FreeSimpleGUI.DEFAULT_MARGINS
        self.ContainerElemementNumber = Window._GetAContainerNumber()
        # The dictionary containing all elements and keys for the window
        # The keys are the keys for the elements and the values are the elements themselves.
        self.AllKeysDict = {}
        self.TransparentColor = transparent_color
        self.UniqueKeyCounter = 0
        self.DebuggerEnabled = debugger_enabled
        self.WasClosed = False
        self.ElementJustification = element_justification
        self.FocusSet = False
        self.metadata = metadata
        self.TtkTheme = ttk_theme or FreeSimpleGUI.DEFAULT_TTK_THEME
        self.UseTtkButtons = use_ttk_buttons if use_ttk_buttons is not None else FreeSimpleGUI.USE_TTK_BUTTONS
        self.user_bind_dict = {}  # Used when user defines a tkinter binding using bind method - convert bind string to key modifier
        self.user_bind_event = None  # Used when user defines a tkinter binding using bind method - event data from tkinter
        self.modal = modal
        self.thread_queue = None  # type: queue.Queue
        self.thread_lock = None  # type: threading.Lock
        self.thread_timer = None  # type: tk.Misc
        self.thread_strvar = None  # type: tk.StringVar
        self.read_closed_window_count = 0
        self.config_last_size = (None, None)
        self.config_last_location = (None, None)
        self.starting_window_position = (None, None)
        self.not_completed_initial_movement = True
        self.config_count = 0
        self.saw_00 = False
        self.maximized = False
        self.right_click_menu_background_color = right_click_menu_background_color if right_click_menu_background_color is not None else theme_input_background_color()
        self.right_click_menu_text_color = right_click_menu_text_color if right_click_menu_text_color is not None else theme_input_text_color()
        self.right_click_menu_disabled_text_color = right_click_menu_disabled_text_color if right_click_menu_disabled_text_color is not None else COLOR_SYSTEM_DEFAULT
        self.right_click_menu_font = right_click_menu_font if right_click_menu_font is not None else self.Font
        self.right_click_menu_tearoff = right_click_menu_tearoff
        self.auto_close_timer_needs_starting = False
        self.finalize_in_progress = False
        self.close_destroys_window = not enable_close_attempted_event if enable_close_attempted_event is not None else None
        self.enable_window_config_events = enable_window_config_events
        self.override_custom_titlebar = False
        self.use_custom_titlebar = use_custom_titlebar or theme_use_custom_titlebar()
        self.titlebar_background_color = titlebar_background_color
        self.titlebar_text_color = titlebar_text_color
        self.titlebar_font = titlebar_font
        self.titlebar_icon = titlebar_icon
        self.right_click_menu_selected_colors = _simplified_dual_color_to_tuple(right_click_menu_selected_colors, (self.right_click_menu_background_color, self.right_click_menu_text_color))
        self.TKRightClickMenu = None
        self._grab_anywhere_ignore_these_list = []
        self._grab_anywhere_include_these_list = []
        self._has_custom_titlebar = use_custom_titlebar
        self._mousex = self._mousey = 0
        self._startx = self._starty = 0
        self.scaling = scaling if scaling is not None else FreeSimpleGUI.DEFAULT_SCALING
        if self.use_custom_titlebar:
            self.Margins = (0, 0)
            self.NoTitleBar = True
        self._mouse_offset_x = self._mouse_offset_y = 0

        if watermark is True:
            Window._watermark_temp_forced = True
            _global_settings_get_watermark_info()
        elif watermark is False:
            Window._watermark = None
            Window._watermark_temp_forced = False

        self.ttk_part_overrides = TTKPartOverrides(
            sbar_trough_color=sbar_trough_color,
            sbar_background_color=sbar_background_color,
            sbar_arrow_color=sbar_arrow_color,
            sbar_width=sbar_width,
            sbar_arrow_width=sbar_arrow_width,
            sbar_frame_color=sbar_frame_color,
            sbar_relief=sbar_relief,
        )

        if no_titlebar is True:
            self.override_custom_titlebar = True

        if layout is not None and type(layout) not in (list, tuple):
            warnings.warn('Your layout is not a list or tuple... this is not good!')

        if layout is not None:
            self.Layout(layout)
            if finalize:
                self.Finalize()

        if FreeSimpleGUI.CURRENT_LOOK_AND_FEEL == 'Default':
            print(
                'Window will be a boring gray. Try removing the theme call entirely\n',
                'You will get the default theme or the one set in global settings\n' "If you seriously want this gray window and no more nagging, add  theme('DefaultNoMoreNagging')  or theme('Gray Gray Gray') for completely gray/System Defaults",
            )

    @classmethod
    def _GetAContainerNumber(cls):
        """
        Not user callable!
        :return: A simple counter that makes each container element unique
        :rtype:
        """
        cls._container_element_counter += 1
        return cls._container_element_counter

    @classmethod
    def _IncrementOpenCount(self):
        """
        Not user callable!  Increments the number of open windows
        Note - there is a bug where this count easily gets out of sync. Issue has been opened already. No ill effects
        """
        self.NumOpenWindows += 1
        # print('+++++ INCREMENTING Num Open Windows = {} ---'.format(Window.NumOpenWindows))

    @classmethod
    def _DecrementOpenCount(self):
        """
        Not user callable!  Decrements the number of open windows
        """
        self.NumOpenWindows -= 1 * (self.NumOpenWindows != 0)  # decrement if not 0
        # print('----- DECREMENTING Num Open Windows = {} ---'.format(Window.NumOpenWindows))

    @classmethod
    def get_screen_size(self):
        """
        This is a "Class Method" meaning you call it by writing: width, height = Window.get_screen_size()
        Returns the size of the "screen" as determined by tkinter.  This can vary depending on your operating system and the number of monitors installed on your system.  For Windows, the primary monitor's size is returns. On some multi-monitored Linux systems, the monitors are combined and the total size is reported as if one screen.

        :return: Size of the screen in pixels as determined by tkinter
        :rtype:  (int, int)
        """
        root = _get_hidden_master_root()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        return screen_width, screen_height

    @property
    def metadata(self):
        """
        Metadata is available for all windows. You can set to any value.
        :return: the current metadata value
        :rtype:  (Any)
        """
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        """
        Metadata is available for all windows. You can set to any value.
        :param value: Anything you want it to be
        :type value:  (Any)
        """
        self._metadata = value

    # ------------------------- Add ONE Row to Form ------------------------- #
    def add_row(self, *args):
        """
        Adds a single row of elements to a window's self.Rows variables.
        Generally speaking this is NOT how users should be building Window layouts.
        Users, create a single layout (a list of lists) and pass as a parameter to Window object, or call Window.Layout(layout)

        :param *args: List[Elements]
        :type *args:
        """
        NumRows = len(self.Rows)  # number of existing rows is our row number
        CurrentRowNumber = NumRows  # this row's number
        CurrentRow = []  # start with a blank row and build up
        # -------------------------  Add the elements to a row  ------------------------- #
        for i, element in enumerate(args):  # Loop through list of elements and add them to the row

            if isinstance(element, tuple) or isinstance(element, list):
                self.add_row(*element)
                continue
                _error_popup_with_traceback(
                    'Error creating Window layout',
                    'Layout has a LIST instead of an ELEMENT',
                    'This sometimes means you have a badly placed ]',
                    'The offensive list is:',
                    element,
                    'This list will be stripped from your layout',
                )
                continue
            elif callable(element) and not isinstance(element, Element):
                _error_popup_with_traceback(
                    'Error creating Window layout',
                    'Layout has a FUNCTION instead of an ELEMENT',
                    'This likely means you are missing () from your layout',
                    'The offensive list is:',
                    element,
                    'This item will be stripped from your layout',
                )
                continue
            if element.ParentContainer is not None:
                warnings.warn(
                    '*** YOU ARE ATTEMPTING TO REUSE AN ELEMENT IN YOUR LAYOUT! Once placed in a layout, an element cannot be used in another layout. ***',
                    UserWarning,
                )
                _error_popup_with_traceback(
                    'Error detected in layout - Contains an element that has already been used.',
                    'You have attempted to reuse an element in your layout.',
                    "The layout specified has an element that's already been used.",
                    'You MUST start with a "clean", unused layout every time you create a window',
                    'The offensive Element = ',
                    element,
                    'and has a key = ',
                    element.Key,
                    'This item will be stripped from your layout',
                    'Hint - try printing your layout and matching the IDs "print(layout)"',
                )
                continue
            element.Position = (CurrentRowNumber, i)
            element.ParentContainer = self
            CurrentRow.append(element)
            # if this element is a titlebar, then automatically set the window margins to (0,0) and turn off normal titlebar
            if element.metadata == TITLEBAR_METADATA_MARKER:
                self.Margins = (0, 0)
                self.NoTitleBar = True
        # -------------------------  Append the row to list of Rows  ------------------------- #
        self.Rows.append(CurrentRow)

    # ------------------------- Add Multiple Rows to Form ------------------------- #
    def add_rows(self, rows):
        """
        Loops through a list of lists of elements and adds each row, list, to the layout.
        This is NOT the best way to go about creating a window.  Sending the entire layout at one time and passing
        it as a parameter to the Window call is better.

        :param rows: A list of a list of elements
        :type rows:  List[List[Elements]]
        """
        for row in rows:
            try:
                iter(row)
            except TypeError:
                _error_popup_with_traceback(
                    'Error Creating Window Layout',
                    'Error creating Window layout',
                    'Your row is not an iterable (e.g. a list)',
                    f'Instead of a list, the type found was {type(row)}',
                    'The offensive row = ',
                    row,
                    'This item will be stripped from your layout',
                )
                continue
            self.add_row(*row)
        if Window._watermark is not None:
            self.add_row(Window._watermark(self))

    def layout(self, rows):
        """
        Second of two preferred ways of telling a Window what its layout is. The other way is to pass the layout as
        a parameter to Window object.  The parameter method is the currently preferred method. This call to Layout
        has been removed from examples contained in documents and in the Demo Programs. Trying to remove this call
        from history and replace with sending as a parameter to Window.

        :param rows: Your entire layout
        :type rows:  List[List[Elements]]
        :return:     self so that you can chain method calls
        :rtype:      (Window)
        """
        if self.use_custom_titlebar and not self.override_custom_titlebar:
            if self.titlebar_icon is not None:
                icon = self.titlebar_icon
            elif FreeSimpleGUI.CUSTOM_TITLEBAR_ICON is not None:
                icon = FreeSimpleGUI.CUSTOM_TITLEBAR_ICON
            elif self.titlebar_icon is not None:
                icon = self.titlebar_icon
            elif self.WindowIcon == FreeSimpleGUI.DEFAULT_WINDOW_ICON:
                icon = FreeSimpleGUI.DEFAULT_BASE64_ICON_16_BY_16
            else:
                icon = None

            new_rows = [
                [
                    Titlebar(
                        title=self.Title,
                        icon=icon,
                        text_color=self.titlebar_text_color,
                        background_color=self.titlebar_background_color,
                        font=self.titlebar_font,
                    )
                ]
            ] + rows
        else:
            new_rows = rows
        self.add_rows(new_rows)
        self._BuildKeyDict()

        if self._has_custom_titlebar_element():
            self.Margins = (0, 0)
            self.NoTitleBar = True
            self._has_custom_titlebar = True
        return self

    def extend_layout(self, container, rows):
        """
        Adds new rows to an existing container element inside of this window
        If the container is a scrollable Column, you need to also call the contents_changed() method

        :param container: The container Element the layout will be placed inside of
        :type container:  Frame | Column | Tab
        :param rows:      The layout to be added
        :type rows:       (List[List[Element]])
        :return:          (Window) self so could be chained
        :rtype:           (Window)
        """
        column = Column(rows, pad=(0, 0), background_color=container.BackgroundColor)
        if self == container:
            frame = self.TKroot
        elif isinstance(container.Widget, TkScrollableFrame):
            frame = container.Widget.TKFrame
        else:
            frame = container.Widget
        PackFormIntoFrame(column, frame, self)
        # sg.PackFormIntoFrame(col, window.TKroot, window)
        self.AddRow(column)
        self.AllKeysDict = self._BuildKeyDictForWindow(self, column, self.AllKeysDict)
        return self

    def LayoutAndRead(self, rows, non_blocking=False):
        """
        Deprecated!!  Now your layout your window's rows (layout) and then separately call Read.

        :param rows:         The layout of the window
        :type rows:          List[List[Element]]
        :param non_blocking: if True the Read call will not block
        :type non_blocking:  (bool)
        """
        _error_popup_with_traceback(
            'LayoutAndRead Depricated',
            'Wow!  You have been using PySimpleGUI for a very long time.',
            'The Window.LayoutAndRead call is no longer supported',
        )

        raise DeprecationWarning('LayoutAndRead is no longer supported... change your call window.Layout(layout).Read()\nor window(title, layout).Read()')

    def LayoutAndShow(self, rows):
        """
        Deprecated - do not use any longer.  Layout your window and then call Read.  Or can add a Finalize call before the Read
        """
        raise DeprecationWarning('LayoutAndShow is no longer supported... ')

    def _Show(self, non_blocking=False):
        """
        NOT TO BE CALLED BY USERS.  INTERNAL ONLY!
        It's this method that first shows the window to the user, collects results

        :param non_blocking: if True, this is a non-blocking call
        :type non_blocking:  (bool)
        :return:             Tuple[Any, Dict] The event, values turple that is returned from Read calls
        :rtype:
        """
        self.Shown = True
        # Compute num rows & num cols (it'll come in handy debugging)
        self.NumRows = len(self.Rows)
        self.NumCols = max(len(row) for row in self.Rows)
        self.NonBlocking = non_blocking

        # Search through entire form to see if any elements set the focus
        # if not, then will set the focus to the first input element
        found_focus = False
        for row in self.Rows:
            for element in row:
                try:
                    if element.Focus:
                        found_focus = True
                except:
                    pass
                try:
                    if element.Key is not None:
                        self.UseDictionary = True
                except:
                    pass

        if not found_focus and self.UseDefaultFocus:
            self.UseDefaultFocus = True
        else:
            self.UseDefaultFocus = False
        # -=-=-=-=-=-=-=-=- RUN the GUI -=-=-=-=-=-=-=-=- ##
        StartupTK(self)
        # If a button or keyboard event happened but no results have been built, build the results
        if self.LastKeyboardEvent is not None or self.LastButtonClicked is not None:
            return _BuildResults(self, False, self)
        return self.ReturnValues

    # ------------------------- SetIcon - set the window's fav icon ------------------------- #
    def set_icon(self, icon=None, pngbase64=None):
        """
        Changes the icon that is shown on the title bar and on the task bar.
        NOTE - The file type is IMPORTANT and depends on the OS!
        Can pass in:
        * filename which must be a .ICO icon file for windows, PNG file for Linux
        * bytes object
        * BASE64 encoded file held in a variable

        :param icon:      Filename or bytes object
        :type icon:       (str)
        :param pngbase64: Base64 encoded image
        :type pngbase64:  (bytes)
        """
        if type(icon) is bytes or pngbase64 is not None:
            wicon = tkinter.PhotoImage(data=icon if icon is not None else pngbase64)
            try:
                self.TKroot.tk.call('wm', 'iconphoto', self.TKroot._w, wicon)
            except:
                wicon = tkinter.PhotoImage(data=FreeSimpleGUI.DEFAULT_BASE64_ICON)
                try:
                    self.TKroot.tk.call('wm', 'iconphoto', self.TKroot._w, wicon)
                except:
                    pass
            self.WindowIcon = wicon
            return

        wicon = icon
        try:
            self.TKroot.iconbitmap(icon)
        except:
            try:
                wicon = tkinter.PhotoImage(file=icon)
                self.TKroot.tk.call('wm', 'iconphoto', self.TKroot._w, wicon)
            except:
                try:
                    wicon = tkinter.PhotoImage(data=FreeSimpleGUI.DEFAULT_BASE64_ICON)
                    try:
                        self.TKroot.tk.call('wm', 'iconphoto', self.TKroot._w, wicon)
                    except:
                        pass
                except:
                    pass
        self.WindowIcon = wicon

    def _GetElementAtLocation(self, location):
        """
        Given a (row, col) location in a layout, return the element located at that position

        :param location: (int, int) Return the element located at (row, col) in layout
        :type location:
        :return:         (Element) The Element located at that position in this window
        :rtype:
        """

        (row_num, col_num) = location
        row = self.Rows[row_num]
        element = row[col_num]
        return element

    def _GetDefaultElementSize(self):
        """
        Returns the default elementSize

        :return: (width, height) of the default element size
        :rtype:  (int, int)
        """

        return self.DefaultElementSize

    def _AutoCloseAlarmCallback(self):
        """
        Function that's called by tkinter when autoclode timer expires.  Closes the window

        """
        try:
            window = self
            if window:
                if window.NonBlocking:
                    self.Close()
                else:
                    window._Close()
                    self.TKroot.quit()
                    self.RootNeedsDestroying = True
        except:
            pass

    def _TimeoutAlarmCallback(self):
        """
        Read Timeout Alarm callback. Will kick a mainloop call out of the tkinter event loop and cause it to return
        """
        # first, get the results table built
        # modify the Results table in the parent FlexForm object
        # print('TIMEOUT CALLBACK')
        if self.TimerCancelled:
            # print('** timer was cancelled **')
            return
        self.LastButtonClicked = self.TimeoutKey
        self.FormRemainedOpen = True
        self.TKroot.quit()  # kick the users out of the mainloop

    def _calendar_chooser_button_clicked(self, elem):
        """

        :param elem:
        :type elem:
        :return:
        :rtype:
        """
        target_element, strvar, should_submit_window = elem._find_target()

        if elem.calendar_default_date_M_D_Y == (None, None, None):
            now = datetime.datetime.now()
            cur_month, cur_day, cur_year = now.month, now.day, now.year
        else:
            cur_month, cur_day, cur_year = elem.calendar_default_date_M_D_Y

        date_chosen = popup_get_date(
            start_mon=cur_month,
            start_day=cur_day,
            start_year=cur_year,
            close_when_chosen=elem.calendar_close_when_chosen,
            no_titlebar=elem.calendar_no_titlebar,
            begin_at_sunday_plus=elem.calendar_begin_at_sunday_plus,
            locale=elem.calendar_locale,
            location=elem.calendar_location,
            month_names=elem.calendar_month_names,
            day_abbreviations=elem.calendar_day_abbreviations,
            title=elem.calendar_title,
        )
        if date_chosen is not None:
            month, day, year = date_chosen
            now = datetime.datetime.now()
            hour, minute, second = now.hour, now.minute, now.second
            try:
                date_string = calendar.datetime.datetime(year, month, day, hour, minute, second).strftime(elem.calendar_format)
            except Exception as e:
                print('Bad format string in calendar chooser button', e)
                date_string = 'Bad format string'

            if target_element is not None and target_element != elem:
                target_element.update(date_string)
            elif target_element == elem:
                elem.calendar_selection = date_string

            strvar.set(date_string)
            elem.TKStringVar.set(date_string)
            if should_submit_window:
                self.LastButtonClicked = target_element.Key
                _BuildResults(self, False, self)
        else:
            should_submit_window = False
        return should_submit_window

    # @_timeit_summary
    def read(self, timeout=None, timeout_key=TIMEOUT_KEY, close=False):
        """
        THE biggest deal method in the Window class! This is how you get all of your data from your Window.
            Pass in a timeout (in milliseconds) to wait for a maximum of timeout milliseconds. Will return timeout_key
            if no other GUI events happen first.

        :param timeout:     Milliseconds to wait until the Read will return IF no other GUI events happen first
        :type timeout:      (int)
        :param timeout_key: The value that will be returned from the call if the timer expired
        :type timeout_key:  (Any)
        :param close:       if True the window will be closed prior to returning
        :type close:        (bool)
        :return:            (event, values)
        :rtype:             Tuple[(Any), Dict[Any, Any], List[Any], None]
        """

        if Window._floating_debug_window_build_needed is True:
            Window._floating_debug_window_build_needed = False
            _Debugger.debugger._build_floating_window()

        if Window._main_debug_window_build_needed is True:
            Window._main_debug_window_build_needed = False
            _Debugger.debugger._build_main_debugger_window()

        # ensure called only 1 time through a single read cycle
        if not Window._read_call_from_debugger:
            _refresh_debugger()

        # if the user has not added timeout and a debug window is open, then set a timeout for them so the debugger continuously refreshes
        if _debugger_window_is_open() and not Window._read_call_from_debugger:
            if timeout is None or timeout > 3000:
                timeout = 200

        while True:
            Window._root_running_mainloop = self.TKroot
            results = self._read(timeout=timeout, timeout_key=timeout_key)
            if results is not None:
                if results[0] == FreeSimpleGUI.DEFAULT_WINDOW_SNAPSHOT_KEY:
                    self.save_window_screenshot_to_disk()
                    popup_quick_message(
                        'Saved window screenshot to disk',
                        background_color='#1c1e23',
                        text_color='white',
                        keep_on_top=True,
                        font='_ 30',
                    )
                    continue
            # Post processing for Calendar Chooser Button
            try:
                if results[0] == timeout_key:  # if a timeout, then not a calendar button
                    break
                elem = self.find_element(results[0], silent_on_error=True)  # get the element that caused the event
                if elem.Type == ELEM_TYPE_BUTTON:
                    if elem.BType == BUTTON_TYPE_CALENDAR_CHOOSER:
                        if self._calendar_chooser_button_clicked(elem):  # returns True if should break out
                            results = self.ReturnValues
                            break
                        else:
                            continue
                break
            except:
                break  # wasn't a calendar button for sure

        if close:
            self.close()

        return results

    # @_timeit
    def _read(self, timeout=None, timeout_key=TIMEOUT_KEY):
        """
        THE biggest deal method in the Window class! This is how you get all of your data from your Window.
            Pass in a timeout (in milliseconds) to wait for a maximum of timeout milliseconds. Will return timeout_key
            if no other GUI events happen first.

        :param timeout:     Milliseconds to wait until the Read will return IF no other GUI events happen first
        :type timeout:      (int)
        :param timeout_key: The value that will be returned from the call if the timer expired
        :type timeout_key:  (Any)
        :return:            (event, values) (event or timeout_key or None, Dictionary of values or List of values from all elements in the Window)
        :rtype:             Tuple[(Any), Dict[Any, Any], List[Any], None]
        """

        # if there are events in the thread event queue, then return those events before doing anything else.
        if self._queued_thread_event_available():
            self.ReturnValues = results = _BuildResults(self, False, self)
            return results

        if self.finalize_in_progress and self.auto_close_timer_needs_starting:
            self._start_autoclose_timer()
            self.auto_close_timer_needs_starting = False

        timeout = int(timeout) if timeout is not None else None
        if timeout == 0:  # timeout of zero runs the old readnonblocking
            event, values = self._ReadNonBlocking()
            if event is None:
                event = timeout_key
            if values is None:
                event = None
            return event, values  # make event None if values was None and return
        # Read with a timeout
        self.Timeout = timeout
        self.TimeoutKey = timeout_key
        self.NonBlocking = False
        if self.TKrootDestroyed:
            self.read_closed_window_count += 1
            if self.read_closed_window_count > 100:
                popup_error_with_traceback(
                    'Trying to read a closed window',
                    'You have tried 100 times to read a closed window.',
                    'You need to add a check for event == WIN_CLOSED',
                )
            return None, None
        if not self.Shown:
            self._Show()
        else:
            # if already have a button waiting, the return previously built results
            if self.LastButtonClicked is not None and not self.LastButtonClickedWasRealtime:
                results = _BuildResults(self, False, self)
                self.LastButtonClicked = None
                return results
            InitializeResults(self)

            if self._queued_thread_event_available():
                self.ReturnValues = results = _BuildResults(self, False, self)
                return results

            # if the last button clicked was realtime, emulate a read non-blocking
            # the idea is to quickly return realtime buttons without any blocks until released
            if self.LastButtonClickedWasRealtime:
                # clear the realtime flag if the element is not a button element (for example a graph element that is dragging)
                if self.AllKeysDict.get(self.LastButtonClicked, None):
                    if self.AllKeysDict.get(self.LastButtonClicked).Type != ELEM_TYPE_BUTTON:
                        self.LastButtonClickedWasRealtime = False  # stops from generating events until something changes
                else:  # it is possible for the key to not be in the dicitonary because it has a modifier. If so, then clear the realtime button flag
                    self.LastButtonClickedWasRealtime = False  # stops from generating events until something changes

                try:
                    self.TKroot.update()
                except:
                    self.TKrootDestroyed = True
                    Window._DecrementOpenCount()
                results = _BuildResults(self, False, self)
                if results[0] is not None and results[0] != timeout_key:
                    return results
                else:
                    pass
            if self.RootNeedsDestroying:
                try:
                    self.TKroot.destroy()
                except:
                    pass
                # _my_windows.Decrement()
                self.LastButtonClicked = None
                return None, None

            # normal read blocking code....
            if timeout is not None:
                self.TimerCancelled = False
                self.TKAfterID = self.TKroot.after(timeout, self._TimeoutAlarmCallback)
            self.CurrentlyRunningMainloop = True
            Window._window_running_mainloop = self
            try:
                Window._root_running_mainloop.mainloop()
            except:
                print('**** EXITING ****')
                sys.exit(-1)
            # print('Out main')
            self.CurrentlyRunningMainloop = False
            # if self.LastButtonClicked != TIMEOUT_KEY:
            try:
                self.TKroot.after_cancel(self.TKAfterID)
                del self.TKAfterID
            except:
                pass
                # print('** tkafter cancel failed **')
            self.TimerCancelled = True
            if self.RootNeedsDestroying:
                # print('*** DESTROYING LATE ***')
                try:
                    self.TKroot.destroy()
                except:
                    pass
                Window._DecrementOpenCount()
                # _my_windows.Decrement()
                self.LastButtonClicked = None
                return None, None
            # if form was closed with X
            if self.LastButtonClicked is None and self.LastKeyboardEvent is None and self.ReturnValues[0] is None:
                Window._DecrementOpenCount()
        # Determine return values
        if self.LastKeyboardEvent is not None or self.LastButtonClicked is not None:
            results = _BuildResults(self, False, self)
            if not self.LastButtonClickedWasRealtime:
                self.LastButtonClicked = None
            return results
        else:
            if self._queued_thread_event_available():
                self.ReturnValues = results = _BuildResults(self, False, self)
                return results
            if not self.XFound and self.Timeout != 0 and self.Timeout is not None and self.ReturnValues[0] is None:  # Special Qt case because returning for no reason so fake timeout
                self.ReturnValues = self.TimeoutKey, self.ReturnValues[1]  # fake a timeout
            elif not self.XFound and self.ReturnValues[0] is None:  # Return a timeout event... can happen when autoclose used on another window
                self.ReturnValues = self.TimeoutKey, self.ReturnValues[1]  # fake a timeout
            return self.ReturnValues

    def _ReadNonBlocking(self):
        """
        Should be NEVER called directly by the user.  The user can call Window.read(timeout=0) to get same effect

        :return: (event, values). (event or timeout_key or None, Dictionary of values or List of values from all elements in the Window)
        :rtype:  Tuple[(Any), Dict[Any, Any] | List[Any] | None]
        """
        if self.TKrootDestroyed:
            try:
                self.TKroot.quit()
                self.TKroot.destroy()
            except:
                pass
                # print('DESTROY FAILED')
            return None, None
        if not self.Shown:
            self._Show(non_blocking=True)
        try:
            self.TKroot.update()
        except:
            self.TKrootDestroyed = True
            Window._DecrementOpenCount()
        if self.RootNeedsDestroying:
            self.TKroot.destroy()
            Window._DecrementOpenCount()
            self.Values = None
            self.LastButtonClicked = None
            return None, None
        return _BuildResults(self, False, self)

    def _start_autoclose_timer(self):
        duration = FreeSimpleGUI.DEFAULT_AUTOCLOSE_TIME if self.AutoCloseDuration is None else self.AutoCloseDuration
        self.TKAfterID = self.TKroot.after(int(duration * 1000), self._AutoCloseAlarmCallback)

    def finalize(self):
        """
        Use this method to cause your layout to built into a real tkinter window.  In reality this method is like
        Read(timeout=0).  It doesn't block and uses your layout to create tkinter widgets to represent the elements.
        Lots of action!

        :return: Returns 'self' so that method "Chaining" can happen (read up about it as it's very cool!)
        :rtype:  (Window)
        """

        if self.TKrootDestroyed:
            return self
        self.finalize_in_progress = True

        self.Read(timeout=1)

        if self.AutoClose:
            self.auto_close_timer_needs_starting = True
        # add the window to the list of active windows
        Window._active_windows[self] = Window.hidden_master_root
        return self
        # OLD CODE FOLLOWS
        if not self.Shown:
            self._Show(non_blocking=True)
        try:
            self.TKroot.update()
        except:
            self.TKrootDestroyed = True
            Window._DecrementOpenCount()
            print('** Finalize failed **')
        return self

    def refresh(self):
        """
        Refreshes the window by calling tkroot.update().  Can sometimes get away with a refresh instead of a Read.
        Use this call when you want something to appear in your Window immediately (as soon as this function is called).
        If you change an element in a window, your change will not be visible until the next call to Window.read
        or a call to Window.refresh()

        :return: `self` so that method calls can be easily "chained"
        :rtype:  (Window)
        """

        if self.TKrootDestroyed:
            return self
        try:
            self.TKroot.update()
        except:
            pass
        return self

    def fill(self, values_dict):
        """
        Fill in elements that are input fields with data based on a 'values dictionary'

        :param values_dict: pairs
        :type values_dict:  (Dict[Any, Any]) - {Element_key : value}
        :return:            returns self so can be chained with other methods
        :rtype:             (Window)
        """

        fill_form_with_values(self, values_dict)
        return self

    def _find_closest_key(self, search_key):
        if not isinstance(search_key, str):
            search_key = str(search_key)
        matches = difflib.get_close_matches(search_key, [str(k) for k in self.AllKeysDict.keys()])
        if not len(matches):
            return None
        for k in self.AllKeysDict.keys():
            if matches[0] == str(k):
                return k
        return matches[0] if len(matches) else None

    def FindElement(self, key, silent_on_error=False):
        """
        ** Warning ** This call will eventually be depricated. **

        It is suggested that you modify your code to use the recommended window[key] lookup or the PEP8 compliant window.find_element(key)

        For now, you'll only see a message printed and the call will continue to funcation as before.

        :param key:             Used with window.find_element and with return values to uniquely identify this element
        :type key:              str | int | tuple | object
        :param silent_on_error: If True do not display popup nor print warning of key errors
        :type silent_on_error:  (bool)
        :return:                Return value can be: the Element that matches the supplied key if found; an Error Element if silent_on_error is False; None if silent_on_error True;
        :rtype:                 Element | Error Element | None
        """

        warnings.warn(
            'Use of FindElement is not recommended.\nEither switch to the recommended window[key] format\nor the PEP8 compliant find_element',
            UserWarning,
        )
        print('** Warning - FindElement should not be used to look up elements. window[key] or window.find_element are recommended. **')

        return self.find_element(key, silent_on_error=silent_on_error)

    def find_element(self, key, silent_on_error=False, supress_guessing=None, supress_raise=None):
        """
        Find element object associated with the provided key.
        THIS METHOD IS NO LONGER NEEDED to be called by the user

        You can perform the same operation by writing this statement:
        element = window[key]

        You can drop the entire "find_element" function name and use [ ] instead.

        However, if you wish to perform a lookup without error checking, and don't have error popups turned
        off globally, you'll need to make this call so that you can disable error checks on this call.

        find_element is typically used in combination with a call to element's update method (or any other element method!):
        window[key].update(new_value)

        Versus the "old way"
        window.FindElement(key).Update(new_value)

        This call can be abbreviated to any of these:
        find_element = FindElement == Element == Find
        With find_element being the PEP8 compliant call that should be used.

        Rememeber that this call will return None if no match is found which may cause your code to crash if not
        checked for.

        :param key:              Used with window.find_element and with return values to uniquely identify this element
        :type key:               str | int | tuple | object
        :param silent_on_error:  If True do not display popup nor print warning of key errors
        :type silent_on_error:   (bool)
        :param supress_guessing: Override for the global key guessing setting.
        :type supress_guessing:  (bool | None)
        :param supress_raise:    Override for the global setting that determines if a key error should raise an exception
        :type supress_raise:     (bool | None)
        :return:                 Return value can be: the Element that matches the supplied key if found; an Error Element if silent_on_error is False; None if silent_on_error True
        :rtype:                  Element | FreeSimpleGUI.elements.error.ErrorElement | None
        """

        key_error = False
        closest_key = None
        supress_guessing = supress_guessing if supress_guessing is not None else FreeSimpleGUI.SUPPRESS_KEY_GUESSING
        supress_raise = supress_raise if supress_raise is not None else FreeSimpleGUI.SUPPRESS_RAISE_KEY_ERRORS
        try:
            element = self.AllKeysDict[key]
        except KeyError:
            key_error = True
            closest_key = self._find_closest_key(key)
            if not silent_on_error:
                print('** Error looking up your element using the key: ', key, 'The closest matching key: ', closest_key)
                _error_popup_with_traceback(
                    'Key Error',
                    'Problem finding your key ' + str(key),
                    'Closest match = ' + str(closest_key),
                    emoji=EMOJI_BASE64_KEY,
                )
                element = ErrorElement(key=key)
            else:
                element = None
            if not supress_raise:
                raise KeyError(key)

        if key_error:
            if not supress_guessing and closest_key is not None:
                element = self.AllKeysDict[closest_key]

        return element

    Element = find_element  # Shortcut function
    Find = find_element  # Shortcut function, most likely not used by many people.
    Elem = find_element  # NEW for 2019!  More laziness... Another shortcut

    def find_element_with_focus(self):
        """
        Returns the Element that currently has focus as reported by tkinter. If no element is found None is returned!
        :return: An Element if one has been found with focus or None if no element found
        :rtype:  Element | None
        """
        element = _FindElementWithFocusInSubForm(self)
        return element

    def widget_to_element(self, widget):
        """
        Returns the element that matches a supplied tkinter widget.
        If no matching element is found, then None is returned.


        :return:    Element that uses the specified widget
        :rtype:     Element | None
        """
        if self.AllKeysDict is None or len(self.AllKeysDict) == 0:
            return None
        for key, element in self.AllKeysDict.items():
            if element.Widget == widget:
                return element
        return None

    def _BuildKeyDict(self):
        """
        Used internally only! Not user callable
        Builds a dictionary containing all elements with keys for this window.
        """
        dict = {}
        self.AllKeysDict = self._BuildKeyDictForWindow(self, self, dict)

    def _BuildKeyDictForWindow(self, top_window, window, key_dict):
        """
        Loop through all Rows and all Container Elements for this window and create the keys for all of them.
        Note that the calls are recursive as all pathes must be walked

        :param top_window: The highest level of the window
        :type top_window:  (Window)
        :param window:     The "sub-window" (container element) to be searched
        :type window:      Column | Frame | FreeSimpleGUI.elements.tab.TabGroup | FreeSimpleGUI.elements.pane.Pane | FreeSimpleGUI.elements.tab.Tab
        :param key_dict:   The dictionary as it currently stands.... used as part of recursive call
        :type key_dict:
        :return:           (dict) Dictionary filled with all keys in the window
        :rtype:
        """
        for row_num, row in enumerate(window.Rows):
            for col_num, element in enumerate(row):
                if element.Type == ELEM_TYPE_COLUMN:
                    key_dict = self._BuildKeyDictForWindow(top_window, element, key_dict)
                if element.Type == ELEM_TYPE_FRAME:
                    key_dict = self._BuildKeyDictForWindow(top_window, element, key_dict)
                if element.Type == ELEM_TYPE_TAB_GROUP:
                    key_dict = self._BuildKeyDictForWindow(top_window, element, key_dict)
                if element.Type == ELEM_TYPE_PANE:
                    key_dict = self._BuildKeyDictForWindow(top_window, element, key_dict)
                if element.Type == ELEM_TYPE_TAB:
                    key_dict = self._BuildKeyDictForWindow(top_window, element, key_dict)
                if element.Key is None:  # if no key has been assigned.... create one for input elements
                    if element.Type == ELEM_TYPE_BUTTON:
                        element.Key = element.ButtonText
                    elif element.Type == ELEM_TYPE_TAB:
                        element.Key = element.Title
                    if element.Type in (
                        ELEM_TYPE_MENUBAR,
                        ELEM_TYPE_BUTTONMENU,
                        ELEM_TYPE_INPUT_SLIDER,
                        ELEM_TYPE_GRAPH,
                        ELEM_TYPE_IMAGE,
                        ELEM_TYPE_INPUT_CHECKBOX,
                        ELEM_TYPE_INPUT_LISTBOX,
                        ELEM_TYPE_INPUT_COMBO,
                        ELEM_TYPE_INPUT_MULTILINE,
                        ELEM_TYPE_INPUT_OPTION_MENU,
                        ELEM_TYPE_INPUT_SPIN,
                        ELEM_TYPE_INPUT_RADIO,
                        ELEM_TYPE_INPUT_TEXT,
                        ELEM_TYPE_PROGRESS_BAR,
                        ELEM_TYPE_TABLE,
                        ELEM_TYPE_TREE,
                        ELEM_TYPE_TAB_GROUP,
                        ELEM_TYPE_SEPARATOR,
                    ):
                        element.Key = top_window.DictionaryKeyCounter
                        top_window.DictionaryKeyCounter += 1
                if element.Key is not None:
                    if element.Key in key_dict.keys():
                        if element.Type == ELEM_TYPE_BUTTON and FreeSimpleGUI.WARN_DUPLICATE_BUTTON_KEY_ERRORS:  # for Buttons see if should complain
                            warnings.warn(f'*** Duplicate key found in your layout {element.Key} ***', UserWarning)
                            warnings.warn(f'*** Replaced new key with {str(element.Key) + str(self.UniqueKeyCounter)} ***')
                            if not FreeSimpleGUI.SUPPRESS_ERROR_POPUPS:
                                _error_popup_with_traceback(
                                    'Duplicate key found in your layout',
                                    f'Dupliate key: {element.Key}',
                                    f'Is being replaced with: {str(element.Key) + str(self.UniqueKeyCounter)}',
                                    'The line of code above shows you which layout, but does not tell you exactly where the element was defined',
                                    f'The element type is {element.Type}',
                                )
                        element.Key = str(element.Key) + str(self.UniqueKeyCounter)
                        self.UniqueKeyCounter += 1
                    key_dict[element.Key] = element
        return key_dict

    def element_list(self):
        """
        Returns a list of all elements in the window

        :return: List of all elements in the window and container elements in the window
        :rtype:  List[Element]
        """
        return self._build_element_list()

    def _build_element_list(self):
        """
        Used internally only! Not user callable
        Builds a dictionary containing all elements with keys for this window.
        """
        elem_list = []
        elem_list = self._build_element_list_for_form(self, self, elem_list)
        return elem_list

    def _build_element_list_for_form(self, top_window, window, elem_list):
        """
        Loop through all Rows and all Container Elements for this window and create a list
        Note that the calls are recursive as all pathes must be walked

        :param top_window: The highest level of the window
        :type top_window:  (Window)
        :param window:     The "sub-window" (container element) to be searched
        :type window:      Column | Frame | TabGroup | Pane | Tab
        :param elem_list:  The element list as it currently stands.... used as part of recursive call
        :type elem_list:   ???
        :return:           List of all elements in this sub-window
        :rtype:            List[Element]
        """
        for row_num, row in enumerate(window.Rows):
            for col_num, element in enumerate(row):
                elem_list.append(element)
                if element.Type in (
                    ELEM_TYPE_COLUMN,
                    ELEM_TYPE_FRAME,
                    ELEM_TYPE_TAB_GROUP,
                    ELEM_TYPE_PANE,
                    ELEM_TYPE_TAB,
                ):
                    elem_list = self._build_element_list_for_form(top_window, element, elem_list)
        return elem_list

    def save_to_disk(self, filename):
        """
        Saves the values contained in each of the input areas of the form. Basically saves what would be returned from a call to Read.  It takes these results and saves them to disk using pickle.
         Note that every element in your layout that is to be saved must have a key assigned to it.

        :param filename: Filename to save the values to in pickled form
        :type filename:  str
        """
        try:
            event, values = _BuildResults(self, False, self)
            remove_these = []
            for key in values:
                if self.Element(key).Type == ELEM_TYPE_BUTTON:
                    remove_these.append(key)
            for key in remove_these:
                del values[key]
            with open(filename, 'wb') as sf:
                pickle.dump(values, sf)
        except:
            print('*** Error saving Window contents to disk ***')

    def load_from_disk(self, filename):
        """
        Restore values from a previous call to SaveToDisk which saves the returned values dictionary in Pickle format

        :param filename: Pickle Filename to load
        :type filename:  (str)
        """
        try:
            with open(filename, 'rb') as df:
                self.Fill(pickle.load(df))
        except:
            print('*** Error loading form to disk ***')

    def get_screen_dimensions(self):
        """
        Get the screen dimensions.  NOTE - you must have a window already open for this to work (blame tkinter not me)

        :return: Tuple containing width and height of screen in pixels
        :rtype:  Tuple[None, None] | Tuple[width, height]
        """

        if self.TKrootDestroyed or self.TKroot is None:
            return Window.get_screen_size()
        screen_width = self.TKroot.winfo_screenwidth()  # get window info to move to middle of screen
        screen_height = self.TKroot.winfo_screenheight()
        return screen_width, screen_height

    def move(self, x, y):
        """
        Move the upper left corner of this window to the x,y coordinates provided
        :param x: x coordinate in pixels
        :type x:  (int)
        :param y: y coordinate in pixels
        :type y:  (int)
        """
        try:
            self.TKroot.geometry('+{}+{}'.format(x, y))
            self.config_last_location = (int(x), (int(y)))

        except:
            pass

    def move_to_center(self):
        """
        Recenter your window after it's been moved or the size changed.

        This is a conveinence method. There are no tkinter calls involved, only pure PySimpleGUI API calls.
        """
        if not self._is_window_created('tried Window.move_to_center'):
            return
        screen_width, screen_height = self.get_screen_dimensions()
        win_width, win_height = self.size
        x, y = (screen_width - win_width) // 2, (screen_height - win_height) // 2
        self.move(x, y)

    def minimize(self):
        """
        Minimize this window to the task bar
        """
        if not self._is_window_created('tried Window.minimize'):
            return
        if self.use_custom_titlebar is True:
            self._custom_titlebar_minimize()
        else:
            self.TKroot.iconify()
        self.maximized = False

    def maximize(self):
        """
        Maximize the window. This is done differently on a windows system versus a linux or mac one.  For non-Windows
        the root attribute '-fullscreen' is set to True.  For Windows the "root" state is changed to "zoomed"
        The reason for the difference is the title bar is removed in some cases when using fullscreen option
        """

        if not self._is_window_created('tried Window.maximize'):
            return
        if not running_linux():
            self.TKroot.state('zoomed')
        else:
            self.TKroot.attributes('-fullscreen', True)
        self.maximized = True

    def normal(self):
        """
        Restore a window to a non-maximized state.  Does different things depending on platform.  See Maximize for more.
        """
        if not self._is_window_created('tried Window.normal'):
            return
        if self.use_custom_titlebar:
            self._custom_titlebar_restore()
        else:
            if self.TKroot.state() == 'iconic':
                self.TKroot.deiconify()
            else:
                if not running_linux():
                    self.TKroot.state('normal')
                else:
                    self.TKroot.attributes('-fullscreen', False)
            self.maximized = False

    def _StartMoveUsingControlKey(self, event):
        """
        Used by "Grab Anywhere" style windows. This function is bound to mouse-down. It marks the beginning of a drag.
        :param event: event information passed in by tkinter. Contains x,y position of mouse
        :type event:  (event)
        """
        self._start_move_save_offset(event)
        return

    def _StartMoveGrabAnywhere(self, event):
        """
        Used by "Grab Anywhere" style windows. This function is bound to mouse-down. It marks the beginning of a drag.
        :param event: event information passed in by tkinter. Contains x,y position of mouse
        :type event:  (event)
        """
        if (isinstance(event.widget, GRAB_ANYWHERE_IGNORE_THESE_WIDGETS) or event.widget in self._grab_anywhere_ignore_these_list) and event.widget not in self._grab_anywhere_include_these_list:
            # print('Found widget to ignore in grab anywhere...')
            return
        self._start_move_save_offset(event)

    def _StartMove(self, event):
        self._start_move_save_offset(event)
        return

    def _StopMove(self, event):
        """
        Used by "Grab Anywhere" style windows. This function is bound to mouse-up. It marks the ending of a drag.
        Sets the position of the window to this final x,y coordinates
        :param event: event information passed in by tkinter. Contains x,y position of mouse
        :type event:  (event)
        """
        return

    def _start_move_save_offset(self, event):
        self._mousex = event.x + event.widget.winfo_rootx()
        self._mousey = event.y + event.widget.winfo_rooty()
        geometry = self.TKroot.geometry()
        location = geometry[geometry.find('+') + 1 :].split('+')
        self._startx = int(location[0])
        self._starty = int(location[1])
        self._mouse_offset_x = self._mousex - self._startx
        self._mouse_offset_y = self._mousey - self._starty
        # ------ Move All Windows code ------
        if Window._move_all_windows:
            # print('Moving all')
            for win in Window._active_windows:
                if win == self:
                    continue
                geometry = win.TKroot.geometry()
                location = geometry[geometry.find('+') + 1 :].split('+')
                _startx = int(location[0])
                _starty = int(location[1])
                win._mouse_offset_x = event.x_root - _startx
                win._mouse_offset_y = event.y_root - _starty

    def _OnMotionUsingControlKey(self, event):
        self._OnMotion(event)

    def _OnMotionGrabAnywhere(self, event):
        """
        Used by "Grab Anywhere" style windows. This function is bound to mouse motion. It actually moves the window
        :param event: event information passed in by tkinter. Contains x,y position of mouse
        :type event:  (event)
        """
        if (isinstance(event.widget, GRAB_ANYWHERE_IGNORE_THESE_WIDGETS) or event.widget in self._grab_anywhere_ignore_these_list) and event.widget not in self._grab_anywhere_include_these_list:
            # print('Found widget to ignore in grab anywhere...')
            return

        self._OnMotion(event)

    def _OnMotion(self, event):

        self.TKroot.geometry(f'+{event.x_root - self._mouse_offset_x}+{event.y_root - self._mouse_offset_y}')
        # ------ Move All Windows code ------
        try:
            if Window._move_all_windows:
                for win in Window._active_windows:
                    if win == self:
                        continue
                    win.TKroot.geometry(f'+{event.x_root - win._mouse_offset_x}+{event.y_root - win._mouse_offset_y}')
        except Exception as e:
            print('on motion error', e)

    def _focus_callback(self, event):
        print(f'Focus event = {event} window = {self.Title}')

    def _config_callback(self, event):
        """
        Called when a config event happens for the window

        :param event:            From tkinter and is not used
        :type event:             Any
        """
        self.LastButtonClicked = WINDOW_CONFIG_EVENT
        self.FormRemainedOpen = True
        self.user_bind_event = event
        _exit_mainloop(self)

    def _move_callback(self, event):
        """
        Called when a control + arrow key is pressed.
        This is a built-in window positioning key sequence

        :param event:            From tkinter and is not used
        :type event:             Any
        """
        if not self._is_window_created('Tried to move window using arrow keys'):
            return
        x, y = self.current_location()
        if event.keysym == 'Up':
            self.move(x, y - 1)
        elif event.keysym == 'Down':
            self.move(x, y + 1)
        elif event.keysym == 'Left':
            self.move(x - 1, y)
        elif event.keysym == 'Right':
            self.move(x + 1, y)

    """
    def _config_callback(self, event):
        new_x = event.x
        new_y = event.y


        if self.not_completed_initial_movement:
            if self.starting_window_position != (new_x, new_y):
                return
            self.not_completed_initial_movement = False
            return

        if not self.saw_00:
            if new_x == 0 and new_y == 0:
                self.saw_00 = True

        # self.config_count += 1
        # if self.config_count < 40:
        #     return

        print('Move LOGIC')

        if self.config_last_size != (event.width, event.height):
            self.config_last_size = (event.width, event.height)

        if self.config_last_location[0] != new_x or self.config_last_location[1] != new_y:
            if self.config_last_location == (None, None):
                self.config_last_location = (new_x, new_y)
                return

        deltax = self.config_last_location[0] - event.x
        deltay = self.config_last_location[1] - event.y
        if deltax == 0 and deltay == 0:
            print('not moving so returning')
            return
        if Window._move_all_windows:
            print('checking all windows')
            for window in Window._active_windows:
                if window == self:
                    continue
                x = window.TKroot.winfo_x() + deltax
                y = window.TKroot.winfo_y() + deltay
                # window.TKroot.geometry("+%s+%s" % (x, y))  # this is what really moves the window
                # window.config_last_location = (x,y)
    """

    def _KeyboardCallback(self, event):
        """
        Window keyboard callback. Called by tkinter.  Will kick user out of the tkinter event loop. Should only be
        called if user has requested window level keyboard events

        :param event: object provided by tkinter that contains the key information
        :type event:  (event)
        """
        self.LastButtonClicked = None
        self.FormRemainedOpen = True
        if event.char != '':
            self.LastKeyboardEvent = event.char
        else:
            self.LastKeyboardEvent = str(event.keysym) + ':' + str(event.keycode)
        # if not self.NonBlocking:
        #     _BuildResults(self, False, self)
        _exit_mainloop(self)

    def _MouseWheelCallback(self, event):
        """
        Called by tkinter when a mouse wheel event has happened. Only called if keyboard events for the window
        have been enabled

        :param event: object sent in by tkinter that has the wheel direction
        :type event:  (event)
        """
        self.LastButtonClicked = None
        self.FormRemainedOpen = True
        self.LastKeyboardEvent = 'MouseWheel:Down' if event.delta < 0 or event.num == 5 else 'MouseWheel:Up'
        _exit_mainloop(self)

    def _Close(self, without_event=False):
        """
        The internal close call that does the real work of building. This method basically sets up for closing
        but doesn't destroy the window like the User's version of Close does

        :parm without_event: if True, then do not cause an event to be generated, "silently" close the window
        :type without_event: (bool)
        """

        try:
            self.TKroot.update()
        except:
            pass

        if not self.NonBlocking or not without_event:
            _BuildResults(self, False, self)
        if self.TKrootDestroyed:
            return
        self.TKrootDestroyed = True
        self.RootNeedsDestroying = True
        return

    def close(self):
        """
        Closes window.  Users can safely call even if window has been destroyed.   Should always call when done with
        a window so that resources are properly freed up within your thread.
        """

        try:
            del Window._active_windows[self]  # will only be in the list if window was explicitly finalized
        except:
            pass

        try:
            self.TKroot.update()  # On Linux must call update if the user closed with X or else won't actually close the window
        except:
            pass

        self._restore_stdout()
        self._restore_stderr()

        _TimerPeriodic.stop_all_timers_for_window(self)

        if self.TKrootDestroyed:
            return
        try:
            self.TKroot.destroy()
            self.TKroot.update()
            Window._DecrementOpenCount()
        except:
            pass
        self.TKrootDestroyed = True

        # Free up anything that was held in the layout and the root variables
        self.Rows = None
        self.TKroot = None

    def is_closed(self, quick_check=None):
        """
        Returns True is the window is maybe closed.  Can be difficult to tell sometimes
        NOTE - the call to TKroot.update was taking over 500 ms sometimes so added a flag to bypass the lengthy call.
        :param quick_quick: If True, then don't use the root.update call, only check the flags
        :type quick_check:  bool
        :return:            True if the window was closed or destroyed
        :rtype:             (bool)
        """

        if self.TKrootDestroyed or self.TKroot is None:
            return True

        # if performing a quick check only, then skip calling tkinter for performance reasons
        if quick_check is True:
            return False

        # see if can do an update... if not, then it's been destroyed
        try:
            self.TKroot.update()
        except:
            return True
        return False

    # IT FINALLY WORKED! 29-Oct-2018 was the first time this damned thing got called
    def _OnClosingCallback(self):
        """
        Internally used method ONLY. Not sure callable.  tkinter calls this when the window is closed by clicking X
        """
        if self.DisableClose:
            return
        if self.CurrentlyRunningMainloop:  # quit if this is the current mainloop, otherwise don't quit!
            _exit_mainloop(self)
            if self.close_destroys_window:
                self.TKroot.destroy()  # destroy this window
                self.TKrootDestroyed = True
                self.XFound = True
            else:
                self.LastButtonClicked = WINDOW_CLOSE_ATTEMPTED_EVENT
        elif Window._root_running_mainloop == Window.hidden_master_root:
            _exit_mainloop(self)
        else:
            if self.close_destroys_window:
                self.TKroot.destroy()  # destroy this window
                self.XFound = True
            else:
                self.LastButtonClicked = WINDOW_CLOSE_ATTEMPTED_EVENT
        if self.close_destroys_window:
            self.RootNeedsDestroying = True
        self._restore_stdout()
        self._restore_stderr()

    def disable(self):
        """
        Disables window from taking any input from the user
        """
        if not self._is_window_created('tried Window.disable'):
            return
        self.TKroot.attributes('-disabled', 1)
        # self.TKroot.grab_set_global()

    def enable(self):
        """
        Re-enables window to take user input after having it be Disabled previously
        """
        if not self._is_window_created('tried Window.enable'):
            return
        self.TKroot.attributes('-disabled', 0)
        # self.TKroot.grab_release()

    def hide(self):
        """
        Hides the window from the screen and the task bar
        """
        if not self._is_window_created('tried Window.hide'):
            return
        self._Hidden = True
        self.TKroot.withdraw()

    def un_hide(self):
        """
        Used to bring back a window that was previously hidden using the Hide method
        """
        if not self._is_window_created('tried Window.un_hide'):
            return
        if self._Hidden:
            self.TKroot.deiconify()
            self._Hidden = False

    def is_hidden(self):
        """
            Returns True if the window is currently hidden
        :return:    Returns True if the window is currently hidden
        :rtype:     bool
        """
        return self._Hidden

    def disappear(self):
        """
        Causes a window to "disappear" from the screen, but remain on the taskbar. It does this by turning the alpha
        channel to 0.  NOTE that on some platforms alpha is not supported. The window will remain showing on these
        platforms.  The Raspberry Pi for example does not have an alpha setting
        """
        if not self._is_window_created('tried Window.disappear'):
            return
        self.TKroot.attributes('-alpha', 0)

    def reappear(self):
        """
        Causes a window previously made to "Disappear" (using that method). Does this by restoring the alpha channel
        """
        if not self._is_window_created('tried Window.reappear'):
            return
        self.TKroot.attributes('-alpha', 255)

    def set_alpha(self, alpha):
        """
        Sets the Alpha Channel for a window.  Values are between 0 and 1 where 0 is completely transparent

        :param alpha: 0 to 1. 0 is completely transparent.  1 is completely visible and solid (can't see through)
        :type alpha:  (float)
        """
        if not self._is_window_created('tried Window.set_alpha'):
            return
        self._AlphaChannel = alpha
        self.TKroot.attributes('-alpha', alpha)

    @property
    def alpha_channel(self):
        """
        A property that changes the current alpha channel value (internal value)
        :return: the current alpha channel setting according to self, not read directly from tkinter
        :rtype:  (float)
        """
        return self._AlphaChannel

    @alpha_channel.setter
    def alpha_channel(self, alpha):
        """
        The setter method for this "property".
        Planning on depricating so that a Set call is always used by users. This is more in line with the SDK
        :param alpha: 0 to 1. 0 is completely transparent.  1 is completely visible and solid (can't see through)
        :type alpha:  (float)
        """
        if not self._is_window_created('tried Window.alpha_channel'):
            return
        self._AlphaChannel = alpha
        self.TKroot.attributes('-alpha', alpha)

    def bring_to_front(self):
        """
        Brings this window to the top of all other windows (perhaps may not be brought before a window made to "stay
        on top")
        """
        if not self._is_window_created('tried Window.bring_to_front'):
            return
        if running_windows():
            try:
                self.TKroot.wm_attributes('-topmost', 0)
                self.TKroot.wm_attributes('-topmost', 1)
                if not self.KeepOnTop:
                    self.TKroot.wm_attributes('-topmost', 0)
            except Exception as e:
                warnings.warn('Problem in Window.bring_to_front' + str(e), UserWarning)
        else:
            try:
                self.TKroot.lift()
            except:
                pass

    def send_to_back(self):
        """
        Pushes this window to the bottom of the stack of windows. It is the opposite of BringToFront
        """
        if not self._is_window_created('tried Window.send_to_back'):
            return
        try:
            self.TKroot.lower()
        except:
            pass

    def keep_on_top_set(self):
        """
        Sets keep_on_top after a window has been created.  Effect is the same
        as if the window was created with this set.  The Window is also brought
        to the front
        """
        if not self._is_window_created('tried Window.keep_on_top_set'):
            return
        self.KeepOnTop = True
        self.bring_to_front()
        try:
            self.TKroot.wm_attributes('-topmost', 1)
        except Exception as e:
            warnings.warn('Problem in Window.keep_on_top_set trying to set wm_attributes topmost' + str(e), UserWarning)

    def keep_on_top_clear(self):
        """
        Clears keep_on_top after a window has been created.  Effect is the same
        as if the window was created with this set.
        """
        if not self._is_window_created('tried Window.keep_on_top_clear'):
            return
        self.KeepOnTop = False
        try:
            self.TKroot.wm_attributes('-topmost', 0)
        except Exception as e:
            warnings.warn('Problem in Window.keep_on_top_clear trying to clear wm_attributes topmost' + str(e), UserWarning)

    def current_location(self, more_accurate=False, without_titlebar=False):
        """
        Get the current location of the window's top left corner.
        Sometimes, depending on the environment, the value returned does not include the titlebar,etc
        A new option, more_accurate, can be used to get the theoretical upper leftmost corner of the window.
        The titlebar and menubar are crated by the OS. It gets really confusing when running in a webpage (repl, trinket)
        Thus, the values can appear top be "off" due to the sometimes unpredictable way the location is calculated.
        If without_titlebar is set then the location of the root x,y is used which should not include the titlebar but
            may be OS dependent.

        :param more_accurate:    If True, will use the window's geometry to get the topmost location with titlebar, menubar taken into account
        :type more_accurate:     (bool)
        :param without_titlebar: If True, return location of top left of main window area without the titlebar (may be OS dependent?)
        :type without_titlebar:  (bool)
        :return:                 The x and y location in tuple form (x,y)
        :rtype:                  Tuple[(int | None), (int | None)]
        """

        if not self._is_window_created('tried Window.current_location'):
            return (None, None)
        try:
            if without_titlebar is True:
                x, y = self.TKroot.winfo_rootx(), self.TKroot.winfo_rooty()
            elif more_accurate:
                geometry = self.TKroot.geometry()
                location = geometry[geometry.find('+') + 1 :].split('+')
                x, y = int(location[0]), int(location[1])
            else:
                x, y = int(self.TKroot.winfo_x()), int(self.TKroot.winfo_y())
        except Exception as e:
            warnings.warn('Error in Window.current_location. Trouble getting x,y location\n' + str(e), UserWarning)
            x, y = (None, None)
        return (x, y)

    def current_size_accurate(self):
        """
        Get the current location of the window based on tkinter's geometry setting

        :return:              The x and y size in tuple form (x,y)
        :rtype:               Tuple[(int | None), (int | None)]
        """

        if not self._is_window_created('tried Window.current_location'):
            return (None, None)
        try:
            geometry = self.TKroot.geometry()
            geometry_tuple = geometry.split('+')
            window_size = geometry_tuple[0].split('x')
            x, y = int(window_size[0]), int(window_size[1])
        except Exception as e:
            warnings.warn(
                'Error in Window.current_size_accurate. Trouble getting x,y size\n{} {}'.format(geometry, geometry_tuple) + str(e),
                UserWarning,
            )
            x, y = (None, None)
        return (x, y)

    @property
    def size(self):
        """
        Return the current size of the window in pixels

        :return: (width, height) of the window
        :rtype:  Tuple[(int), (int)] or Tuple[None, None]
        """
        if not self._is_window_created('Tried to use Window.size property'):
            return (None, None)
        win_width = self.TKroot.winfo_width()
        win_height = self.TKroot.winfo_height()
        return win_width, win_height

    @size.setter
    def size(self, size):
        """
        Changes the size of the window, if possible

        :param size: (width, height) of the desired window size
        :type size:  (int, int)
        """
        try:
            self.TKroot.geometry('{}x{}'.format(size[0], size[1]))
            self.TKroot.update_idletasks()
        except:
            pass

    def set_size(self, size):
        """
        Changes the size of the window, if possible. You can also use the Window.size prooerty
        to set/get the size.

        :param size: (width, height) of the desired window size
        :type size:  (int, int)
        """
        if not self._is_window_created('Tried to change the size of the window prior to creation.'):
            return
        try:
            self.TKroot.geometry('{}x{}'.format(size[0], size[1]))
            self.TKroot.update_idletasks()
        except:
            pass

    def set_min_size(self, size):
        """
        Changes the minimum size of the window. Note Window must be read or finalized first.

        :param size: (width, height) tuple (int, int) of the desired window size in pixels
        :type size:  (int, int)
        """
        if not self._is_window_created('tried Window.set_min_size'):
            return
        self.TKroot.minsize(size[0], size[1])
        self.TKroot.update_idletasks()

    def set_resizable(self, x_axis_enable, y_axis_enable):
        """
        Changes if a window can be resized in either the X or the Y direction.
        Note Window must be read or finalized first.

        :param x_axis_enable: If True, the window can be changed in the X-axis direction. If False, it cannot
        :type x_axis_enable: (bool)
        :param y_axis_enable: If True, the window can be changed in the Y-axis direction. If False, it cannot
        :type y_axis_enable: (bool)
        """

        if not self._is_window_created('tried Window.set_resixable'):
            return
        try:
            self.TKroot.resizable(x_axis_enable, y_axis_enable)
        except Exception as e:
            _error_popup_with_traceback('Window.set_resizable - tkinter reported error', e)

    def visibility_changed(self):
        """
        When making an element in a column or someplace that has a scrollbar, then you'll want to call this function
        prior to the column's contents_changed() method.
        """
        self.refresh()

    def set_transparent_color(self, color):
        """
        Set the color that will be transparent in your window. Areas with this color will be SEE THROUGH.

        :param color: Color string that defines the transparent color
        :type color:  (str)
        """
        if not self._is_window_created('tried Window.set_transparent_color'):
            return
        try:
            self.TKroot.attributes('-transparentcolor', color)
            self.TransparentColor = color
        except:
            print('Transparent color not supported on this platform (windows only)')

    def mouse_location(self):
        """
        Return the (x,y) location of the mouse relative to the entire screen.  It's the same location that
        you would use to create a window, popup, etc.

        :return:    The location of the mouse pointer
        :rtype:     (int, int)
        """
        if not self._is_window_created('tried Window.mouse_location'):
            return (0, 0)

        return (self.TKroot.winfo_pointerx(), self.TKroot.winfo_pointery())

    def grab_any_where_on(self):
        """
        Turns on Grab Anywhere functionality AFTER a window has been created.  Don't try on a window that's not yet
        been Finalized or Read.
        """
        if not self._is_window_created('tried Window.grab_any_where_on'):
            return
        self.TKroot.bind('<ButtonPress-1>', self._StartMoveGrabAnywhere)
        self.TKroot.bind('<ButtonRelease-1>', self._StopMove)
        self.TKroot.bind('<B1-Motion>', self._OnMotionGrabAnywhere)

    def grab_any_where_off(self):
        """
        Turns off Grab Anywhere functionality AFTER a window has been created.  Don't try on a window that's not yet
        been Finalized or Read.
        """
        if not self._is_window_created('tried Window.grab_any_where_off'):
            return
        self.TKroot.unbind('<ButtonPress-1>')
        self.TKroot.unbind('<ButtonRelease-1>')
        self.TKroot.unbind('<B1-Motion>')

    def _user_bind_callback(self, bind_string, event, propagate=True):
        """
        Used when user binds a tkinter event directly to an element

        :param bind_string: The event that was bound so can lookup the key modifier
        :type bind_string:  (str)
        :param event:       Event data passed in by tkinter (not used)
        :type event:
        :param propagate:   If True then tkinter will be told to propagate the event
        :type propagate:    (bool)
        """
        # print('bind callback', bind_string, event)
        key = self.user_bind_dict.get(bind_string, '')
        self.user_bind_event = event
        if key is not None:
            self.LastButtonClicked = key
        else:
            self.LastButtonClicked = bind_string
        self.FormRemainedOpen = True
        _exit_mainloop(self)
        return 'break' if propagate is not True else None

    def bind(self, bind_string, key, propagate=True):
        """
        Used to add tkinter events to a Window.
        The tkinter specific data is in the Window's member variable user_bind_event
        :param bind_string: The string tkinter expected in its bind function
        :type bind_string:  (str)
        :param key:         The event that will be generated when the tkinter event occurs
        :type key:          str | int | tuple | object
        :param propagate:   If True then tkinter will be told to propagate the event
        :type propagate:    (bool)
        """
        if not self._is_window_created('tried Window.bind'):
            return
        try:
            self.TKroot.bind(bind_string, lambda evt: self._user_bind_callback(bind_string, evt, propagate))
        except Exception:
            self.TKroot.unbind_all(bind_string)
            return
            # _error_popup_with_traceback('Window.bind error', e)
        self.user_bind_dict[bind_string] = key

    def unbind(self, bind_string):
        """
        Used to remove tkinter events to a Window.
        This implementation removes ALL of the binds of the bind_string from the Window.  If there
        are multiple binds for the Window itself, they will all be removed.  This can be extended later if there
        is a need.
        :param bind_string: The string tkinter expected in its bind function
        :type bind_string:  (str)
        """
        if not self._is_window_created('tried Window.unbind'):
            return
        self.TKroot.unbind(bind_string)

    def _callback_main_debugger_window_create_keystroke(self, event):
        """
        Called when user presses the key that creates the main debugger window
        March 2022 - now causes the user reads to return timeout events automatically
        :param event: (event) not used. Passed in event info
        :type event:
        """
        Window._main_debug_window_build_needed = True
        # exit the event loop in a way that resembles a timeout occurring
        self.LastButtonClicked = self.TimeoutKey
        self.FormRemainedOpen = True
        self.TKroot.quit()  # kick the users out of the mainloop

    def _callback_popout_window_create_keystroke(self, event):
        """
        Called when user presses the key that creates the floating debugger window
        March 2022 - now causes the user reads to return timeout events automatically
        :param event: (event) not used. Passed in event info
        :type event:
        """
        Window._floating_debug_window_build_needed = True
        # exit the event loop in a way that resembles a timeout occurring
        self.LastButtonClicked = self.TimeoutKey
        self.FormRemainedOpen = True
        self.TKroot.quit()  # kick the users out of the mainloop

    def enable_debugger(self):
        """
        Enables the internal debugger. By default, the debugger IS enabled
        """
        if not self._is_window_created('tried Window.enable_debugger'):
            return
        self.TKroot.bind('<Cancel>', self._callback_main_debugger_window_create_keystroke)
        self.TKroot.bind('<Pause>', self._callback_popout_window_create_keystroke)
        self.DebuggerEnabled = True

    def disable_debugger(self):
        """
        Disable the internal debugger. By default the debugger is ENABLED
        """
        if not self._is_window_created('tried Window.disable_debugger'):
            return
        self.TKroot.unbind('<Cancel>')
        self.TKroot.unbind('<Pause>')
        self.DebuggerEnabled = False

    def set_title(self, title):
        """
        Change the title of the window

        :param title: The string to set the title to
        :type title:  (str)
        """
        if not self._is_window_created('tried Window.set_title'):
            return
        if self._has_custom_titlebar:
            try:  # just in case something goes badly, don't crash
                self.find_element(TITLEBAR_TEXT_KEY).update(title)
            except:
                pass
        # even with custom titlebar, set the main window's title too so it'll match when minimized
        self.TKroot.wm_title(str(title))

    def make_modal(self):
        """
        Makes a window into a "Modal Window"
        This means user will not be able to interact with other windows until this one is closed

        NOTE - Sorry Mac users - you can't have modal windows.... lobby your tkinter Mac devs
        """
        if not self._is_window_created('tried Window.make_modal'):
            return

        if running_mac() and FreeSimpleGUI.ENABLE_MAC_MODAL_DISABLE_PATCH:
            return

        # if modal windows have been disabled globally
        if not FreeSimpleGUI.DEFAULT_MODAL_WINDOWS_ENABLED and not FreeSimpleGUI.DEFAULT_MODAL_WINDOWS_FORCED:
            return

        try:
            self.TKroot.transient()
            self.TKroot.grab_set()
            self.TKroot.focus_force()
        except Exception as e:
            print('Exception trying to make modal', e)

    def force_focus(self):
        """
        Forces this window to take focus
        """
        if not self._is_window_created('tried Window.force_focus'):
            return
        self.TKroot.focus_force()

    def was_closed(self):
        """
        Returns True if the window was closed

        :return: True if the window is closed
        :rtype:  bool
        """
        return self.TKrootDestroyed

    def set_cursor(self, cursor):
        """
        Sets the cursor for the window.
        If you do not want any mouse pointer, then use the string "none"

        :param cursor: The tkinter cursor name
        :type cursor:  (str)
        """

        if not self._is_window_created('tried Window.set_cursor'):
            return
        try:
            self.TKroot.config(cursor=cursor)
        except Exception as e:
            print('Warning bad cursor specified ', cursor)
            print(e)

    def ding(self, display_number=0):
        """
        Make a "bell" sound. A capability provided by tkinter.  Your window needs to be finalized prior to calling.
        Ring a display's bell is the tkinter description of the call.
        :param display_number: Passed to tkinter's bell method as parameter "displayof".
        :type display_number:  int
        """
        if not self._is_window_created('tried Window.ding'):
            return
        try:
            self.TKroot.bell(display_number)
        except Exception as e:
            if not FreeSimpleGUI.SUPPRESS_ERROR_POPUPS:
                _error_popup_with_traceback('Window.ding() - tkinter reported error from bell() call', e)

    def _window_tkvar_changed_callback(self, *args):
        """
        Internal callback function for when the thread

        :param event: Information from tkinter about the callback
        :type event:

        """
        if self._queued_thread_event_available():
            self.FormRemainedOpen = True
            _exit_mainloop(self)

    def _create_thread_queue(self):
        """
        Creates the queue used by threads to communicate with this window
        """

        if self.thread_queue is None:
            self.thread_queue = queue.Queue()

        if self.thread_lock is None:
            self.thread_lock = threading.Lock()

        if self.thread_strvar is None:
            self.thread_strvar = tk.StringVar()
            if tk.TkVersion < 9:
                self.thread_strvar.trace('w', self._window_tkvar_changed_callback)
            else:
                self.thread_strvar.trace_add('write', self._window_tkvar_changed_callback)

    def write_event_value(self, key, value):
        """
        Adds a key & value tuple to the queue that is used by threads to communicate with the window

        :param key:   The key that will be returned as the event when reading the window
        :type key:    Any
        :param value: The value that will be in the values dictionary
        :type value:  Any
        """

        if self.thread_queue is None:
            print('*** Warning Window.write_event_value - no thread queue found ***')
            return
        # self.thread_lock.acquire()  # first lock the critical section
        self.thread_queue.put(item=(key, value))
        self.TKroot.tk.willdispatch()  # brilliant bit of code provided by Giuliano who I owe a million thank yous!
        self.thread_strvar.set('new item')

    def _queued_thread_event_read(self):
        if self.thread_queue is None:
            return None

        try:  # see if something has been posted to Queue
            message = self.thread_queue.get_nowait()
        except queue.Empty:  # get_nowait() will get exception when Queue is empty
            return None

        return message

    def _queued_thread_event_available(self):

        if self.thread_queue is None:
            return False
        # self.thread_lock.acquire()
        qsize = self.thread_queue.qsize()
        if qsize == 0:
            self.thread_timer = None
        # self.thread_lock.release()
        return qsize != 0

    def _RightClickMenuCallback(self, event):
        """
        When a right click menu is specified for an entire window, then this callback catches right clicks
        that happen to the window itself, when there are no elements that are in that area.

        The only portion that is not currently covered correctly is the row frame itself.  There will still
        be parts of the window, at the moment, that don't respond to a right click.  It's getting there, bit
        by bit.

        Callback function that's called when a right click happens. Shows right click menu as result.

        :param event: information provided by tkinter about the event including x,y location of click
        :type event:
        """
        # if there are widgets under the mouse, then see if it's the root only.  If not, then let the widget (element) show their menu instead
        x, y = self.TKroot.winfo_pointerxy()
        widget = self.TKroot.winfo_containing(x, y)
        if widget != self.TKroot:
            return
        self.TKRightClickMenu.tk_popup(event.x_root, event.y_root, 0)
        self.TKRightClickMenu.grab_release()

    def save_window_screenshot_to_disk(self, filename=None):
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
            # Get location of window to save
            pos = self.current_location()
            # Add a little to the X direction if window has a titlebar
            if not self.NoTitleBar:
                pos = (pos[0] + 7, pos[1])
            # Get size of wiondow
            size = self.current_size_accurate()
            # Get size of the titlebar
            titlebar_height = self.TKroot.winfo_rooty() - self.TKroot.winfo_y()
            # Add titlebar to size of window so that titlebar and window will be saved
            size = (size[0], size[1] + titlebar_height)
            if not self.NoTitleBar:
                size_adjustment = (2, 1)
            else:
                size_adjustment = (0, 0)
            # Make the "Bounding rectangle" used by PLK to do the screen grap "operation
            rect = (pos[0], pos[1], pos[0] + size[0] + size_adjustment[0], pos[1] + size[1] + size_adjustment[1])
            # Grab the image
            grab = ImageGrab.grab(bbox=rect)
            # Save the grabbed image to disk
        except Exception as e:
            # print(e)
            popup_error_with_traceback('Screen capture failure', 'Error happened while trying to save screencapture', e)

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

    def perform_long_operation(self, func, end_key=None):
        """
        Call your function that will take a long time to execute.  When it's complete, send an event
        specified by the end_key.

        Starts a thread on your behalf.

        This is a way for you to "ease into" threading without learning the details of threading.
        Your function will run, and when it returns 2 things will happen:
        1. The value you provide for end_key will be returned to you when you call window.read()
        2. If your function returns a value, then the value returned will also be included in your windows.read call in the values dictionary

        importANT - This method uses THREADS... this means you CANNOT make any FreeSimpleGUI calls from
        the function you provide with the exception of one function, Window.write_event_value.

        :param func:    A lambda or a function name with no parms
        :type func:     Any
        :param end_key: Optional key that will be generated when the function returns
        :type end_key:  (Any | None)
        :return:        The id of the thread
        :rtype:         threading.Thread
        """

        thread = threading.Thread(target=_long_func_thread, args=(self, end_key, func), daemon=True)
        thread.start()
        return thread

    @property
    def key_dict(self):
        """
        Returns a dictionary with all keys and their corresponding elements
        { key : Element }
        :return: Dictionary of keys and elements
        :rtype:  Dict[Any, Element]
        """
        return self.AllKeysDict

    def key_is_good(self, key):
        """
        Checks to see if this is a good key for this window
        If there's an element with the key provided, then True is returned
        :param key:     The key to check
        :type key:      str | int | tuple | object
        :return:        True if key is an element in this window
        :rtype:         bool
        """
        if key in self.key_dict:
            return True
        return False

    def get_scaling(self):
        """
        Returns the current scaling value set for this window

        :return:    Scaling according to tkinter. Returns FreeSimpleGUI.DEFAULT_SCALING if error
        :rtype:     float
        """

        if not self._is_window_created('Tried Window.set_scaling'):
            return FreeSimpleGUI.DEFAULT_SCALING
        try:
            scaling = self.TKroot.tk.call('tk', 'scaling')
        except Exception as e:
            if not FreeSimpleGUI.SUPPRESS_ERROR_POPUPS:
                _error_popup_with_traceback('Window.get_scaling() - tkinter reported error', e)
            scaling = FreeSimpleGUI.DEFAULT_SCALING

        return scaling

    def _custom_titlebar_restore_callback(self, event):
        self._custom_titlebar_restore()

    def _custom_titlebar_restore(self):
        if running_linux():
            self.TKroot.unbind('<Button-1>')
            self.TKroot.deiconify()

            # self.ParentForm.TKroot.wm_overrideredirect(True)
            self.TKroot.wm_attributes('-type', 'dock')

        else:
            self.TKroot.unbind('<Expose>')
            self.TKroot.wm_overrideredirect(True)
        if self.TKroot.state() == 'iconic':
            self.TKroot.deiconify()
        else:
            if not running_linux():
                self.TKroot.state('normal')
            else:
                self.TKroot.attributes('-fullscreen', False)
        self.maximized = False

    def _custom_titlebar_minimize(self):
        if running_linux():
            self.TKroot.wm_attributes('-type', 'normal')
            self.TKroot.wm_overrideredirect(False)
            self.TKroot.iconify()
            self.TKroot.bind('<Button-1>', self._custom_titlebar_restore_callback)
        else:
            self.TKroot.wm_overrideredirect(False)
            self.TKroot.iconify()
            self.TKroot.bind('<Expose>', self._custom_titlebar_restore_callback)

    def _custom_titlebar_callback(self, key):
        """
        One of the Custom Titlbar buttons was clicked
        :param key:
        :return:
        """
        if key == TITLEBAR_MINIMIZE_KEY:
            if not self.DisableMinimize:
                self._custom_titlebar_minimize()
        elif key == TITLEBAR_MAXIMIZE_KEY:
            if self.Resizable:
                if self.maximized:
                    self.normal()
                else:
                    self.maximize()
        elif key == TITLEBAR_CLOSE_KEY:
            if not self.DisableClose:
                self._OnClosingCallback()

    def timer_start(self, frequency_ms, key=EVENT_TIMER, repeating=True):
        """
        Starts a timer that gnerates Timer Events.  The default is to repeat the timer events until timer is stopped.
        You can provide your own key or a default key will be used.  The default key is defined
        with the constants EVENT_TIMER or TIMER_KEY.  They both equal the same value.
        The values dictionary will contain the timer ID that is returned from this function.

        :param frequency_ms:    How often to generate timer events in milliseconds
        :type frequency_ms:     int
        :param key:             Key to be returned as the timer event
        :type key:              str | int | tuple | object
        :param repeating:       If True then repeat timer events until timer is explicitly stopped
        :type repeating:        bool
        :return:                Timer ID for the timer
        :rtype:                 int
        """
        timer = _TimerPeriodic(self, frequency_ms=frequency_ms, key=key, repeating=repeating)
        return timer.id

    def timer_stop(self, timer_id):
        """
        Stops a timer with a given ID

        :param timer_id:        Timer ID of timer to stop
        :type timer_id:         int
        :return:
        """
        _TimerPeriodic.stop_timer_with_id(timer_id)

    def timer_stop_all(self):
        """
        Stops all timers for THIS window
        """
        _TimerPeriodic.stop_all_timers_for_window(self)

    def timer_get_active_timers(self):
        """
        Returns a list of currently active timers for a window
        :return:    List of timers for the window
        :rtype:     List[int]
        """
        return _TimerPeriodic.get_all_timers_for_window(self)

    @classmethod
    def _restore_stdout(cls):
        for item in cls._rerouted_stdout_stack:
            (window, element) = item  # type: (Window, Element)
            if not window.is_closed():
                sys.stdout = element
                break
        cls._rerouted_stdout_stack = [item for item in cls._rerouted_stdout_stack if not item[0].is_closed()]
        if len(cls._rerouted_stdout_stack) == 0 and cls._original_stdout is not None:
            sys.stdout = cls._original_stdout
        # print('Restored stdout... new stack:',  [item[0].Title for item in cls._rerouted_stdout_stack ])

    @classmethod
    def _restore_stderr(cls):
        for item in cls._rerouted_stderr_stack:
            (window, element) = item  # type: (Window, Element)
            if not window.is_closed():
                sys.stderr = element
                break
        cls._rerouted_stderr_stack = [item for item in cls._rerouted_stderr_stack if not item[0].is_closed()]
        if len(cls._rerouted_stderr_stack) == 0 and cls._original_stderr is not None:
            sys.stderr = cls._original_stderr

    def __getitem__(self, key):
        """
        Returns Element that matches the passed in key.
        This is "called" by writing code as thus:
        window['element key'].update

        :param key: The key to find
        :type key:  str | int | tuple | object
        :return:    The element found
        :rtype:     Element | Input | Combo | OptionMenu | Listbox | Radio | Checkbox | Spin | Multiline | Text | StatusBar | FreeSimpleGUI.elements.multiline.Output | Button | ButtonMenu | ProgressBar | Image | FreeSimpleGUI.elements.canvas.Canvas | Graph | Frame | VerticalSeparator | HorizontalSeparator | FreeSimpleGUI.elements.tab.Tab | FreeSimpleGUI.elements.tab.TabGroup | Slider | Column | FreeSimpleGUI.elements.pane.Pane | Menu | FreeSimpleGUI.elements.table.Table | FreeSimpleGUI.elements.tree.Tree | FreeSimpleGUI.elements.error.ErrorElement | None
        """

        return self.find_element(key)

    def __call__(self, *args, **kwargs):
        """
        Call window.read but without having to type it out.
        window() == window.read()
        window(timeout=50) == window.read(timeout=50)

        :return: The famous event, values that read returns.
        :rtype:  Tuple[Any, Dict[Any, Any]]
        """
        return self.read(*args, **kwargs)

    def _is_window_created(self, additional_message=''):
        msg = str(additional_message)
        if self.TKroot is None:
            warnings.warn(
                'You cannot perform operations on a Window until it is read or finalized. Adding a "finalize=True" parameter to your Window creation will fix this. ' + msg,
                UserWarning,
            )
            if not FreeSimpleGUI.SUPPRESS_ERROR_POPUPS:
                _error_popup_with_traceback(
                    'You cannot perform operations on a Window until it is read or finalized.',
                    'Adding a "finalize=True" parameter to your Window creation will likely fix this',
                    msg,
                )
            return False
        return True

    def _has_custom_titlebar_element(self):
        for elem in self.AllKeysDict.values():
            if elem.Key in (TITLEBAR_MAXIMIZE_KEY, TITLEBAR_CLOSE_KEY, TITLEBAR_IMAGE_KEY):
                return True
            if elem.metadata == TITLEBAR_METADATA_MARKER:
                return True
        return False

    AddRow = add_row
    AddRows = add_rows
    AlphaChannel = alpha_channel
    BringToFront = bring_to_front
    Close = close
    CurrentLocation = current_location
    Disable = disable
    DisableDebugger = disable_debugger
    Disappear = disappear
    Enable = enable
    EnableDebugger = enable_debugger
    Fill = fill
    Finalize = finalize
    # FindElement = find_element
    FindElementWithFocus = find_element_with_focus
    GetScreenDimensions = get_screen_dimensions
    GrabAnyWhereOff = grab_any_where_off
    GrabAnyWhereOn = grab_any_where_on
    Hide = hide
    Layout = layout
    LoadFromDisk = load_from_disk
    Maximize = maximize
    Minimize = minimize
    Move = move
    Normal = normal
    Read = read
    Reappear = reappear
    Refresh = refresh
    SaveToDisk = save_to_disk
    SendToBack = send_to_back
    SetAlpha = set_alpha
    SetIcon = set_icon
    SetTransparentColor = set_transparent_color
    Size = size
    UnHide = un_hide
    VisibilityChanged = visibility_changed
    CloseNonBlocking = close
    CloseNonBlockingForm = close
    start_thread = perform_long_operation


from FreeSimpleGUI.elements.column import Column
from FreeSimpleGUI.elements.error import ErrorElement
from FreeSimpleGUI.elements.column import TkScrollableFrame
