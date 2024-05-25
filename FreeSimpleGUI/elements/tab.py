from __future__ import annotations

import tkinter as tk
import warnings
from tkinter import ttk

import FreeSimpleGUI
from FreeSimpleGUI import _add_right_click_menu
from FreeSimpleGUI import _random_error_emoji
from FreeSimpleGUI import COLOR_SYSTEM_DEFAULT
from FreeSimpleGUI import ELEM_TYPE_TAB
from FreeSimpleGUI import ELEM_TYPE_TAB_GROUP
from FreeSimpleGUI import Element
from FreeSimpleGUI import LOOK_AND_FEEL_TABLE
from FreeSimpleGUI import PackFormIntoFrame
from FreeSimpleGUI import popup_error
from FreeSimpleGUI import popup_error_with_traceback
from FreeSimpleGUI import ToolTip
from FreeSimpleGUI._utils import _error_popup_with_traceback
from FreeSimpleGUI.window import Window


class Tab(Element):
    """
    Tab Element is another "Container" element that holds a layout and displays a tab with text. Used with TabGroup only
    Tabs are never placed directly into a layout.  They are always "Contained" in a TabGroup layout
    """

    def __init__(
        self,
        title,
        layout,
        title_color=None,
        background_color=None,
        font=None,
        pad=None,
        p=None,
        disabled=False,
        border_width=None,
        key=None,
        k=None,
        tooltip=None,
        right_click_menu=None,
        expand_x=False,
        expand_y=False,
        visible=True,
        element_justification='left',
        image_source=None,
        image_subsample=None,
        image_zoom=None,
        metadata=None,
    ):
        """
        :param title:                 text to show on the tab
        :type title:                  (str)
        :param layout:                The element layout that will be shown in the tab
        :type layout:                 List[List[Element]]
        :param title_color:           color of the tab text (note not currently working on tkinter)
        :type title_color:            (str)
        :param background_color:      color of background of the entire layout
        :type background_color:       (str)
        :param font:                  NOT USED in the tkinter port
        :type font:                   (str or (str, int[, str]) or None)
        :param pad:                   Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:                    (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                     Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                      (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param disabled:              If True button will be created disabled
        :type disabled:               (bool)
        :param border_width:          NOT USED in tkinter port
        :type border_width:           (int)
        :param key:                   Value that uniquely identifies this element from all other elements. Used when Finding an element or in return values. Must be unique to the window
        :type key:                    str | int | tuple | object
        :param k:                     Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                      str | int | tuple | object
        :param tooltip:               text, that will appear when mouse hovers over the element
        :type tooltip:                (str)
        :param right_click_menu:      A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type right_click_menu:       List[List[ List[str] | str ]]
        :param expand_x:              If True the element will automatically expand in the X direction to fill available space
        :type expand_x:               (bool)
        :param expand_y:              If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:               (bool)
        :param visible:               set visibility state of the element
        :type visible:                (bool)
        :param element_justification: All elements inside the Tab will have this justification 'left', 'right', 'center' are valid values
        :type element_justification:  (str)
        :param image_source:          A filename or a base64 bytes of an image to place on the Tab
        :type image_source:            str | bytes | None
        :param image_subsample:       amount to reduce the size of the image. Divides the size by this number. 2=1/2, 3=1/3, 4=1/4, etc
        :type image_subsample:        (int)
        :param image_zoom:            amount to increase the size of the image. 2=twice size, 3=3 times, etc
        :type image_zoom:             (int)
        :param metadata:              User metadata that can be set to ANYTHING
        :type metadata:               (Any)
        """

        filename = data = None
        if image_source is not None:
            if isinstance(image_source, bytes):
                data = image_source
            elif isinstance(image_source, str):
                filename = image_source
            else:
                warnings.warn(f'Image element - source is not a valid type: {type(image_source)}', UserWarning)

        self.Filename = filename
        self.Data = data
        self.ImageSubsample = image_subsample
        self.zoom = int(image_zoom) if image_zoom is not None else None
        self.UseDictionary = False
        self.ReturnValues = None
        self.ReturnValuesList = []
        self.ReturnValuesDictionary = {}
        self.DictionaryKeyCounter = 0
        self.ParentWindow = None
        self.Rows = []
        self.TKFrame = None
        self.Widget = None  # type: tk.Frame
        self.Title = title
        self.BorderWidth = border_width
        self.Disabled = disabled
        self.ParentNotebook = None
        self.TabID = None
        self.BackgroundColor = background_color if background_color is not None else FreeSimpleGUI.DEFAULT_BACKGROUND_COLOR
        self.RightClickMenu = right_click_menu
        self.ContainerElemementNumber = Window._GetAContainerNumber()
        self.ElementJustification = element_justification
        key = key if key is not None else k
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y

        self.Layout(layout)

        super().__init__(
            ELEM_TYPE_TAB,
            background_color=background_color,
            text_color=title_color,
            font=font,
            pad=pad,
            key=key,
            tooltip=tooltip,
            visible=visible,
            metadata=metadata,
        )
        return

    def add_row(self, *args):
        """
        Not recommended use call.  Used to add rows of Elements to the Frame Element.

        :param *args: The list of elements for this row
        :type *args:  List[Element]
        """
        NumRows = len(self.Rows)  # number of existing rows is our row number
        CurrentRowNumber = NumRows  # this row's number
        CurrentRow = []  # start with a blank row and build up
        # -------------------------  Add the elements to a row  ------------------------- #
        for i, element in enumerate(args):  # Loop through list of elements and add them to the row
            if type(element) is list:
                popup_error_with_traceback(
                    'Error creating Tab layout',
                    'Layout has a LIST instead of an ELEMENT',
                    'This sometimes means you have a badly placed ]',
                    'The offensive list is:',
                    element,
                    'This list will be stripped from your layout',
                )
                continue
            elif callable(element) and not isinstance(element, Element):
                popup_error_with_traceback(
                    'Error creating Tab layout',
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
                popup_error_with_traceback(
                    'Error creating Tab layout',
                    'The layout specified has already been used',
                    'You MUST start witha "clean", unused layout every time you create a window',
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
            if element.Key is not None:
                self.UseDictionary = True
        # -------------------------  Append the row to list of Rows  ------------------------- #
        self.Rows.append(CurrentRow)

    def layout(self, rows):
        """
        Not user callable.  Use layout parameter instead. Creates the layout using the supplied rows of Elements

        :param rows: List[List[Element]] The list of rows
        :type rows:  List[List[Element]]
        :return:     (Tab) used for chaining
        :rtype:
        """

        for row in rows:
            try:
                iter(row)
            except TypeError:
                popup_error(
                    'Error creating Tab layout',
                    'Your row is not an iterable (e.g. a list)',
                    f'Instead of a list, the type found was {type(row)}',
                    'The offensive row = ',
                    row,
                    'This item will be stripped from your layout',
                    keep_on_top=True,
                    image=_random_error_emoji(),
                )
                continue
            self.AddRow(*row)
        return self

    def update(self, title=None, disabled=None, visible=None):
        """
        Changes some of the settings for the Tab Element. Must call `Window.Read` or `Window.Finalize` prior

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param title:    tab title
        :type title:     (str)
        :param disabled: disable or enable state of the element
        :type disabled:  (bool)
        :param visible:  control visibility of element
        :type visible:   (bool)
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Tab.update - The window was closed')
            return

        state = 'normal'
        if disabled is not None:
            self.Disabled = disabled
            if disabled:
                state = 'disabled'
        if visible is False:
            state = 'hidden'
        if visible is not None:
            self._visible = visible

        self.ParentNotebook.tab(self.TabID, state=state)

        if title is not None:
            self.Title = str(title)
            self.ParentNotebook.tab(self.TabID, text=self.Title)
        return self

    def _GetElementAtLocation(self, location):
        """
        Not user callable. Used to find the Element at a row, col position within the layout

        :param location: (row, column) position of the element to find in layout
        :type location:  (int, int)
        :return:         The element found at the location
        :rtype:          (Element)
        """

        (row_num, col_num) = location
        row = self.Rows[row_num]
        element = row[col_num]
        return element

    def select(self):
        """
        Create a tkinter event that mimics user clicking on a tab. Must have called window.Finalize / Read first!

        """
        # Use a try in case the window has been destoyed
        try:
            self.ParentNotebook.select(self.TabID)
        except Exception as e:
            print(f'Exception Selecting Tab {e}')

    AddRow = add_row
    Layout = layout
    Select = select
    Update = update


class TabGroup(Element):
    """
    TabGroup Element groups together your tabs into the group of tabs you see displayed in your window
    """

    def __init__(
        self,
        layout,
        tab_location=None,
        title_color=None,
        tab_background_color=None,
        selected_title_color=None,
        selected_background_color=None,
        background_color=None,
        focus_color=None,
        font=None,
        change_submits=False,
        enable_events=False,
        pad=None,
        p=None,
        border_width=None,
        tab_border_width=None,
        theme=None,
        key=None,
        k=None,
        size=(None, None),
        s=(None, None),
        tooltip=None,
        right_click_menu=None,
        expand_x=False,
        expand_y=False,
        visible=True,
        metadata=None,
    ):
        """
        :param layout:                    Layout of Tabs. Different than normal layouts. ALL Tabs should be on first row
        :type layout:                     List[List[Tab]]
        :param tab_location:              location that tabs will be displayed. Choices are left, right, top, bottom, lefttop, leftbottom, righttop, rightbottom, bottomleft, bottomright, topleft, topright
        :type tab_location:               (str)
        :param title_color:               color of text on tabs
        :type title_color:                (str)
        :param tab_background_color:      color of all tabs that are not selected
        :type tab_background_color:       (str)
        :param selected_title_color:      color of tab text when it is selected
        :type selected_title_color:       (str)
        :param selected_background_color: color of tab when it is selected
        :type selected_background_color:  (str)
        :param background_color:          color of background area that tabs are located on
        :type background_color:           (str)
        :param focus_color:               color of focus indicator on the tabs
        :type focus_color:                (str)
        :param font:                      specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:                       (str or (str, int[, str]) or None)
        :param change_submits:            * DEPRICATED DO NOT USE. Use `enable_events` instead
        :type change_submits:             (bool)
        :param enable_events:             If True then switching tabs will generate an Event
        :type enable_events:              (bool)
        :param pad:                       Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:                        (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                         Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                          (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param border_width:              width of border around element in pixels
        :type border_width:               (int)
        :param tab_border_width:          width of border around the tabs
        :type tab_border_width:           (int)
        :param theme:                     DEPRICATED - You can only specify themes using set options or when window is created. It's not possible to do it on an element basis
        :type theme:                      (enum)
        :param key:                       Value that uniquely identifies this element from all other elements. Used when Finding an element or in return values. Must be unique to the window
        :type key:                        str | int | tuple | object
        :param k:                         Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                          str | int | tuple | object
        :param size:                      (width, height) w=pixels-wide, h=pixels-high. Either item in tuple can be None to indicate use the computed value and set only 1 direction
        :type size:                       (int|None, int|None)
        :param s:                         Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                          (int|None, int|None)
        :param tooltip:                   text, that will appear when mouse hovers over the element
        :type tooltip:                    (str)
        :param right_click_menu:          A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type right_click_menu:           List[List[ List[str] | str ]]
        :param expand_x:                  If True the element will automatically expand in the X direction to fill available space
        :type expand_x:                   (bool)
        :param expand_y:                  If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:                   (bool)
        :param visible:                   DEPRECATED  - Should you need to control visiblity for the TabGroup as a whole, place it into a Column element
        :type visible:                    (bool)
        :param metadata:                  User metadata that can be set to ANYTHING
        :type metadata:                   (Any)
        """

        self.UseDictionary = False
        self.ReturnValues = None
        self.ReturnValuesList = []
        self.ReturnValuesDictionary = {}
        self.DictionaryKeyCounter = 0
        self.ParentWindow = None
        self.SelectedTitleColor = selected_title_color if selected_title_color is not None else LOOK_AND_FEEL_TABLE[FreeSimpleGUI.CURRENT_LOOK_AND_FEEL]['TEXT']
        self.SelectedBackgroundColor = selected_background_color if selected_background_color is not None else LOOK_AND_FEEL_TABLE[FreeSimpleGUI.CURRENT_LOOK_AND_FEEL]['BACKGROUND']
        title_color = title_color if title_color is not None else LOOK_AND_FEEL_TABLE[FreeSimpleGUI.CURRENT_LOOK_AND_FEEL]['TEXT_INPUT']
        self.TabBackgroundColor = tab_background_color if tab_background_color is not None else LOOK_AND_FEEL_TABLE[FreeSimpleGUI.CURRENT_LOOK_AND_FEEL]['INPUT']
        self.Rows = []
        self.TKNotebook = None  # type: ttk.Notebook
        self.Widget = None  # type: ttk.Notebook
        self.tab_index_to_key = {}  # has a list of the tabs in the notebook and their associated key
        self.TabCount = 0
        self.BorderWidth = border_width
        self.BackgroundColor = background_color if background_color is not None else FreeSimpleGUI.DEFAULT_BACKGROUND_COLOR
        self.ChangeSubmits = change_submits or enable_events
        self.TabLocation = tab_location
        self.ElementJustification = 'left'
        self.RightClickMenu = right_click_menu
        self.TabBorderWidth = tab_border_width
        self.FocusColor = focus_color

        key = key if key is not None else k
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y

        self.Layout(layout)

        super().__init__(
            ELEM_TYPE_TAB_GROUP,
            size=sz,
            background_color=background_color,
            text_color=title_color,
            font=font,
            pad=pad,
            key=key,
            tooltip=tooltip,
            visible=visible,
            metadata=metadata,
        )
        return

    def add_row(self, *args):
        """
        Not recommended user call.  Used to add rows of Elements to the Frame Element.

        :param *args:     The list of elements for this row
        :type *args:      List[Element]
        """

        NumRows = len(self.Rows)  # number of existing rows is our row number
        CurrentRowNumber = NumRows  # this row's number
        CurrentRow = []  # start with a blank row and build up
        # -------------------------  Add the elements to a row  ------------------------- #
        for i, element in enumerate(args):  # Loop through list of elements and add them to the row
            if type(element) is list:
                popup_error(
                    'Error creating Tab layout',
                    'Layout has a LIST instead of an ELEMENT',
                    'This sometimes means you have a badly placed ]',
                    'The offensive list is:',
                    element,
                    'This list will be stripped from your layout',
                    keep_on_top=True,
                    image=_random_error_emoji(),
                )
                continue
            elif callable(element) and not isinstance(element, Element):
                popup_error(
                    'Error creating Tab layout',
                    'Layout has a FUNCTION instead of an ELEMENT',
                    'This likely means you are missing () from your layout',
                    'The offensive list is:',
                    element,
                    'This item will be stripped from your layout',
                    keep_on_top=True,
                    image=_random_error_emoji(),
                )
                continue
            if element.ParentContainer is not None:
                warnings.warn(
                    '*** YOU ARE ATTEMPTING TO REUSE AN ELEMENT IN YOUR LAYOUT! Once placed in a layout, an element cannot be used in another layout. ***',
                    UserWarning,
                )
                popup_error(
                    'Error creating Tab layout',
                    'The layout specified has already been used',
                    'You MUST start witha "clean", unused layout every time you create a window',
                    'The offensive Element = ',
                    element,
                    'and has a key = ',
                    element.Key,
                    'This item will be stripped from your layout',
                    'Hint - try printing your layout and matching the IDs "print(layout)"',
                    keep_on_top=True,
                    image=_random_error_emoji(),
                )
                continue
            element.Position = (CurrentRowNumber, i)
            element.ParentContainer = self
            CurrentRow.append(element)
            if element.Key is not None:
                self.UseDictionary = True
        # -------------------------  Append the row to list of Rows  ------------------------- #
        self.Rows.append(CurrentRow)

    def layout(self, rows):
        """
        Can use like the Window.Layout method, but it's better to use the layout parameter when creating

        :param rows: The rows of Elements
        :type rows:  List[List[Element]]
        :return:     Used for chaining
        :rtype:      (Frame)
        """
        for row in rows:
            try:
                iter(row)
            except TypeError:
                popup_error(
                    'Error creating Tab layout',
                    'Your row is not an iterable (e.g. a list)',
                    f'Instead of a list, the type found was {type(row)}',
                    'The offensive row = ',
                    row,
                    'This item will be stripped from your layout',
                    keep_on_top=True,
                    image=_random_error_emoji(),
                )
                continue
            self.AddRow(*row)
        return self

    def _GetElementAtLocation(self, location):
        """
        Not user callable. Used to find the Element at a row, col position within the layout

        :param location: (row, column) position of the element to find in layout
        :type location:  (int, int)
        :return:         The element found at the location
        :rtype:          (Element)
        """

        (row_num, col_num) = location
        row = self.Rows[row_num]
        element = row[col_num]
        return element

    def find_key_from_tab_name(self, tab_name):
        """
        Searches through the layout to find the key that matches the text on the tab. Implies names should be unique

        :param tab_name: name of a tab
        :type tab_name:  str
        :return:         Returns the key or None if no key found
        :rtype:          key | None
        """
        for row in self.Rows:
            for element in row:
                if element.Title == tab_name:
                    return element.Key
        return None

    def find_currently_active_tab_key(self):
        """
        Returns the key for the currently active tab in this TabGroup
        :return:    Returns the key or None of no key found
        :rtype:     key | None
        """
        try:
            current_index = self.TKNotebook.index('current')
            key = self.tab_index_to_key.get(current_index, None)
        except:
            key = None

        return key

    def get(self):
        """
        Returns the current value for the Tab Group, which will be the currently selected tab's KEY or the text on
        the tab if no key is defined.  Returns None if an error occurs.
        Note that this is exactly the same data that would be returned from a call to Window.read. Are you sure you
        are using this method correctly?

        :return: The key of the currently selected tab or None if there is an error
        :rtype:  Any | None
        """

        try:
            current_index = self.TKNotebook.index('current')
            key = self.tab_index_to_key.get(current_index, None)
        except:
            key = None

        return key

    def add_tab(self, tab_element):
        """
        Add a new tab to an existing TabGroup
        This call was written so that tabs can be added at runtime as your user performs operations.
        Your Window should already be created and finalized.

        :param tab_element: A Tab Element that has a layout in it
        :type tab_element:  Tab
        """

        self.add_row(tab_element)
        tab_element.TKFrame = tab_element.Widget = tk.Frame(self.TKNotebook)
        form = self.ParentForm
        form._BuildKeyDictForWindow(form, tab_element, form.AllKeysDict)
        form.AllKeysDict[tab_element.Key] = tab_element
        # Pack the tab's layout into the tab. NOTE - This does NOT pack the Tab itself... for that see below...
        PackFormIntoFrame(tab_element, tab_element.TKFrame, self.ParentForm)

        # - This is below -    Perform the same operation that is performed when a Tab is packed into the window.
        # If there's an image in the tab, then do the imagey-stuff
        # ------------------- start of imagey-stuff -------------------
        try:
            if tab_element.Filename is not None:
                photo = tk.PhotoImage(file=tab_element.Filename)
            elif tab_element.Data is not None:
                photo = tk.PhotoImage(data=tab_element.Data)
            else:
                photo = None

            if tab_element.ImageSubsample and photo is not None:
                photo = photo.subsample(tab_element.ImageSubsample)
                # print('*ERROR laying out form.... Image Element has no image specified*')
        except Exception as e:
            photo = None
            _error_popup_with_traceback(
                'Your Window has an Tab Element with an IMAGE problem',
                'The traceback will show you the Window with the problem layout',
                f'Look in this Window\'s layout for an Image tab_element that has a key of {tab_element.Key}',
                'The error occuring is:',
                e,
            )

        tab_element.photo = photo
        # add the label
        if photo is not None:
            width, height = photo.width(), photo.height()
            tab_element.tktext_label = tk.Label(tab_element.ParentRowFrame, image=photo, width=width, height=height, bd=0)
        else:
            tab_element.tktext_label = tk.Label(tab_element.ParentRowFrame, bd=0)
        # ------------------- end of imagey-stuff -------------------

        state = 'normal'
        if tab_element.Disabled:
            state = 'disabled'
        if tab_element.visible is False:
            state = 'hidden'
        if photo is not None:
            self.TKNotebook.add(tab_element.TKFrame, text=tab_element.Title, compound=tk.LEFT, state=state, image=photo)
        else:
            self.TKNotebook.add(tab_element.TKFrame, text=tab_element.Title, state=state)
        tab_element.ParentNotebook = self.TKNotebook
        tab_element.TabID = self.TabCount
        tab_element.ParentForm = self.ParentForm
        self.TabCount += 1
        if tab_element.BackgroundColor != COLOR_SYSTEM_DEFAULT and tab_element.BackgroundColor is not None:
            tab_element.TKFrame.configure(
                background=tab_element.BackgroundColor,
                highlightbackground=tab_element.BackgroundColor,
                highlightcolor=tab_element.BackgroundColor,
            )
        if tab_element.BorderWidth is not None:
            tab_element.TKFrame.configure(borderwidth=tab_element.BorderWidth)
        if tab_element.Tooltip is not None:
            tab_element.TooltipObject = ToolTip(tab_element.TKFrame, text=tab_element.Tooltip, timeout=FreeSimpleGUI.DEFAULT_TOOLTIP_TIME)
        _add_right_click_menu(tab_element, form)

    def update(self, visible=None):
        """
        Enables changing the visibility

        :param visible:  control visibility of element
        :type visible:   (bool)
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in TabGroup.update - The window was closed')
            return

        if visible is False:
            self._pack_forget_save_settings()
        elif visible is True:
            self._pack_restore_settings()

        if visible is not None:
            self._visible = visible

    AddRow = add_row
    FindKeyFromTabName = find_key_from_tab_name
    Get = get
    Layout = layout
