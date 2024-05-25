from __future__ import annotations

import tkinter as tk
import warnings

import FreeSimpleGUI
from FreeSimpleGUI import _make_ttk_scrollbar
from FreeSimpleGUI import _random_error_emoji
from FreeSimpleGUI import ELEM_TYPE_COLUMN
from FreeSimpleGUI import popup_error
from FreeSimpleGUI import VarHolder
from FreeSimpleGUI._utils import _error_popup_with_traceback
from FreeSimpleGUI.elements.base import Element


class TkFixedFrame(tk.Frame):
    """
    A tkinter frame that is used with Column Elements that do not have a scrollbar
    """

    def __init__(self, master, **kwargs):
        """
        :param master:   The parent widget
        :type master:    (tk.Widget)
        :param **kwargs: The keyword args
        :type **kwargs:
        """
        tk.Frame.__init__(self, master, **kwargs)

        self.canvas = tk.Canvas(self)

        self.canvas.pack(side='left', fill='both', expand=True)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.TKFrame = tk.Frame(self.canvas, **kwargs)
        self.frame_id = self.canvas.create_window(0, 0, window=self.TKFrame, anchor='nw')
        self.canvas.config(borderwidth=0, highlightthickness=0)
        self.TKFrame.config(borderwidth=0, highlightthickness=0)
        self.config(borderwidth=0, highlightthickness=0)


class TkScrollableFrame(tk.Frame):
    """
    A frame with one or two scrollbars.  Used to make Columns with scrollbars
    """

    def __init__(self, master, vertical_only, element, window, **kwargs):
        """
        :param master:        The parent widget
        :type master:         (tk.Widget)
        :param vertical_only: if True the only a vertical scrollbar will be shown
        :type vertical_only:  (bool)
        :param element:       The element containing this object
        :type element:        (Column)
        """
        tk.Frame.__init__(self, master, **kwargs)
        # create a canvas object and a vertical scrollbar for scrolling it

        self.canvas = tk.Canvas(self)
        element.Widget = self.canvas
        # Okay, we're gonna make a list. Containing the y-min, x-min, y-max, and x-max of the frame
        element.element_frame = self
        _make_ttk_scrollbar(element, 'v', window)
        # element.vsb = tk.Scrollbar(self, orient=tk.VERTICAL)
        element.vsb.pack(side='right', fill='y', expand='false')

        if not vertical_only:
            _make_ttk_scrollbar(element, 'h', window)
            # self.hscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
            element.hsb.pack(side='bottom', fill='x', expand='false')
            self.canvas.config(xscrollcommand=element.hsb.set)

        self.canvas.config(yscrollcommand=element.vsb.set)
        self.canvas.pack(side='left', fill='both', expand=True)
        element.vsb.config(command=self.canvas.yview)
        if not vertical_only:
            element.hsb.config(command=self.canvas.xview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.TKFrame = tk.Frame(self.canvas, **kwargs)
        self.frame_id = self.canvas.create_window(0, 0, window=self.TKFrame, anchor='nw')
        self.canvas.config(borderwidth=0, highlightthickness=0)
        self.TKFrame.config(borderwidth=0, highlightthickness=0)
        self.config(borderwidth=0, highlightthickness=0)

        # Canvas can be: master, canvas, TKFrame

        self.unhookMouseWheel(None)
        self.canvas.bind('<Enter>', self.hookMouseWheel)
        self.canvas.bind('<Leave>', self.unhookMouseWheel)
        self.bind('<Configure>', self.set_scrollregion)

    def hookMouseWheel(self, e):
        # print("enter")
        VarHolder.canvas_holder = self.canvas
        self.canvas.bind_all('<4>', self.yscroll, add='+')
        self.canvas.bind_all('<5>', self.yscroll, add='+')
        self.canvas.bind_all('<MouseWheel>', self.yscroll, add='+')
        self.canvas.bind_all('<Shift-MouseWheel>', self.xscroll, add='+')

    # Chr0nic
    def unhookMouseWheel(self, e):
        # print("leave")
        VarHolder.canvas_holder = None
        self.canvas.unbind_all('<4>')
        self.canvas.unbind_all('<5>')
        self.canvas.unbind_all('<MouseWheel>')
        self.canvas.unbind_all('<Shift-MouseWheel>')

    def resize_frame(self, e):
        self.canvas.itemconfig(self.frame_id, height=e.height, width=e.width)

    def yscroll(self, event):
        if self.canvas.yview() == (0.0, 1.0):
            return
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, 'unit')
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, 'unit')

    def xscroll(self, event):
        if event.num == 5 or event.delta < 0:
            self.canvas.xview_scroll(1, 'unit')
        elif event.num == 4 or event.delta > 0:
            self.canvas.xview_scroll(-1, 'unit')

    def bind_mouse_scroll(self, parent, mode):
        # ~~ Windows only
        parent.bind('<MouseWheel>', mode)
        # ~~ Unix only
        parent.bind('<Button-4>', mode)
        parent.bind('<Button-5>', mode)

    def set_scrollregion(self, event=None):
        """Set the scroll region on the canvas"""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))


