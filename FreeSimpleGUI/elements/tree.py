from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Any
from typing import Dict
from typing import List

import FreeSimpleGUI
from FreeSimpleGUI import ELEM_TYPE_TREE
from FreeSimpleGUI import Element
from FreeSimpleGUI import LOOK_AND_FEEL_TABLE
from FreeSimpleGUI import theme_button_color
from FreeSimpleGUI._utils import _error_popup_with_traceback
from FreeSimpleGUI._utils import _exit_mainloop


class Tree(Element):
    """
    Tree Element - Presents data in a tree-like manner, much like a file/folder browser.  Uses the TreeData class
    to hold the user's data and pass to the element for display.
    """

    def __init__(
        self,
        data=None,
        headings=None,
        visible_column_map=None,
        col_widths=None,
        col0_width=10,
        col0_heading='',
        def_col_width=10,
        auto_size_columns=True,
        max_col_width=20,
        select_mode=None,
        show_expanded=False,
        change_submits=False,
        enable_events=False,
        click_toggles_select=None,
        font=None,
        justification='right',
        text_color=None,
        border_width=None,
        background_color=None,
        selected_row_colors=(None, None),
        header_text_color=None,
        header_background_color=None,
        header_font=None,
        header_border_width=None,
        header_relief=None,
        num_rows=None,
        sbar_trough_color=None,
        sbar_background_color=None,
        sbar_arrow_color=None,
        sbar_width=None,
        sbar_arrow_width=None,
        sbar_frame_color=None,
        sbar_relief=None,
        row_height=None,
        vertical_scroll_only=True,
        hide_vertical_scroll=False,
        pad=None,
        p=None,
        key=None,
        k=None,
        tooltip=None,
        right_click_menu=None,
        expand_x=False,
        expand_y=False,
        visible=True,
        metadata=None,
    ):
        """
        :param data:                    The data represented using a PySimpleGUI provided TreeData class
        :type data:                     (TreeData)
        :param headings:                List of individual headings for each column
        :type headings:                 List[str]
        :param visible_column_map:      Determines if a column should be visible. If left empty, all columns will be shown
        :type visible_column_map:       List[bool]
        :param col_widths:              List of column widths so that individual column widths can be controlled
        :type col_widths:               List[int]
        :param col0_width:              Size of Column 0 which is where the row numbers will be optionally shown
        :type col0_width:               (int)
        :param col0_heading:            Text to be shown in the header for the left-most column
        :type col0_heading:             (str)
        :param def_col_width:           default column width
        :type def_col_width:            (int)
        :param auto_size_columns:       if True, the size of a column is determined  using the contents of the column
        :type auto_size_columns:        (bool)
        :param max_col_width:           the maximum size a column can be
        :type max_col_width:            (int)
        :param select_mode:             Use same values as found on Table Element.  Valid values include: TABLE_SELECT_MODE_NONE TABLE_SELECT_MODE_BROWSE TABLE_SELECT_MODE_EXTENDED
        :type select_mode:              (enum)
        :param show_expanded:           if True then the tree will be initially shown with all nodes completely expanded
        :type show_expanded:            (bool)
        :param change_submits:          DO NOT USE. Only listed for backwards compat - Use enable_events instead
        :type change_submits:           (bool)
        :param enable_events:           Turns on the element specific events. Tree events happen when row is clicked
        :type enable_events:            (bool)
        :param click_toggles_select:    If True then clicking a row will cause the selection for that row to toggle between selected and deselected
        :type click_toggles_select:     (bool)
        :param font:                    specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:                     (str or (str, int[, str]) or None)
        :param justification:           'left', 'right', 'center' are valid choices
        :type justification:            (str)
        :param text_color:              color of the text
        :type text_color:               (str)
        :param border_width:            Border width/depth in pixels
        :type border_width:             (int)
        :param background_color:        color of background
        :type background_color:         (str)
        :param selected_row_colors:     Sets the text color and background color for a selected row. Same format as button colors - tuple ('red', 'yellow') or string 'red on yellow'. Defaults to theme's button color
        :type selected_row_colors:      str or (str, str)
        :param header_text_color:       sets the text color for the header
        :type header_text_color:        (str)
        :param header_background_color: sets the background color for the header
        :type header_background_color:  (str)
        :param header_font:             specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type header_font:              (str or (str, int[, str]) or None)
        :param header_border_width:     Border width for the header portion
        :type header_border_width:      (int | None)
        :param header_relief:           Relief style for the header. Values are same as other elements that use relief. RELIEF_RAISED RELIEF_SUNKEN RELIEF_FLAT RELIEF_RIDGE RELIEF_GROOVE RELIEF_SOLID
        :type header_relief:            (str | None)
        :param num_rows:                The number of rows of the table to display at a time
        :type num_rows:                 (int)
        :param row_height:              height of a single row in pixels
        :type row_height:               (int)
        :param vertical_scroll_only:    if True only the vertical scrollbar will be visible
        :type vertical_scroll_only:     (bool)
        :param hide_vertical_scroll:    if True vertical scrollbar will be hidden
        :type hide_vertical_scroll:     (bool)
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
        :param pad:                     Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:                      (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                       Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                        (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param key:                     Used with window.find_element and with return values to uniquely identify this element to uniquely identify this element
        :type key:                      str | int | tuple | object
        :param k:                       Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                        str | int | tuple | object
        :param tooltip:                 text, that will appear when mouse hovers over the element
        :type tooltip:                  (str)
        :param right_click_menu:        A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type right_click_menu:         List[List[str] | str]]
        :param expand_x:                If True the element will automatically expand in the X direction to fill available space
        :type expand_x:                 (bool)
        :param expand_y:                If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:                 (bool)
        :param visible:                 set visibility state of the element
        :type visible:                  (bool)
        :param metadata:                User metadata that can be set to ANYTHING
        :type metadata:                 (Any)
        """

        self.image_dict = {}

        self.TreeData = data
        self.ColumnHeadings = headings
        self.ColumnsToDisplay = visible_column_map
        self.ColumnWidths = col_widths
        self.MaxColumnWidth = max_col_width
        self.DefaultColumnWidth = def_col_width
        self.AutoSizeColumns = auto_size_columns
        self.BackgroundColor = background_color if background_color is not None else FreeSimpleGUI.DEFAULT_BACKGROUND_COLOR
        self.TextColor = text_color
        self.HeaderTextColor = header_text_color if header_text_color is not None else LOOK_AND_FEEL_TABLE[FreeSimpleGUI.CURRENT_LOOK_AND_FEEL]['TEXT_INPUT']
        self.HeaderBackgroundColor = header_background_color if header_background_color is not None else LOOK_AND_FEEL_TABLE[FreeSimpleGUI.CURRENT_LOOK_AND_FEEL]['INPUT']
        self.HeaderBorderWidth = header_border_width
        self.BorderWidth = border_width
        self.HeaderRelief = header_relief
        self.click_toggles_select = click_toggles_select
        if selected_row_colors == (None, None):
            # selected_row_colors = DEFAULT_TABLE_AND_TREE_SELECTED_ROW_COLORS
            selected_row_colors = theme_button_color()
        else:
            try:
                if isinstance(selected_row_colors, str):
                    selected_row_colors = selected_row_colors.split(' on ')
            except Exception as e:
                print('* Table Element Warning * you messed up with color formatting of Selected Row Color', e)
        self.SelectedRowColors = selected_row_colors

        self.HeaderFont = header_font
        self.Justification = justification
        self.InitialState = None
        self.SelectMode = select_mode
        self.ShowExpanded = show_expanded
        self.NumRows = num_rows
        self.Col0Width = col0_width
        self.col0_heading = col0_heading
        self.TKTreeview = None  # type: ttk.Treeview
        self.element_frame = None  # type: tk.Frame
        self.VerticalScrollOnly = vertical_scroll_only
        self.HideVerticalScroll = hide_vertical_scroll
        self.SelectedRows = []
        self.ChangeSubmits = change_submits or enable_events
        self.RightClickMenu = right_click_menu
        self.RowHeight = row_height
        self.IconList = {}
        self.IdToKey = {'': ''}
        self.KeyToID = {'': ''}
        key = key if key is not None else k
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y

        super().__init__(
            ELEM_TYPE_TREE,
            text_color=text_color,
            background_color=background_color,
            font=font,
            pad=pad,
            key=key,
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
        return

    def _treeview_selected(self, event):
        """
        Not a user function.  Callback function that happens when an item is selected from the tree.  In this
        method, it saves away the reported selections so they can be properly returned.

        :param event: An event parameter passed in by tkinter.  Not used
        :type event:  (Any)
        """

        selections = self.TKTreeview.selection()
        selected_rows = [self.IdToKey[x] for x in selections]
        if self.click_toggles_select:
            if set(self.SelectedRows) == set(selected_rows):
                for item in selections:
                    self.TKTreeview.selection_remove(item)
                selections = []
        self.SelectedRows = [self.IdToKey[x] for x in selections]

        if self.ChangeSubmits:
            if self.Key is not None:
                self.ParentForm.LastButtonClicked = self.Key
            else:
                self.ParentForm.LastButtonClicked = ''
            self.ParentForm.FormRemainedOpen = True
            _exit_mainloop(self.ParentForm)

    def add_treeview_data(self, node):
        """
        Not a user function.  Recursive method that inserts tree data into the tkinter treeview widget.

        :param node: The node to insert.  Will insert all nodes from starting point downward, recursively
        :type node:  (TreeData)
        """
        if node.key != '':
            if node.icon:
                try:
                    if node.icon not in self.image_dict:
                        if type(node.icon) is bytes:
                            photo = tk.PhotoImage(data=node.icon)
                        else:
                            photo = tk.PhotoImage(file=node.icon)
                        self.image_dict[node.icon] = photo
                    else:
                        photo = self.image_dict.get(node.icon)

                    node.photo = photo
                    id = self.TKTreeview.insert(
                        self.KeyToID[node.parent],
                        'end',
                        iid=None,
                        text=node.text,
                        values=node.values,
                        open=self.ShowExpanded,
                        image=node.photo,
                    )
                    self.IdToKey[id] = node.key
                    self.KeyToID[node.key] = id
                except:
                    self.photo = None
            else:
                id = self.TKTreeview.insert(
                    self.KeyToID[node.parent],
                    'end',
                    iid=None,
                    text=node.text,
                    values=node.values,
                    open=self.ShowExpanded,
                )
                self.IdToKey[id] = node.key
                self.KeyToID[node.key] = id

        for node in node.children:
            self.add_treeview_data(node)

    def update(self, values=None, key=None, value=None, text=None, icon=None, visible=None):
        """
        Changes some of the settings for the Tree Element. Must call `Window.Read` or `Window.Finalize` prior

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param values:  Representation of the tree
        :type values:   (TreeData)
        :param key:     identifies a particular item in tree to update
        :type key:      str | int | tuple | object
        :param value:   sets the node identified by key to a particular value
        :type value:    (Any)
        :param text:    sets the node identified by key to this string
        :type text:     (str)
        :param icon:    can be either a base64 icon or a filename for the icon
        :type icon:     bytes | str
        :param visible: control visibility of element
        :type visible:  (bool)
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Tree.update - The window was closed')
            return

        if values is not None:
            children = self.TKTreeview.get_children()
            for i in children:
                self.TKTreeview.detach(i)
                self.TKTreeview.delete(i)
            children = self.TKTreeview.get_children()
            self.TreeData = values
            self.IdToKey = {'': ''}
            self.KeyToID = {'': ''}
            self.add_treeview_data(self.TreeData.root_node)
            self.SelectedRows = []
        if key is not None:
            for id in self.IdToKey.keys():
                if key == self.IdToKey[id]:
                    break
            else:
                id = None
                print('** Key not found **')
        else:
            id = None
        if id:
            # item = self.TKTreeview.item(id)
            if value is not None:
                self.TKTreeview.item(id, values=value)
            if text is not None:
                self.TKTreeview.item(id, text=text)
            if icon is not None:
                try:
                    if type(icon) is bytes:
                        photo = tk.PhotoImage(data=icon)
                    else:
                        photo = tk.PhotoImage(file=icon)
                    self.TKTreeview.item(id, image=photo)
                    self.IconList[key] = photo  # save so that it's not deleted (save reference)
                except:
                    pass
            # item = self.TKTreeview.item(id)
        if visible is False:
            self._pack_forget_save_settings(self.element_frame)
        elif visible is True:
            self._pack_restore_settings(self.element_frame)

        if visible is not None:
            self._visible = visible

        return self

    Update = update


class TreeData:
    """
    Class that user fills in to represent their tree data. It's a very simple tree representation with a root "Node"
    with possibly one or more children "Nodes".  Each Node contains a key, text to display, list of values to display
    and an icon.  The entire tree is built using a single method, Insert.  Nothing else is required to make the tree.
    """

    class Node:
        """
        Contains information about the individual node in the tree
        """

        def __init__(self, parent, key, text, values, icon=None):
            """
            Represents a node within the TreeData class

            :param parent: The parent Node
            :type parent:  (TreeData.Node)
            :param key:    Used to uniquely identify this node
            :type key:     str | int | tuple | object
            :param text:   The text that is displayed at this node's location
            :type text:    (str)
            :param values: The list of values that are displayed at this node
            :type values:  List[Any]
            :param icon:   just a icon
            :type icon:    str | bytes
            """

            self.parent = parent  # type: TreeData.Node
            self.children = []  # type: List[TreeData.Node]
            self.key = key  # type: str
            self.text = text  # type: str
            self.values = values  # type: List[Any]
            self.icon = icon  # type: str | bytes

        def _Add(self, node):
            self.children.append(node)

    def __init__(self):
        """
        Instantiate the object, initializes the Tree Data, creates a root node for you
        """
        self.tree_dict = {}  # type: Dict[str, TreeData.Node]
        self.root_node = self.Node('', '', 'root', [], None)  # The root node
        self.tree_dict[''] = self.root_node  # Start the tree out with the root node

    def _AddNode(self, key, node):
        """
        Adds a node to tree dictionary (not user callable)

        :param key:  Uniquely identifies this Node
        :type key:   (str)
        :param node: Node being added
        :type node:  (TreeData.Node)
        """
        self.tree_dict[key] = node

    def insert(self, parent, key, text, values, icon=None):
        """
        Inserts a node into the tree. This is how user builds their tree, by Inserting Nodes
        This is the ONLY user callable method in the TreeData class

        :param parent: the parent Node
        :type parent:  (Node)
        :param key:    Used to uniquely identify this node
        :type key:     str | int | tuple | object
        :param text:   The text that is displayed at this node's location
        :type text:    (str)
        :param values: The list of values that are displayed at this node
        :type values:  List[Any]
        :param icon:   icon
        :type icon:    str | bytes
        """

        node = self.Node(parent, key, text, values, icon)
        self.tree_dict[key] = node
        parent_node = self.tree_dict[parent]
        parent_node._Add(node)

    def __repr__(self):
        """
        Converts the TreeData into a printable version, nicely formatted

        :return: (str) A formatted, text version of the TreeData
        :rtype:
        """
        return self._NodeStr(self.root_node, 1)

    def _NodeStr(self, node, level):
        """
        Does the magic of converting the TreeData into a nicely formatted string version

        :param node:  The node to begin printing the tree
        :type node:   (TreeData.Node)
        :param level: The indentation level for string formatting
        :type level:  (int)
        """
        return '\n'.join([str(node.key) + ' : ' + str(node.text) + ' [ ' + ', '.join([str(v) for v in node.values]) + ' ]'] + [' ' * 4 * level + self._NodeStr(child, level + 1) for child in node.children])

    Insert = insert
