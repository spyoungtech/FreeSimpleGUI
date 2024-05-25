from __future__ import annotations

import copy
import tkinter as tk
import warnings
from tkinter import ttk

import FreeSimpleGUI
from FreeSimpleGUI import BROWSE_FILES_DELIMITER
from FreeSimpleGUI import BUTTON_DISABLED_MEANS_IGNORE
from FreeSimpleGUI import BUTTON_TYPE_BROWSE_FILE
from FreeSimpleGUI import BUTTON_TYPE_BROWSE_FILES
from FreeSimpleGUI import BUTTON_TYPE_BROWSE_FOLDER
from FreeSimpleGUI import BUTTON_TYPE_CALENDAR_CHOOSER
from FreeSimpleGUI import BUTTON_TYPE_CLOSES_WIN
from FreeSimpleGUI import BUTTON_TYPE_CLOSES_WIN_ONLY
from FreeSimpleGUI import BUTTON_TYPE_COLOR_CHOOSER
from FreeSimpleGUI import BUTTON_TYPE_READ_FORM
from FreeSimpleGUI import BUTTON_TYPE_SAVEAS_FILE
from FreeSimpleGUI import COLOR_SYSTEM_DEFAULT
from FreeSimpleGUI import ELEM_TYPE_BUTTON
from FreeSimpleGUI import ELEM_TYPE_BUTTONMENU
from FreeSimpleGUI import FILE_TYPES_ALL_FILES
from FreeSimpleGUI import MENU_SHORTCUT_CHARACTER
from FreeSimpleGUI import running_mac
from FreeSimpleGUI import theme_background_color
from FreeSimpleGUI import theme_button_color
from FreeSimpleGUI import theme_input_background_color
from FreeSimpleGUI import theme_input_text_color
from FreeSimpleGUI import ThisRow
from FreeSimpleGUI.elements.base import Element
from FreeSimpleGUI.elements.helpers import AddMenuItem
from FreeSimpleGUI.elements.helpers import button_color_to_tuple


