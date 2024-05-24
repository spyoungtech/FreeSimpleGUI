from __future__ import annotations

import FreeSimpleGUI
from FreeSimpleGUI import ELEM_TYPE_PANE
from FreeSimpleGUI import Element
from FreeSimpleGUI import RELIEF_RAISED
from FreeSimpleGUI._utils import _error_popup_with_traceback


class Pane(Element):
    """
    A sliding Pane that is unique to tkinter.  Uses Columns to create individual panes
    """

    def __init__(
        self,
        pane_list,
        background_color=None,
        size=(None, None),
        s=(None, None),
        pad=None,
        p=None,
        orientation='vertical',
        show_handle=True,
        relief=RELIEF_RAISED,
        handle_size=None,
        border_width=None,
        key=None,
        k=None,
        expand_x=None,
        expand_y=None,
        visible=True,
        metadata=None,
    ):
        """
        :param pane_list:        Must be a list of Column Elements. Each Column supplied becomes one pane that's shown
        :type pane_list:         List[Column] | Tuple[Column]
        :param background_color: color of background
        :type background_color:  (str)
        :param size:             (width, height) w=characters-wide, h=rows-high How much room to reserve for the Pane
        :type size:              (int, int)
        :param s:                Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                 (int, int)  | (None, None)
        :param pad:              Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:               (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                 (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param orientation:      'horizontal' or 'vertical' or ('h' or 'v'). Direction the Pane should slide
        :type orientation:       (str)
        :param show_handle:      if True, the handle is drawn that makes it easier to grab and slide
        :type show_handle:       (bool)
        :param relief:           relief style. Values are same as other elements that use relief values. RELIEF_RAISED RELIEF_SUNKEN RELIEF_FLAT RELIEF_RIDGE RELIEF_GROOVE RELIEF_SOLID
        :type relief:            (enum)
        :param handle_size:      Size of the handle in pixels
        :type handle_size:       (int)
        :param border_width:     width of border around element in pixels
        :type border_width:      (int)
        :param key:              Value that uniquely identifies this element from all other elements. Used when Finding an element or in return values. Must be unique to the window
        :type key:               str | int | tuple | object
        :param k:                Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                 str | int | tuple | object
        :param expand_x:         If True the column will automatically expand in the X direction to fill available space
        :type expand_x:          (bool)
        :param expand_y:         If True the column will automatically expand in the Y direction to fill available space
        :type expand_y:          (bool)
        :param visible:          set visibility state of the element
        :type visible:           (bool)
        :param metadata:         User metadata that can be set to ANYTHING
        :type metadata:          (Any)
        """

        self.UseDictionary = False
        self.ReturnValues = None
        self.ReturnValuesList = []
        self.ReturnValuesDictionary = {}
        self.DictionaryKeyCounter = 0
        self.ParentWindow = None
        self.Rows = []
        self.TKFrame = None
        self.PanedWindow = None
        self.Orientation = orientation
        self.PaneList = pane_list
        self.ShowHandle = show_handle
        self.Relief = relief
        self.HandleSize = handle_size or 8
        self.BorderDepth = border_width
        bg = background_color if background_color is not None else FreeSimpleGUI.DEFAULT_BACKGROUND_COLOR

        self.Rows = [pane_list]
        key = key if key is not None else k
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y

        super().__init__(ELEM_TYPE_PANE, background_color=bg, size=sz, pad=pad, key=key, visible=visible, metadata=metadata)
        return

    def update(self, visible=None):
        """
        Changes some of the settings for the Pane Element. Must call `Window.Read` or `Window.Finalize` prior

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
            _error_popup_with_traceback('Error in Pane.update - The window was closed')
            return

        if visible is False:
            self._pack_forget_save_settings()
        elif visible is True:
            self._pack_restore_settings()

        if visible is not None:
            self._visible = visible

    Update = update
