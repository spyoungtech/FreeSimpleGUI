from __future__ import annotations

import tkinter as tk
import warnings

import FreeSimpleGUI
from FreeSimpleGUI import _random_error_emoji
from FreeSimpleGUI import ELEM_TYPE_FRAME
from FreeSimpleGUI import Element
from FreeSimpleGUI import popup_error
from FreeSimpleGUI._utils import _error_popup_with_traceback
from FreeSimpleGUI.window import Window


class Frame(Element):
    """
    A Frame Element that contains other Elements. Encloses with a line around elements and a text label.
    """

    def __init__(
        self,
        title,
        layout,
        title_color=None,
        background_color=None,
        title_location=None,
        relief=FreeSimpleGUI.DEFAULT_FRAME_RELIEF,
        size=(None, None),
        s=(None, None),
        font=None,
        pad=None,
        p=None,
        border_width=None,
        key=None,
        k=None,
        tooltip=None,
        right_click_menu=None,
        expand_x=False,
        expand_y=False,
        grab=None,
        visible=True,
        element_justification='left',
        vertical_alignment=None,
        metadata=None,
    ):
        """
        :param title:                 text that is displayed as the Frame's "label" or title
        :type title:                  (str)
        :param layout:                The layout to put inside the Frame
        :type layout:                 List[List[Elements]]
        :param title_color:           color of the title text
        :type title_color:            (str)
        :param background_color:      background color of the Frame
        :type background_color:       (str)
        :param title_location:        location to place the text title.  Choices include: TITLE_LOCATION_TOP TITLE_LOCATION_BOTTOM TITLE_LOCATION_LEFT TITLE_LOCATION_RIGHT TITLE_LOCATION_TOP_LEFT TITLE_LOCATION_TOP_RIGHT TITLE_LOCATION_BOTTOM_LEFT TITLE_LOCATION_BOTTOM_RIGHT
        :type title_location:         (enum)
        :param relief:                relief style. Values are same as other elements with reliefs. Choices include RELIEF_RAISED RELIEF_SUNKEN RELIEF_FLAT RELIEF_RIDGE RELIEF_GROOVE RELIEF_SOLID
        :type relief:                 (enum)
        :param size:                  (width, height) Sets an initial hard-coded size for the Frame. This used to be a problem, but was fixed in 4.53.0 and works better than Columns when using the size paramter
        :type size:                   (int, int)
        :param s:                     Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                      (int, int)  | (None, None) | int
        :param font:                  specifies the  font family, size, etc. for the TITLE. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:                   (str or (str, int[, str]) or None)
        :param pad:                   Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:                    (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                     Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                      (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param border_width:          width of border around element in pixels
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
        :param grab:                  If True can grab this element and move the window around. Default is False
        :type grab:                   (bool)
        :param visible:               set visibility state of the element
        :type visible:                (bool)
        :param element_justification: All elements inside the Frame will have this justification 'left', 'right', 'center' are valid values
        :type element_justification:  (str)
        :param vertical_alignment:    Place the Frame at the 'top', 'center', 'bottom' of the row (can also use t,c,r). Defaults to no setting (tkinter decides)
        :type vertical_alignment:     (str)
        :param metadata:              User metadata that can be set to ANYTHING
        :type metadata:               (Any)
        """

        self.UseDictionary = False
        self.ReturnValues = None
        self.ReturnValuesList = []
        self.ReturnValuesDictionary = {}
        self.DictionaryKeyCounter = 0
        self.ParentWindow = None
        self.Rows = []
        # self.ParentForm = None
        self.TKFrame = None
        self.Title = title
        self.Relief = relief
        self.TitleLocation = title_location
        self.BorderWidth = border_width
        self.BackgroundColor = background_color if background_color is not None else FreeSimpleGUI.DEFAULT_BACKGROUND_COLOR
        self.RightClickMenu = right_click_menu
        self.ContainerElemementNumber = Window._GetAContainerNumber()
        self.ElementJustification = element_justification
        self.VerticalAlignment = vertical_alignment
        self.Widget = None  # type: tk.LabelFrame
        self.Grab = grab
        self.Layout(layout)
        key = key if key is not None else k
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y

        super().__init__(
            ELEM_TYPE_FRAME,
            background_color=background_color,
            text_color=title_color,
            size=sz,
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

        :param *args: The list of elements for this row
        :type *args:  List[Element]
        """
        NumRows = len(self.Rows)  # number of existing rows is our row number
        CurrentRowNumber = NumRows  # this row's number
        CurrentRow = []  # start with a blank row and build up
        # -------------------------  Add the elements to a row  ------------------------- #
        for i, element in enumerate(args):  # Loop through list of elements and add them to the row
            if type(element) is list:
                popup_error(
                    'Error creating Frame layout',
                    'Layout has a LIST instead of an ELEMENT',
                    'This sometimes means you have a badly placed ]',
                    'The offensive list is:',
                    element,
                    'This list will be stripped from your layout',
                    keep_on_top=True,
                )
                continue
            elif callable(element) and not isinstance(element, Element):
                popup_error(
                    'Error creating Frame layout',
                    'Layout has a FUNCTION instead of an ELEMENT',
                    'This likely means you are missing () from your layout',
                    'The offensive list is:',
                    element,
                    'This item will be stripped from your layout',
                    keep_on_top=True,
                )
                continue
            if element.ParentContainer is not None:
                warnings.warn(
                    '*** YOU ARE ATTEMPTING TO REUSE AN ELEMENT IN YOUR LAYOUT! Once placed in a layout, an element cannot be used in another layout. ***',
                    UserWarning,
                )
                _error_popup_with_traceback(
                    'Error creating Frame layout',
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
                    'Error creating Frame layout',
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
        :return:         (Element) The element found at the location
        :rtype:          (Element)
        """

        (row_num, col_num) = location
        row = self.Rows[row_num]
        element = row[col_num]
        return element

    def update(self, value=None, visible=None):
        """
        Changes some of the settings for the Frame Element. Must call `Window.Read` or `Window.Finalize` prior

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param value:   New text value to show on frame
        :type value:    (Any)
        :param visible: control visibility of element
        :type visible:  (bool)
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Frame.update - The window was closed')
            return

        if visible is False:
            self._pack_forget_save_settings()
            # self.TKFrame.pack_forget()
        elif visible is True:
            self._pack_restore_settings()
            # self.TKFrame.pack(padx=self.pad_used[0], pady=self.pad_used[1])
        if value is not None:
            self.TKFrame.config(text=str(value))
        if visible is not None:
            self._visible = visible

    AddRow = add_row
    Layout = layout
    Update = update
