from __future__ import annotations

import warnings
from tkinter import ttk

import FreeSimpleGUI
from FreeSimpleGUI import COLOR_SYSTEM_DEFAULT
from FreeSimpleGUI import ELEM_TYPE_TABLE
from FreeSimpleGUI import Element
from FreeSimpleGUI import LOOK_AND_FEEL_TABLE
from FreeSimpleGUI import obj_to_string_single_obj
from FreeSimpleGUI import running_mac
from FreeSimpleGUI import TABLE_CLICKED_INDICATOR
from FreeSimpleGUI import theme_button_color
from FreeSimpleGUI._utils import _create_error_message
from FreeSimpleGUI._utils import _error_popup_with_traceback
from FreeSimpleGUI._utils import _exit_mainloop


class Table(Element):
    def __init__(
        self,
        values,
        headings=None,
        visible_column_map=None,
        col_widths=None,
        cols_justification=None,
        def_col_width=10,
        auto_size_columns=True,
        max_col_width=20,
        select_mode=None,
        display_row_numbers=False,
        starting_row_number=0,
        num_rows=None,
        row_height=None,
        font=None,
        justification='right',
        text_color=None,
        background_color=None,
        alternating_row_color=None,
        selected_row_colors=(None, None),
        header_text_color=None,
        header_background_color=None,
        header_font=None,
        header_border_width=None,
        header_relief=None,
        row_colors=None,
        vertical_scroll_only=True,
        hide_vertical_scroll=False,
        border_width=None,
        sbar_trough_color=None,
        sbar_background_color=None,
        sbar_arrow_color=None,
        sbar_width=None,
        sbar_arrow_width=None,
        sbar_frame_color=None,
        sbar_relief=None,
        size=(None, None),
        s=(None, None),
        change_submits=False,
        enable_events=False,
        enable_click_events=False,
        right_click_selects=False,
        bind_return_key=False,
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
        :param values:                  Your table data represented as a 2-dimensions table... a list of rows, with each row representing a row in your table.
        :type values:                   List[List[str | int | float]]
        :param headings:                The headings to show on the top line
        :type headings:                 List[str]
        :param visible_column_map:      One entry for each column. False indicates the column is not shown
        :type visible_column_map:       List[bool]
        :param col_widths:              Number of characters that each column will occupy
        :type col_widths:               List[int]
        :param cols_justification:      Justification for EACH column. Is a list of strings with the value 'l', 'r', 'c' that indicates how the column will be justified. Either no columns should be set, or have to have one for every colun
        :type cols_justification:       List[str] or Tuple[str] or None
        :param def_col_width:           Default column width in characters
        :type def_col_width:            (int)
        :param auto_size_columns:       if True columns will be sized automatically
        :type auto_size_columns:        (bool)
        :param max_col_width:           Maximum width for all columns in characters
        :type max_col_width:            (int)
        :param select_mode:             Select Mode. Valid values start with "TABLE_SELECT_MODE_".  Valid values are: TABLE_SELECT_MODE_NONE TABLE_SELECT_MODE_BROWSE TABLE_SELECT_MODE_EXTENDED
        :type select_mode:              (enum)
        :param display_row_numbers:     if True, the first column of the table will be the row #
        :type display_row_numbers:      (bool)
        :param starting_row_number:     The row number to use for the first row. All following rows will be based on this starting value. Default is 0.
        :type starting_row_number:      (int)
        :param num_rows:                The number of rows of the table to display at a time
        :type num_rows:                 (int)
        :param row_height:              height of a single row in pixels
        :type row_height:               (int)
        :param font:                    specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:                     (str or (str, int[, str]) or None)
        :param justification:           'left', 'right', 'center' are valid choices
        :type justification:            (str)
        :param text_color:              color of the text
        :type text_color:               (str)
        :param background_color:        color of background
        :type background_color:         (str)
        :param alternating_row_color:   if set then every other row will have this color in the background.
        :type alternating_row_color:    (str)
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
        :param row_colors:              list of tuples of (row, background color) OR (row, foreground color, background color). Sets the colors of listed rows to the color(s) provided (note the optional foreground color)
        :type row_colors:               List[Tuple[int, str] | Tuple[Int, str, str]]
        :param vertical_scroll_only:    if True only the vertical scrollbar will be visible
        :type vertical_scroll_only:     (bool)
        :param hide_vertical_scroll:    if True vertical scrollbar will be hidden
        :type hide_vertical_scroll:     (bool)
        :param border_width:            Border width/depth in pixels
        :type border_width:             (int)
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
        :param size:                    DO NOT USE! Use num_rows instead
        :type size:                     (int, int)
        :param change_submits:          DO NOT USE. Only listed for backwards compat - Use enable_events instead
        :type change_submits:           (bool)
        :param enable_events:           Turns on the element specific events. Table events happen when row is clicked
        :type enable_events:            (bool)
        :param enable_click_events:     Turns on the element click events that will give you (row, col) click data when the table is clicked
        :type enable_click_events:      (bool)
        :param right_click_selects:     If True, then right clicking a row will select that row if multiple rows are not currently selected
        :type right_click_selects:      (bool)
        :param bind_return_key:         if True, pressing return key will cause event coming from Table, ALSO a left button double click will generate an event if this parameter is True
        :type bind_return_key:          (bool)
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
        :type right_click_menu:         List[List[ List[str] | str ]]
        :param expand_x:                If True the element will automatically expand in the X direction to fill available space
        :type expand_x:                 (bool)
        :param expand_y:                If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:                 (bool)
        :param visible:                 set visibility state of the element
        :type visible:                  (bool)
        :param metadata:                User metadata that can be set to ANYTHING
        :type metadata:                 (Any)
        """

        self.Values = values
        self.ColumnHeadings = headings
        self.ColumnsToDisplay = visible_column_map
        self.ColumnWidths = col_widths
        self.cols_justification = cols_justification
        self.MaxColumnWidth = max_col_width
        self.DefaultColumnWidth = def_col_width
        self.AutoSizeColumns = auto_size_columns
        self.BackgroundColor = background_color if background_color is not None else FreeSimpleGUI.DEFAULT_BACKGROUND_COLOR
        self.TextColor = text_color
        self.HeaderTextColor = header_text_color if header_text_color is not None else LOOK_AND_FEEL_TABLE[FreeSimpleGUI.CURRENT_LOOK_AND_FEEL]['TEXT_INPUT']
        self.HeaderBackgroundColor = header_background_color if header_background_color is not None else LOOK_AND_FEEL_TABLE[FreeSimpleGUI.CURRENT_LOOK_AND_FEEL]['INPUT']
        self.HeaderFont = header_font
        self.Justification = justification
        self.InitialState = None
        self.SelectMode = select_mode
        self.DisplayRowNumbers = display_row_numbers
        self.NumRows = num_rows if num_rows is not None else size[1]
        self.RowHeight = row_height
        self.Widget = self.TKTreeview = None  # type: ttk.Treeview
        self.AlternatingRowColor = alternating_row_color
        self.VerticalScrollOnly = vertical_scroll_only
        self.HideVerticalScroll = hide_vertical_scroll
        self.SelectedRows = []
        self.ChangeSubmits = change_submits or enable_events
        self.BindReturnKey = bind_return_key
        self.StartingRowNumber = starting_row_number  # When displaying row numbers, where to start
        self.RowHeaderText = 'Row'
        self.enable_click_events = enable_click_events
        self.right_click_selects = right_click_selects
        self.last_clicked_position = (None, None)
        self.HeaderBorderWidth = header_border_width
        self.BorderWidth = border_width
        self.HeaderRelief = header_relief
        self.table_ttk_style_name = None  # the ttk style name for the Table itself
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

        self.RightClickMenu = right_click_menu
        self.RowColors = row_colors
        self.tree_ids = []  # ids returned when inserting items into table - will use to delete colors
        key = key if key is not None else k
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y

        super().__init__(
            ELEM_TYPE_TABLE,
            text_color=text_color,
            background_color=background_color,
            font=font,
            size=sz,
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

    def update(self, values=None, num_rows=None, visible=None, select_rows=None, alternating_row_color=None, row_colors=None):
        """
        Changes some of the settings for the Table Element. Must call `Window.Read` or `Window.Finalize` prior

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param values:                A new 2-dimensional table to show
        :type values:                 List[List[str | int | float]]
        :param num_rows:              How many rows to display at a time
        :type num_rows:               (int)
        :param visible:               if True then will be visible
        :type visible:                (bool)
        :param select_rows:           List of rows to select as if user did
        :type select_rows:            List[int]
        :param alternating_row_color: the color to make every other row
        :type alternating_row_color:  (str)
        :param row_colors:            list of tuples of (row, background color) OR (row, foreground color, background color). Changes the colors of listed rows to the color(s) provided (note the optional foreground color)
        :type row_colors:             List[Tuple[int, str] | Tuple[Int, str, str]]
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Table.update - The window was closed')
            return

        if values is not None:
            for id in self.tree_ids:
                self.TKTreeview.item(id, tags=())
                if self.BackgroundColor is not None and self.BackgroundColor != COLOR_SYSTEM_DEFAULT:
                    self.TKTreeview.tag_configure(id, background=self.BackgroundColor)
                else:
                    self.TKTreeview.tag_configure(id, background='#FFFFFF', foreground='#000000')
                if self.TextColor is not None and self.TextColor != COLOR_SYSTEM_DEFAULT:
                    self.TKTreeview.tag_configure(id, foreground=self.TextColor)
                else:
                    self.TKTreeview.tag_configure(id, foreground='#000000')

            children = self.TKTreeview.get_children()
            for i in children:
                self.TKTreeview.detach(i)
                self.TKTreeview.delete(i)
            children = self.TKTreeview.get_children()

            self.tree_ids = []
            for i, value in enumerate(values):
                if self.DisplayRowNumbers:
                    value = [i + self.StartingRowNumber] + value
                id = self.TKTreeview.insert('', 'end', text=value, iid=i + 1, values=value, tag=i)
                if self.BackgroundColor is not None and self.BackgroundColor != COLOR_SYSTEM_DEFAULT:
                    self.TKTreeview.tag_configure(id, background=self.BackgroundColor)
                else:
                    self.TKTreeview.tag_configure(id, background='#FFFFFF')
                self.tree_ids.append(id)
            self.Values = values
            self.SelectedRows = []
        if visible is False:
            self._pack_forget_save_settings(self.element_frame)
        elif visible is True:
            self._pack_restore_settings(self.element_frame)

        if num_rows is not None:
            self.TKTreeview.config(height=num_rows)
        if select_rows is not None:
            rows_to_select = [i + 1 for i in select_rows]
            self.TKTreeview.selection_set(rows_to_select)

        if alternating_row_color is not None:  # alternating colors
            self.AlternatingRowColor = alternating_row_color

        if self.AlternatingRowColor is not None:
            for row in range(0, len(self.Values), 2):
                self.TKTreeview.tag_configure(row, background=self.AlternatingRowColor)
        if row_colors is not None:  # individual row colors
            self.RowColors = row_colors
            for row_def in self.RowColors:
                if len(row_def) == 2:  # only background is specified
                    self.TKTreeview.tag_configure(row_def[0], background=row_def[1])
                else:
                    self.TKTreeview.tag_configure(row_def[0], background=row_def[2], foreground=row_def[1])
        if visible is not None:
            self._visible = visible

    def _treeview_selected(self, event):
        """
        Not user callable.  Callback function that is called when something is selected from Table.
        Stores the selected rows in Element as they are being selected. If events enabled, then returns from Read

        :param event: event information from tkinter
        :type event:  (unknown)
        """
        # print('**-- in treeview selected --**')
        selections = self.TKTreeview.selection()
        self.SelectedRows = [int(x) - 1 for x in selections]
        if self.ChangeSubmits:
            if self.Key is not None:
                self.ParentForm.LastButtonClicked = self.Key
            else:
                self.ParentForm.LastButtonClicked = ''
            self.ParentForm.FormRemainedOpen = True
            _exit_mainloop(self.ParentForm)

    def _treeview_double_click(self, event):
        """
        Not user callable.  Callback function that is called when something is selected from Table.
        Stores the selected rows in Element as they are being selected. If events enabled, then returns from Read

        :param event: event information from tkinter
        :type event:  (unknown)
        """
        selections = self.TKTreeview.selection()
        self.SelectedRows = [int(x) - 1 for x in selections]
        if self.BindReturnKey:  # Signifies BOTH a return key AND a double click
            if self.Key is not None:
                self.ParentForm.LastButtonClicked = self.Key
            else:
                self.ParentForm.LastButtonClicked = ''
            self.ParentForm.FormRemainedOpen = True
            _exit_mainloop(self.ParentForm)

    def _table_clicked(self, event):
        """
        Not user callable.  Callback function that is called a click happens on a table.
        Stores the selected rows in Element as they are being selected. If events enabled, then returns from Read

        :param event: event information from tkinter
        :type event:  (unknown)
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return
        # popup(obj_to_string_single_obj(event))
        try:
            region = self.Widget.identify('region', event.x, event.y)
            if region == 'heading':
                row = -1
            elif region == 'cell':
                row = int(self.Widget.identify_row(event.y)) - 1
            elif region == 'separator':
                row = None
            else:
                row = None
            col_identified = self.Widget.identify_column(event.x)
            if col_identified:  # Sometimes tkinter returns a value of '' which would cause an error if cast to an int
                column = int(self.Widget.identify_column(event.x)[1:]) - 1 - int(self.DisplayRowNumbers is True)
            else:
                column = None
        except Exception as e:
            warnings.warn(f'Error getting table click data for table with key= {self.Key}\nError: {e}', UserWarning)
            if not FreeSimpleGUI.SUPPRESS_ERROR_POPUPS:
                _error_popup_with_traceback(
                    f'Unable to complete operation getting the clicked event for table with key {self.Key}',
                    _create_error_message(),
                    e,
                    'Event data:',
                    obj_to_string_single_obj(event),
                )
            row = column = None

        self.last_clicked_position = (row, column)

        # update the rows being selected if appropriate
        self.ParentForm.TKroot.update()
        # self.TKTreeview.()
        selections = self.TKTreeview.selection()
        if self.right_click_selects and len(selections) <= 1:
            if (event.num == 3 and not running_mac()) or (event.num == 2 and running_mac()):
                if row != -1 and row is not None:
                    selections = [row + 1]
                    self.TKTreeview.selection_set(selections)
        # print(selections)
        self.SelectedRows = [int(x) - 1 for x in selections]
        # print('The new selected rows = ', self.SelectedRows, 'selections =', selections)
        if self.enable_click_events is True:
            if self.Key is not None:
                self.ParentForm.LastButtonClicked = (self.Key, TABLE_CLICKED_INDICATOR, (row, column))
            else:
                self.ParentForm.LastButtonClicked = ''
            self.ParentForm.FormRemainedOpen = True
            _exit_mainloop(self.ParentForm)

    def get(self):
        """
        Get the selected rows using tktiner's selection method.  Returns a list of the selected rows.

        :return: a list of the index of the selected rows (a list of ints)
        :rtype:  List[int]
        """

        selections = self.TKTreeview.selection()
        selected_rows = [int(x) - 1 for x in selections]
        return selected_rows

    def get_last_clicked_position(self):
        """
        Returns a tuple with the row and column of the cell that was last clicked.
        Headers will have a row == -1 and the Row Number Column (if present) will have a column == -1
        :return: The (row,col) position of the last cell clicked in the table
        :rtype:  (int | None, int | None)
        """
        return self.last_clicked_position

    Update = update
    Get = get