class Button(Element):
    """
    Button Element - Defines all possible buttons. The shortcuts such as Submit, FileBrowse, ... each create a Button
    """

    def __init__(
        self,
        button_text='',
        button_type=BUTTON_TYPE_READ_FORM,
        target=(None, None),
        tooltip=None,
        file_types=FILE_TYPES_ALL_FILES,
        initial_folder=None,
        default_extension='',
        disabled=False,
        change_submits=False,
        enable_events=False,
        image_filename=None,
        image_data=None,
        image_size=(None, None),
        image_subsample=None,
        image_zoom=None,
        image_source=None,
        border_width=None,
        size=(None, None),
        s=(None, None),
        auto_size_button=None,
        button_color=None,
        disabled_button_color=None,
        highlight_colors=None,
        mouseover_colors=(None, None),
        use_ttk_buttons=None,
        font=None,
        bind_return_key=False,
        focus=False,
        pad=None,
        p=None,
        key=None,
        k=None,
        right_click_menu=None,
        expand_x=False,
        expand_y=False,
        visible=True,
        metadata=None,
    ):
        """
        :param button_text:           Text to be displayed on the button
        :type button_text:            (str)
        :param button_type:           You  should NOT be setting this directly. ONLY the shortcut functions set this
        :type button_type:            (int)
        :param target:                key or (row,col) target for the button. Note that -1 for column means 1 element to the left of this one. The constant ThisRow is used to indicate the current row. The Button itself is a valid target for some types of button
        :type target:                 str | (int, int)
        :param tooltip:               text, that will appear when mouse hovers over the element
        :type tooltip:                (str)
        :param file_types:            the filetypes that will be used to match files. To indicate all files: (("ALL Files", "*.* *"),).
        :type file_types:             Tuple[(str, str), ...]
        :param initial_folder:        starting path for folders and files
        :type initial_folder:         (str)
        :param default_extension:     If no extension entered by user, add this to filename (only used in saveas dialogs)
        :type default_extension:      (str)
        :param disabled:              If True button will be created disabled. If BUTTON_DISABLED_MEANS_IGNORE then the button will be ignored rather than disabled using tkinter
        :type disabled:               (bool | str)
        :param change_submits:        DO NOT USE. Only listed for backwards compat - Use enable_events instead
        :type change_submits:         (bool)
        :param enable_events:         Turns on the element specific events. If this button is a target, should it generate an event when filled in
        :type enable_events:          (bool)
        :param image_source:          Image to place on button. Use INSTEAD of the image_filename and image_data. Unifies these into 1 easier to use parm
        :type image_source:           (str | bytes)
        :param image_filename:        image filename if there is a button image. GIFs and PNGs only.
        :type image_filename:         (str)
        :param image_data:            Raw or Base64 representation of the image to put on button. Choose either filename or data
        :type image_data:             bytes | str
        :param image_size:            Size of the image in pixels (width, height)
        :type image_size:             (int, int)
        :param image_subsample:       amount to reduce the size of the image. Divides the size by this number. 2=1/2, 3=1/3, 4=1/4, etc
        :type image_subsample:        (int)
        :param image_zoom:            amount to increase the size of the image. 2=twice size, 3=3 times, etc
        :type image_zoom:             (int)
        :param border_width:          width of border around button in pixels
        :type border_width:           (int)
        :param size:                  (w, h) w=characters-wide, h=rows-high. If an int instead of a tuple is supplied, then height is auto-set to 1
        :type size:                   (int | None, int | None)  | (None, None) | int
        :param s:                     Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                      (int | None, int | None)  | (None, None) | int
        :param auto_size_button:      if True the button size is sized to fit the text
        :type auto_size_button:       (bool)
        :param button_color:          Color of button. default is from theme or the window. Easy to remember which is which if you say "ON" between colors. "red" on "green". Normally a tuple, but can be a simplified-button-color-string "foreground on background". Can be a single color if want to set only the background.
        :type button_color:           (str, str) | str
        :param disabled_button_color: colors to use when button is disabled (text, background). Use None for a color if don't want to change. Only ttk buttons support both text and background colors. tk buttons only support changing text color
        :type disabled_button_color:  (str, str) | str
        :param highlight_colors:      colors to use when button has focus (has focus, does not have focus). None will use colors based on theme. Only used by Linux and only for non-TTK button
        :type highlight_colors:       (str, str)
        :param mouseover_colors:      Important difference between Linux & Windows! Linux - Colors when mouse moved over button.  Windows - colors when button is pressed. The default is to switch the text and background colors (an inverse effect)
        :type mouseover_colors:       (str, str) | str
        :param use_ttk_buttons:       True = use ttk buttons. False = do not use ttk buttons.  None (Default) = use ttk buttons only if on a Mac and not with button images
        :type use_ttk_buttons:        (bool)
        :param font:                  specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:                   (str or (str, int[, str]) or None)
        :param bind_return_key:       If True then pressing the return key in an Input or Multiline Element will cause this button to appear to be clicked (generates event with this button's key
        :type bind_return_key:        (bool)
        :param focus:                 if True, initial focus will be put on this button
        :type focus:                  (bool)
        :param pad:                   Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:                    (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                     Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                      (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param key:                   Used with window.find_element and with return values to uniquely identify this element to uniquely identify this element
        :type key:                    str | int | tuple | object
        :param k:                     Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                      str | int | tuple | object
        :param right_click_menu:      A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type right_click_menu:       List[List[ List[str] | str ]]
        :param expand_x:              If True the element will automatically expand in the X direction to fill available space
        :type expand_x:               (bool)
        :param expand_y:              If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:               (bool)
        :param visible:               set visibility state of the element
        :type visible:                (bool)
        :param metadata:              User metadata that can be set to ANYTHING
        :type metadata:               (Any)
        """

        self.AutoSizeButton = auto_size_button
        self.BType = button_type
        if file_types is not None and len(file_types) == 2 and isinstance(file_types[0], str) and isinstance(file_types[1], str):
            warnings.warn(
                'file_types parameter not correctly specified. This parameter is a LIST of TUPLES. You have passed (str,str) rather than ((str, str),). Fixing it for you this time.\nchanging {} to {}\nPlease correct your code'.format(file_types, ((file_types[0], file_types[1]),)),
                UserWarning,
            )
            file_types = ((file_types[0], file_types[1]),)
        self.FileTypes = file_types
        self.Widget = self.TKButton = None  # type: tk.Button
        self.Target = target
        self.ButtonText = str(button_text)
        self.RightClickMenu = right_click_menu
        # Button colors can be a tuple (text, background) or a string with format "text on background"
        self.ButtonColor = button_color_to_tuple(button_color)

        self.DisabledButtonColor = button_color_to_tuple(disabled_button_color) if disabled_button_color is not None else (None, None)
        if image_source is not None:
            if isinstance(image_source, bytes):
                image_data = image_source
            elif isinstance(image_source, str):
                image_filename = image_source
        self.ImageFilename = image_filename
        self.ImageData = image_data
        self.ImageSize = image_size
        self.ImageSubsample = image_subsample
        self.zoom = int(image_zoom) if image_zoom is not None else None
        self.UserData = None
        self.BorderWidth = border_width if border_width is not None else FreeSimpleGUI.DEFAULT_BORDER_WIDTH
        self.BindReturnKey = bind_return_key
        self.Focus = focus
        self.TKCal = None
        self.calendar_default_date_M_D_Y = (None, None, None)
        self.calendar_close_when_chosen = False
        self.calendar_locale = None
        self.calendar_format = None
        self.calendar_location = (None, None)
        self.calendar_no_titlebar = True
        self.calendar_begin_at_sunday_plus = 0
        self.calendar_month_names = None
        self.calendar_day_abbreviations = None
        self.calendar_title = ''
        self.calendar_selection = ''
        self.default_button = None
        self.InitialFolder = initial_folder
        self.DefaultExtension = default_extension
        self.Disabled = disabled
        self.ChangeSubmits = change_submits or enable_events
        self.UseTtkButtons = use_ttk_buttons
        self._files_delimiter = BROWSE_FILES_DELIMITER  # used by the file browse button. used when multiple files are selected by user
        if use_ttk_buttons is None and running_mac():
            self.UseTtkButtons = True

        if key is None and k is None:
            _key = self.ButtonText
            if FreeSimpleGUI.DEFAULT_USE_BUTTON_SHORTCUTS is True:
                pos = _key.find(MENU_SHORTCUT_CHARACTER)
                if pos != -1:
                    if pos < len(MENU_SHORTCUT_CHARACTER) or _key[pos - len(MENU_SHORTCUT_CHARACTER)] != '\\':
                        _key = _key[:pos] + _key[pos + len(MENU_SHORTCUT_CHARACTER) :]
                    else:
                        _key = _key.replace('\\' + MENU_SHORTCUT_CHARACTER, MENU_SHORTCUT_CHARACTER)
        else:
            _key = key if key is not None else k
        if highlight_colors is not None:
            self.HighlightColors = highlight_colors
        else:
            self.HighlightColors = self._compute_highlight_colors()

        if mouseover_colors != (None, None):
            self.MouseOverColors = button_color_to_tuple(mouseover_colors)
        elif button_color is not None:
            self.MouseOverColors = (self.ButtonColor[1], self.ButtonColor[0])
        else:
            self.MouseOverColors = (theme_button_color()[1], theme_button_color()[0])
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y

        sz = size if size != (None, None) else s
        super().__init__(ELEM_TYPE_BUTTON, size=sz, font=font, pad=pad, key=_key, tooltip=tooltip, visible=visible, metadata=metadata)
        return

    def _compute_highlight_colors(self):
        """
        Determines the color to use to indicate the button has focus. This setting is only used by Linux.
        :return: Pair of colors. (Highlight, Highlight Background)
        :rtype:  (str, str)
        """
        highlight_color = highlight_background = COLOR_SYSTEM_DEFAULT
        if self.ButtonColor != COLOR_SYSTEM_DEFAULT and theme_background_color() != COLOR_SYSTEM_DEFAULT:
            highlight_background = theme_background_color()
        if self.ButtonColor != COLOR_SYSTEM_DEFAULT and self.ButtonColor[0] != COLOR_SYSTEM_DEFAULT:
            if self.ButtonColor[0] != theme_background_color():
                highlight_color = self.ButtonColor[0]
            else:
                highlight_color = 'red'
        return (highlight_color, highlight_background)

        # Realtime button release callback

    def ButtonReleaseCallBack(self, parm):
        """
        Not a user callable function.  Called by tkinter when a "realtime" button is released

        :param parm: the event info from tkinter
        :type parm:

        """
        self.LastButtonClickedWasRealtime = False
        self.ParentForm.LastButtonClicked = None

    # Realtime button callback
    def ButtonPressCallBack(self, parm):
        """
        Not a user callable method. Callback called by tkinter when a "realtime" button is pressed

        :param parm: Event info passed in by tkinter
        :type parm:

        """
        self.ParentForm.LastButtonClickedWasRealtime = True
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = self.ButtonText
        _exit_mainloop(self.ParentForm)

    def _find_target(self):
        target = self.Target
        target_element = None

        if target[0] == ThisRow:
            target = [self.Position[0], target[1]]
            if target[1] < 0:
                target[1] = self.Position[1] + target[1]
        strvar = None
        should_submit_window = False
        if target == (None, None):
            strvar = self.TKStringVar
        else:
            # Need a try-block because if the target is not hashable, the "in" test will raise exception
            try:
                if target in self.ParentForm.AllKeysDict:
                    target_element = self.ParentForm.AllKeysDict[target]
            except:
                pass
            # if target not found or the above try got exception, then keep looking....
            if target_element is None:
                if not isinstance(target, str):
                    if target[0] < 0:
                        target = [self.Position[0] + target[0], target[1]]
                    target_element = self.ParentContainer._GetElementAtLocation(target)
                else:
                    target_element = self.ParentForm.find_element(target)
            try:
                strvar = target_element.TKStringVar
            except:
                pass
            try:
                if target_element.ChangeSubmits:
                    should_submit_window = True
            except:
                pass
        return target_element, strvar, should_submit_window

    # -------  Button Callback  ------- #
    def ButtonCallBack(self):
        """
        Not user callable! Called by tkinter when a button is clicked.  This is where all the fun begins!
        """

        if self.Disabled == BUTTON_DISABLED_MEANS_IGNORE:
            return
        target_element, strvar, should_submit_window = self._find_target()

        filetypes = FILE_TYPES_ALL_FILES if self.FileTypes is None else self.FileTypes

        if self.BType == BUTTON_TYPE_BROWSE_FOLDER:
            if running_mac():  # macs don't like seeing the parent window (go firgure)
                folder_name = tk.filedialog.askdirectory(initialdir=self.InitialFolder)  # show the 'get folder' dialog box
            else:
                folder_name = tk.filedialog.askdirectory(initialdir=self.InitialFolder, parent=self.ParentForm.TKroot)  # show the 'get folder' dialog box
            if folder_name:
                try:
                    strvar.set(folder_name)
                    self.TKStringVar.set(folder_name)
                except:
                    pass
            else:  # if "cancel" button clicked, don't generate an event
                should_submit_window = False
        elif self.BType == BUTTON_TYPE_BROWSE_FILE:
            if running_mac():
                # Workaround for the "*.*" issue on Mac
                is_all = [(x, y) for (x, y) in filetypes if all(ch in '* .' for ch in y)]
                if not len(set(filetypes)) > 1 and (len(is_all) != 0 or filetypes == FILE_TYPES_ALL_FILES):
                    file_name = tk.filedialog.askopenfilename(initialdir=self.InitialFolder)
                else:
                    file_name = tk.filedialog.askopenfilename(initialdir=self.InitialFolder, filetypes=filetypes)  # show the 'get file' dialog box
            else:
                file_name = tk.filedialog.askopenfilename(filetypes=filetypes, initialdir=self.InitialFolder, parent=self.ParentForm.TKroot)  # show the 'get file' dialog box

            if file_name:
                strvar.set(file_name)
                self.TKStringVar.set(file_name)
            else:  # if "cancel" button clicked, don't generate an event
                should_submit_window = False
        elif self.BType == BUTTON_TYPE_COLOR_CHOOSER:
            color = tk.colorchooser.askcolor(parent=self.ParentForm.TKroot, color=self.default_color)  # show the 'get file' dialog box
            color = color[1]  # save only the #RRGGBB portion
            if color is not None:
                strvar.set(color)
                self.TKStringVar.set(color)
        elif self.BType == BUTTON_TYPE_BROWSE_FILES:
            if running_mac():
                # Workaround for the "*.*" issue on Mac
                is_all = [(x, y) for (x, y) in filetypes if all(ch in '* .' for ch in y)]
                if not len(set(filetypes)) > 1 and (len(is_all) != 0 or filetypes == FILE_TYPES_ALL_FILES):
                    file_name = tk.filedialog.askopenfilenames(initialdir=self.InitialFolder)
                else:
                    file_name = tk.filedialog.askopenfilenames(filetypes=filetypes, initialdir=self.InitialFolder)
            else:
                file_name = tk.filedialog.askopenfilenames(filetypes=filetypes, initialdir=self.InitialFolder, parent=self.ParentForm.TKroot)

            if file_name:
                file_name = self._files_delimiter.join(file_name)  # normally a ';'
                strvar.set(file_name)
                self.TKStringVar.set(file_name)
            else:  # if "cancel" button clicked, don't generate an event
                should_submit_window = False
        elif self.BType == BUTTON_TYPE_SAVEAS_FILE:
            # show the 'get file' dialog box
            if running_mac():
                # Workaround for the "*.*" issue on Mac
                is_all = [(x, y) for (x, y) in filetypes if all(ch in '* .' for ch in y)]
                if not len(set(filetypes)) > 1 and (len(is_all) != 0 or filetypes == FILE_TYPES_ALL_FILES):
                    file_name = tk.filedialog.asksaveasfilename(defaultextension=self.DefaultExtension, initialdir=self.InitialFolder)
                else:
                    file_name = tk.filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=self.DefaultExtension, initialdir=self.InitialFolder)
            else:
                file_name = tk.filedialog.asksaveasfilename(
                    filetypes=filetypes,
                    defaultextension=self.DefaultExtension,
                    initialdir=self.InitialFolder,
                    parent=self.ParentForm.TKroot,
                )

            if file_name:
                strvar.set(file_name)
                self.TKStringVar.set(file_name)
            else:  # if "cancel" button clicked, don't generate an event
                should_submit_window = False
        elif self.BType == BUTTON_TYPE_CLOSES_WIN:  # this is a return type button so GET RESULTS and destroy window
            # first, get the results table built
            # modify the Results table in the parent FlexForm object
            if self.Key is not None:
                self.ParentForm.LastButtonClicked = self.Key
            else:
                self.ParentForm.LastButtonClicked = self.ButtonText
            self.ParentForm.FormRemainedOpen = False
            self.ParentForm._Close()
            _exit_mainloop(self.ParentForm)

            if self.ParentForm.NonBlocking:
                self.ParentForm.TKroot.destroy()
                Window._DecrementOpenCount()
        elif self.BType == BUTTON_TYPE_READ_FORM:  # LEAVE THE WINDOW OPEN!! DO NOT CLOSE
            # This is a PLAIN BUTTON
            # first, get the results table built
            # modify the Results table in the parent FlexForm object
            if self.Key is not None:
                self.ParentForm.LastButtonClicked = self.Key
            else:
                self.ParentForm.LastButtonClicked = self.ButtonText
            self.ParentForm.FormRemainedOpen = True
            _exit_mainloop(self.ParentForm)
        elif self.BType == BUTTON_TYPE_CLOSES_WIN_ONLY:  # special kind of button that does not exit main loop
            self.ParentForm._Close(without_event=True)
            self.ParentForm.TKroot.destroy()  # close the window with tkinter
            Window._DecrementOpenCount()
        elif self.BType == BUTTON_TYPE_CALENDAR_CHOOSER:  # this is a return type button so GET RESULTS and destroy window
            # ------------ new chooser code -------------
            self.ParentForm.LastButtonClicked = self.Key  # key should have been generated already if not set by user
            self.ParentForm.FormRemainedOpen = True
            should_submit_window = False
            _exit_mainloop(self.ParentForm)
        # elif self.BType == BUTTON_TYPE_SHOW_DEBUGGER:
        # **** DEPRICATED *****
        # if self.ParentForm.DebuggerEnabled:
        # show_debugger_popout_window()

        if should_submit_window:
            self.ParentForm.LastButtonClicked = target_element.Key
            self.ParentForm.FormRemainedOpen = True
            _exit_mainloop(self.ParentForm)

        return

    def update(
        self,
        text=None,
        button_color=(None, None),
        disabled=None,
        image_source=None,
        image_data=None,
        image_filename=None,
        visible=None,
        image_subsample=None,
        image_zoom=None,
        disabled_button_color=(None, None),
        image_size=None,
    ):
        """
        Changes some of the settings for the Button Element. Must call `Window.Read` or `Window.Finalize` prior

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param text:                  sets button text
        :type text:                   (str)
        :param button_color:          Color of button. default is from theme or the window. Easy to remember which is which if you say "ON" between colors. "red" on "green". Normally a tuple, but can be a simplified-button-color-string "foreground on background". Can be a single color if want to set only the background.
        :type button_color:           (str, str) | str
        :param disabled:              True/False to enable/disable at the GUI level. Use BUTTON_DISABLED_MEANS_IGNORE to ignore clicks (won't change colors)
        :type disabled:               (bool | str)
        :param image_source:          Image to place on button. Use INSTEAD of the image_filename and image_data. Unifies these into 1 easier to use parm
        :type image_source:           (str | bytes)
        :param image_data:            Raw or Base64 representation of the image to put on button. Choose either filename or data
        :type image_data:             bytes | str
        :param image_filename:        image filename if there is a button image. GIFs and PNGs only.
        :type image_filename:         (str)
        :param disabled_button_color: colors to use when button is disabled (text, background). Use None for a color if don't want to change. Only ttk buttons support both text and background colors. tk buttons only support changing text color
        :type disabled_button_color:  (str, str)
        :param visible:               control visibility of element
        :type visible:                (bool)
        :param image_subsample:       amount to reduce the size of the image. Divides the size by this number. 2=1/2, 3=1/3, 4=1/4, etc
        :type image_subsample:        (int)
        :param image_zoom:            amount to increase the size of the image. 2=twice size, 3=3 times, etc
        :type image_zoom:             (int)
        :param image_size:            Size of the image in pixels (width, height)
        :type image_size:             (int, int)
        """

        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Button.update - The window was closed')
            return

        if image_source is not None:
            if isinstance(image_source, bytes):
                image_data = image_source
            elif isinstance(image_source, str):
                image_filename = image_source

        if self.UseTtkButtons:
            style_name = self.ttk_style_name  # created when made initial window (in the pack)
            # style_name = str(self.Key) + 'custombutton.TButton'
            button_style = ttk.Style()
        if text is not None:
            btext = text
            if FreeSimpleGUI.DEFAULT_USE_BUTTON_SHORTCUTS is True:
                pos = btext.find(MENU_SHORTCUT_CHARACTER)
                if pos != -1:
                    if pos < len(MENU_SHORTCUT_CHARACTER) or btext[pos - len(MENU_SHORTCUT_CHARACTER)] != '\\':
                        btext = btext[:pos] + btext[pos + len(MENU_SHORTCUT_CHARACTER) :]
                    else:
                        btext = btext.replace('\\' + MENU_SHORTCUT_CHARACTER, MENU_SHORTCUT_CHARACTER)
                        pos = -1
                if pos != -1:
                    self.TKButton.config(underline=pos)
            self.TKButton.configure(text=btext)
            self.ButtonText = text
        if button_color != (None, None) and button_color != COLOR_SYSTEM_DEFAULT:
            bc = button_color_to_tuple(button_color, self.ButtonColor)
            if self.UseTtkButtons:
                if bc[0] not in (None, COLOR_SYSTEM_DEFAULT):
                    button_style.configure(style_name, foreground=bc[0])
                if bc[1] not in (None, COLOR_SYSTEM_DEFAULT):
                    button_style.configure(style_name, background=bc[1])
            else:
                if bc[0] not in (None, COLOR_SYSTEM_DEFAULT):
                    self.TKButton.config(foreground=bc[0], activebackground=bc[0])
                if bc[1] not in (None, COLOR_SYSTEM_DEFAULT):
                    self.TKButton.config(background=bc[1], activeforeground=bc[1])
            self.ButtonColor = bc
        if disabled is True:
            self.TKButton['state'] = 'disabled'
        elif disabled is False:
            self.TKButton['state'] = 'normal'
        elif disabled == BUTTON_DISABLED_MEANS_IGNORE:
            self.TKButton['state'] = 'normal'
        self.Disabled = disabled if disabled is not None else self.Disabled

        if image_data is not None:
            image = tk.PhotoImage(data=image_data)
            if image_subsample:
                image = image.subsample(image_subsample)
            if image_zoom is not None:
                image = image.zoom(int(image_zoom))
            if image_size is not None:
                width, height = image_size
            else:
                width, height = image.width(), image.height()
            if self.UseTtkButtons:
                button_style.configure(style_name, image=image, width=width, height=height)
            else:
                self.TKButton.config(image=image, width=width, height=height)
            self.TKButton.image = image
        if image_filename is not None:
            image = tk.PhotoImage(file=image_filename)
            if image_subsample:
                image = image.subsample(image_subsample)
            if image_zoom is not None:
                image = image.zoom(int(image_zoom))
            if image_size is not None:
                width, height = image_size
            else:
                width, height = image.width(), image.height()
            if self.UseTtkButtons:
                button_style.configure(style_name, image=image, width=width, height=height)
            else:
                self.TKButton.config(highlightthickness=0, image=image, width=width, height=height)
            self.TKButton.image = image
        if visible is False:
            self._pack_forget_save_settings()
        elif visible is True:
            self._pack_restore_settings()
        if disabled_button_color != (None, None) and disabled_button_color != COLOR_SYSTEM_DEFAULT:
            if not self.UseTtkButtons:
                self.TKButton['disabledforeground'] = disabled_button_color[0]
            else:
                if disabled_button_color[0] is not None:
                    button_style.map(style_name, foreground=[('disabled', disabled_button_color[0])])
                if disabled_button_color[1] is not None:
                    button_style.map(style_name, background=[('disabled', disabled_button_color[1])])
            self.DisabledButtonColor = (
                disabled_button_color[0] if disabled_button_color[0] is not None else self.DisabledButtonColor[0],
                disabled_button_color[1] if disabled_button_color[1] is not None else self.DisabledButtonColor[1],
            )

        if visible is not None:
            self._visible = visible

    def get_text(self):
        """
        Returns the current text shown on a button

        :return: The text currently displayed on the button
        :rtype:  (str)
        """
        return self.ButtonText

    def click(self):
        """
        Generates a click of the button as if the user clicked the button
        Calls the tkinter invoke method for the button
        """
        try:
            self.TKButton.invoke()
        except:
            print('Exception clicking button')

    Click = click
    GetText = get_text
    Update = update