class Column(Element):
    """
    A container element that is used to create a layout within your window's layout
    """

    def __init__(
        self,
        layout,
        background_color=None,
        size=(None, None),
        s=(None, None),
        size_subsample_width=1,
        size_subsample_height=2,
        pad=None,
        p=None,
        scrollable=False,
        vertical_scroll_only=False,
        right_click_menu=None,
        key=None,
        k=None,
        visible=True,
        justification=None,
        element_justification=None,
        vertical_alignment=None,
        grab=None,
        expand_x=None,
        expand_y=None,
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
        :param layout:                      Layout that will be shown in the Column container
        :type layout:                       List[List[Element]]
        :param background_color:            color of background of entire Column
        :type background_color:             (str)
        :param size:                        (width, height) size in pixels (doesn't work quite right, sometimes only 1 dimension is set by tkinter. Use a Sizer Element to help set sizes
        :type size:                         (int | None, int | None)
        :param s:                           Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                            (int | None, int | None)
        :param size_subsample_width:        Determines the size of a scrollable column width based on 1/size_subsample * required size. 1 = match the contents exactly, 2 = 1/2 contents size, 3 = 1/3. Can be a fraction to make larger than required.
        :type size_subsample_width:         (float)
        :param size_subsample_height:       Determines the size of a scrollable height based on 1/size_subsample * required size. 1 = match the contents exactly, 2 = 1/2 contents size, 3 = 1/3. Can be a fraction to make larger than required..
        :type size_subsample_height:        (float)
        :param pad:                         Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:                          (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                           Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                            (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param scrollable:                  if True then scrollbars will be added to the column. If you update the contents of a scrollable column, be sure and call Column.contents_changed also
        :type scrollable:                   (bool)
        :param vertical_scroll_only:        if True then no horizontal scrollbar will be shown if a scrollable column
        :type vertical_scroll_only:         (bool)
        :param right_click_menu:            A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type right_click_menu:             List[List[ List[str] | str ]]
        :param key:                         Value that uniquely identifies this element from all other elements. Used when Finding an element or in return values. Must be unique to the window
        :type key:                          str | int | tuple | object
        :param k:                           Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                            str | int | tuple | object
        :param visible:                     set visibility state of the element
        :type visible:                      (bool)
        :param justification:               set justification for the Column itself. Note entire row containing the Column will be affected
        :type justification:                (str)
        :param element_justification:       All elements inside the Column will have this justification 'left', 'right', 'center' are valid values
        :type element_justification:        (str)
        :param vertical_alignment:          Place the column at the 'top', 'center', 'bottom' of the row (can also use t,c,r). Defaults to no setting (tkinter decides)
        :type vertical_alignment:           (str)
        :param grab:                        If True can grab this element and move the window around. Default is False
        :type grab:                         (bool)
        :param expand_x:                    If True the column will automatically expand in the X direction to fill available space
        :type expand_x:                     (bool)
        :param expand_y:                    If True the column will automatically expand in the Y direction to fill available space
        :type expand_y:                     (bool)
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

        self.UseDictionary = False
        self.ReturnValues = None
        self.ReturnValuesList = []
        self.ReturnValuesDictionary = {}
        self.DictionaryKeyCounter = 0
        self.ParentWindow = None
        self.ParentPanedWindow = None
        self.Rows = []
        self.TKFrame = None
        self.TKColFrame = None  # type: tk.Frame
        self.Scrollable = scrollable
        self.VerticalScrollOnly = vertical_scroll_only

        self.RightClickMenu = right_click_menu
        bg = background_color if background_color is not None else FreeSimpleGUI.DEFAULT_BACKGROUND_COLOR
        self.ContainerElemementNumber = Window._GetAContainerNumber()
        self.ElementJustification = element_justification
        self.Justification = justification
        self.VerticalAlignment = vertical_alignment
        key = key if key is not None else k
        self.Grab = grab
        self.expand_x = expand_x
        self.expand_y = expand_y
        self.Layout(layout)
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p
        self.size_subsample_width = size_subsample_width
        self.size_subsample_height = size_subsample_height

        super().__init__(
            ELEM_TYPE_COLUMN,
            background_color=bg,
            size=sz,
            pad=pad,
            key=key,
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
        return

    def add_row(self, *args):
        """
        Not recommended user call.  Used to add rows of Elements to the Column Element.

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
                    'Error creating Column layout',
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
                    'Error creating Column layout',
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
                    'Error creating Column layout',
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
        :rtype:      (Column)
        """

        for row in rows:
            try:
                iter(row)
            except TypeError:
                popup_error(
                    'Error creating Column layout',
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

        :param location:     (row, column) position of the element to find in layout
        :type  location:     (int, int)
        :return:             The element found at the location
        :rtype:              (Element)
        """

        (row_num, col_num) = location
        row = self.Rows[row_num]
        element = row[col_num]
        return element

    def update(self, visible=None):
        """
        Changes some of the settings for the Column Element. Must call `Window.Read` or `Window.Finalize` prior

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param visible: control visibility of element
        :type visible:  (bool)
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Column.update - The window was closed')
            return

        if visible is False:
            if self.TKColFrame:
                self._pack_forget_save_settings()
            if self.ParentPanedWindow:
                self.ParentPanedWindow.remove(self.TKColFrame)
        elif visible is True:
            if self.TKColFrame:
                self._pack_restore_settings()
            if self.ParentPanedWindow:
                self.ParentPanedWindow.add(self.TKColFrame)
        if visible is not None:
            self._visible = visible

    def contents_changed(self):
        """
        When a scrollable column has part of its layout changed by making elements visible or invisible or the
        layout is extended for the Column, then this method needs to be called so that the new scroll area
        is computed to match the new contents.
        """
        self.TKColFrame.canvas.config(scrollregion=self.TKColFrame.canvas.bbox('all'))

    AddRow = add_row
    Layout = layout
    Update = update


from FreeSimpleGUI.window import Window