class ButtonMenu(Element):
    """
    The Button Menu Element.  Creates a button that when clicked will show a menu similar to right click menu
    """

    def __init__(
        self,
        button_text,
        menu_def,
        tooltip=None,
        disabled=False,
        image_source=None,
        image_filename=None,
        image_data=None,
        image_size=(None, None),
        image_subsample=None,
        image_zoom=None,
        border_width=None,
        size=(None, None),
        s=(None, None),
        auto_size_button=None,
        button_color=None,
        text_color=None,
        background_color=None,
        disabled_text_color=None,
        font=None,
        item_font=None,
        pad=None,
        p=None,
        expand_x=False,
        expand_y=False,
        key=None,
        k=None,
        tearoff=False,
        visible=True,
        metadata=None,
    ):
        """
        :param button_text:               Text to be displayed on the button
        :type button_text:                (str)
        :param menu_def:                  A list of lists of Menu items to show when this element is clicked. See docs for format as they are the same for all menu types
        :type menu_def:                   List[List[str]]
        :param tooltip:                   text, that will appear when mouse hovers over the element
        :type tooltip:                    (str)
        :param disabled:                  If True button will be created disabled
        :type disabled:                   (bool)
        :param image_source:              Image to place on button. Use INSTEAD of the image_filename and image_data. Unifies these into 1 easier to use parm
        :type image_source:               (str | bytes)
        :param image_filename:            image filename if there is a button image. GIFs and PNGs only.
        :type image_filename:             (str)
        :param image_data:                Raw or Base64 representation of the image to put on button. Choose either filename or data
        :type image_data:                 bytes | str
        :param image_size:                Size of the image in pixels (width, height)
        :type image_size:                 (int, int)
        :param image_subsample:           amount to reduce the size of the image. Divides the size by this number. 2=1/2, 3=1/3, 4=1/4, etc
        :type image_subsample:            (int)
        :param image_zoom:                amount to increase the size of the image. 2=twice size, 3=3 times, etc
        :type image_zoom:                 (int)
        :param border_width:              width of border around button in pixels
        :type border_width:               (int)
        :param size:                      (w, h) w=characters-wide, h=rows-high. If an int instead of a tuple is supplied, then height is auto-set to 1
        :type size:                       (int, int)  | (None, None) | int
        :param s:                         Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                          (int, int)  | (None, None) | int
        :param auto_size_button:          if True the button size is sized to fit the text
        :type auto_size_button:           (bool)
        :param button_color:              of button. Easy to remember which is which if you say "ON" between colors. "red" on "green"
        :type button_color:               (str, str) | str
        :param background_color:          color of the background
        :type background_color:           (str)
        :param text_color:                element's text color. Can be in #RRGGBB format or a color name "black"
        :type text_color:                 (str)
        :param disabled_text_color:       color to use for text when item is disabled. Can be in #RRGGBB format or a color name "black"
        :type disabled_text_color:        (str)
        :param font:                      specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:                       (str or (str, int[, str]) or None)
        :param item_font:                 specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike, for the menu items
        :type item_font:                  (str or (str, int[, str]) or None)
        :param pad:                       Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:                        (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                         Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                          (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param expand_x:                  If True the element will automatically expand in the X direction to fill available space
        :type expand_x:                   (bool)
        :param expand_y:                  If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:                   (bool)
        :param key:                       Used with window.find_element and with return values to uniquely identify this element to uniquely identify this element
        :type key:                        str | int | tuple | object
        :param k:                         Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                          str | int | tuple | object
        :param tearoff:                   Determines if menus should allow them to be torn off
        :type tearoff:                    (bool)
        :param visible:                   set visibility state of the element
        :type visible:                    (bool)
        :param metadata:                  User metadata that can be set to ANYTHING
        :type metadata:                   (Any)
        """

        self.MenuDefinition = copy.deepcopy(menu_def)

        self.AutoSizeButton = auto_size_button
        self.ButtonText = button_text
        self.ButtonColor = button_color_to_tuple(button_color)
        self.BackgroundColor = background_color if background_color is not None else theme_input_background_color()
        self.TextColor = text_color if text_color is not None else theme_input_text_color()
        self.DisabledTextColor = disabled_text_color if disabled_text_color is not None else COLOR_SYSTEM_DEFAULT
        self.ItemFont = item_font
        self.BorderWidth = border_width if border_width is not None else FreeSimpleGUI.DEFAULT_BORDER_WIDTH
        if image_source is not None:
            if isinstance(image_source, str):
                image_filename = image_source
            elif isinstance(image_source, bytes):
                image_data = image_source
            else:
                warnings.warn(f'ButtonMenu element - image_source is not a valid type: {type(image_source)}', UserWarning)

        self.ImageFilename = image_filename
        self.ImageData = image_data
        self.ImageSize = image_size
        self.ImageSubsample = image_subsample
        self.zoom = int(image_zoom) if image_zoom is not None else None
        self.Disabled = disabled
        self.IsButtonMenu = True
        self.MenuItemChosen = None
        self.Widget = self.TKButtonMenu = None  # type: tk.Menubutton
        self.TKMenu = None  # type: tk.Menu
        self.part_of_custom_menubar = False
        self.custom_menubar_key = None
        # self.temp_size = size if size != (NONE, NONE) else
        key = key if key is not None else k
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y

        super().__init__(
            ELEM_TYPE_BUTTONMENU,
            size=sz,
            font=font,
            pad=pad,
            key=key,
            tooltip=tooltip,
            text_color=self.TextColor,
            background_color=self.BackgroundColor,
            visible=visible,
            metadata=metadata,
        )
        self.Tearoff = tearoff

    def _MenuItemChosenCallback(self, item_chosen):  # ButtonMenu Menu Item Chosen Callback
        """
        Not a user callable function.  Called by tkinter when an item is chosen from the menu.

        :param item_chosen: The menu item chosen.
        :type item_chosen:  (str)
        """
        # print('IN MENU ITEM CALLBACK', item_chosen)
        self.MenuItemChosen = item_chosen
        self.ParentForm.LastButtonClicked = self.Key
        self.ParentForm.FormRemainedOpen = True
        _exit_mainloop(self.ParentForm)

    def update(
        self,
        menu_definition=None,
        visible=None,
        image_source=None,
        image_size=(None, None),
        image_subsample=None,
        image_zoom=None,
        button_text=None,
        button_color=None,
    ):
        """
        Changes some of the settings for the ButtonMenu Element. Must call `Window.Read` or `Window.Finalize` prior

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param menu_definition: (New menu definition (in menu definition format)
        :type menu_definition:  List[List]
        :param visible:         control visibility of element
        :type visible:          (bool)
        :param image_source:    new image if image is to be changed. Can be a filename or a base64 encoded byte-string
        :type image_source:     (str | bytes)
        :param image_size:      Size of the image in pixels (width, height)
        :type image_size:       (int, int)
        :param image_subsample: amount to reduce the size of the image. Divides the size by this number. 2=1/2, 3=1/3, 4=1/4, etc
        :type image_subsample:  (int)
        :param image_zoom:      amount to increase the size of the image. 2=twice size, 3=3 times, etc
        :type image_zoom:       (int)
        :param button_text:     Text to be shown on the button
        :type button_text:      (str)
        :param button_color:    Normally a tuple, but can be a simplified-button-color-string "foreground on background". Can be a single color if want to set only the background.
        :type button_color:     (str, str) | str
        """

        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in ButtonMenu.update - The window was closed')
            return

        if menu_definition is not None:
            self.MenuDefinition = copy.deepcopy(menu_definition)
            top_menu = self.TKMenu = tk.Menu(self.TKButtonMenu, tearoff=self.Tearoff, font=self.ItemFont, tearoffcommand=self._tearoff_menu_callback)

            if self.BackgroundColor not in (COLOR_SYSTEM_DEFAULT, None):
                top_menu.config(bg=self.BackgroundColor)
            if self.TextColor not in (COLOR_SYSTEM_DEFAULT, None):
                top_menu.config(fg=self.TextColor)
            if self.DisabledTextColor not in (COLOR_SYSTEM_DEFAULT, None):
                top_menu.config(disabledforeground=self.DisabledTextColor)
            if self.ItemFont is not None:
                top_menu.config(font=self.ItemFont)
            AddMenuItem(self.TKMenu, self.MenuDefinition[1], self)
            self.TKButtonMenu.configure(menu=self.TKMenu)
        if image_source is not None:
            filename = data = None
            if image_source is not None:
                if isinstance(image_source, bytes):
                    data = image_source
                elif isinstance(image_source, str):
                    filename = image_source
                else:
                    warnings.warn(
                        f'ButtonMenu element - image_source is not a valid type: {type(image_source)}',
                        UserWarning,
                    )
            image = None
            if filename is not None:
                image = tk.PhotoImage(file=filename)
                if image_subsample is not None:
                    image = image.subsample(image_subsample)
                if image_zoom is not None:
                    image = image.zoom(int(image_zoom))
            elif data is not None:
                # if type(data) is bytes:
                try:
                    image = tk.PhotoImage(data=data)
                    if image_subsample is not None:
                        image = image.subsample(image_subsample)
                    if image_zoom is not None:
                        image = image.zoom(int(image_zoom))
                except Exception:
                    image = data

            if image is not None:
                if type(image) is not bytes:
                    width, height = (
                        image_size[0] if image_size[0] is not None else image.width(),
                        image_size[1] if image_size[1] is not None else image.height(),
                    )
                else:
                    width, height = image_size

                self.TKButtonMenu.config(image=image, compound=tk.CENTER, width=width, height=height)
                self.TKButtonMenu.image = image
        if button_text is not None:
            self.TKButtonMenu.configure(text=button_text)
            self.ButtonText = button_text
        if visible is False:
            self._pack_forget_save_settings()
        elif visible is True:
            self._pack_restore_settings()
        if visible is not None:
            self._visible = visible
        if button_color != (None, None) and button_color != COLOR_SYSTEM_DEFAULT:
            bc = button_color_to_tuple(button_color, self.ButtonColor)
            if bc[0] not in (None, COLOR_SYSTEM_DEFAULT):
                self.TKButtonMenu.config(foreground=bc[0], activeforeground=bc[0])
            if bc[1] not in (None, COLOR_SYSTEM_DEFAULT):
                self.TKButtonMenu.config(background=bc[1], activebackground=bc[1])
            self.ButtonColor = bc

    def click(self):
        """
        Generates a click of the button as if the user clicked the button
        Calls the tkinter invoke method for the button
        """
        try:
            self.TKMenu.invoke(1)
        except:
            print('Exception clicking button')

    Update = update
    Click = click


from FreeSimpleGUI._utils import _error_popup_with_traceback, _exit_mainloop
from FreeSimpleGUI.window import Window
