from __future__ import annotations

import copy
import tkinter as tk

from FreeSimpleGUI import COLOR_SYSTEM_DEFAULT
from FreeSimpleGUI import ELEM_TYPE_MENUBAR
from FreeSimpleGUI import MENU_DISABLED_CHARACTER
from FreeSimpleGUI import MENU_SHORTCUT_CHARACTER
from FreeSimpleGUI import theme_input_background_color
from FreeSimpleGUI import theme_input_text_color
from FreeSimpleGUI._utils import _error_popup_with_traceback
from FreeSimpleGUI._utils import _exit_mainloop
from FreeSimpleGUI.elements.base import Element
from FreeSimpleGUI.elements.helpers import AddMenuItem


class Menu(Element):
    """
    Menu Element is the Element that provides a Menu Bar that goes across the top of the window, just below titlebar.
    Here is an example layout.  The "&" are shortcut keys ALT+key.
    Is a List of -  "Item String" + List
    Where Item String is what will be displayed on the Menubar itself.
    The List that follows the item represents the items that are shown then Menu item is clicked
    Notice how an "entry" in a mennu can be a list which means it branches out and shows another menu, etc. (resursive)
    menu_def = [['&File', ['!&Open', '&Save::savekey', '---', '&Properties', 'E&xit']],
                ['!&Edit', ['!&Paste', ['Special', 'Normal', ], 'Undo'], ],
                ['&Debugger', ['Popout', 'Launch Debugger']],
                ['&Toolbar', ['Command &1', 'Command &2', 'Command &3', 'Command &4']],
                ['&Help', '&About...'], ]
    Important Note!  The colors, font, look of the Menubar itself cannot be changed, only the menus shown AFTER clicking the menubar
    can be changed.  If you want to change the style/colors the Menubar, then you will have to use the MenubarCustom element.
    Finally, "keys" can be added to entries so make them unique.  The "Save" entry has a key associated with it. You
    can see it has a "::" which signifies the beginning of a key.  The user will not see the key portion when the
    menu is shown.  The key portion is returned as part of the event.
    """

    def __init__(
        self,
        menu_definition,
        background_color=None,
        text_color=None,
        disabled_text_color=None,
        size=(None, None),
        s=(None, None),
        tearoff=False,
        font=None,
        pad=None,
        p=None,
        key=None,
        k=None,
        visible=True,
        metadata=None,
    ):
        """
        :param menu_definition:           The Menu definition specified using lists (docs explain the format)
        :type menu_definition:            List[List[Tuple[str, List[str]]]
        :param background_color:          color of the background of menus, NOT the Menubar
        :type background_color:           (str)
        :param text_color:                text color for menus, NOT the Menubar. Can be in #RRGGBB format or a color name "black".
        :type text_color:                 (str)
        :param disabled_text_color:       color to use for text when item in submenu, not the menubar itself, is disabled. Can be in #RRGGBB format or a color name "black"
        :type disabled_text_color:        (str)
        :param size:                      Not used in the tkinter port
        :type size:                       (int, int)
        :param s:                         Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                          (int, int)  | (None, None)
        :param tearoff:                   if True, then can tear the menu off from the window ans use as a floating window. Very cool effect
        :type tearoff:                    (bool)
        :param pad:                       Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:                        (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                         Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                          (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param font:                      specifies the  font family, size, etc. of submenus. Does NOT apply to the Menubar itself. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:                       (str or (str, int[, str]) or None)
        :param key:                       Value that uniquely identifies this element from all other elements. Used when Finding an element or in return values. Must be unique to the window
        :type key:                        str | int | tuple | object
        :param k:                         Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                          str | int | tuple | object
        :param visible:                   set visibility state of the element
        :type visible:                    (bool)
        :param metadata:                  User metadata that can be set to ANYTHING
        :type metadata:                   (Any)
        """

        self.BackgroundColor = background_color if background_color is not None else theme_input_background_color()
        self.TextColor = text_color if text_color is not None else theme_input_text_color()

        self.DisabledTextColor = disabled_text_color if disabled_text_color is not None else COLOR_SYSTEM_DEFAULT
        self.MenuDefinition = copy.deepcopy(menu_definition)
        self.Widget = self.TKMenu = None  # type: tk.Menu
        self.MenuItemChosen = None
        key = key if key is not None else k
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p

        super().__init__(
            ELEM_TYPE_MENUBAR,
            background_color=self.BackgroundColor,
            text_color=self.TextColor,
            size=sz,
            pad=pad,
            key=key,
            visible=visible,
            font=font,
            metadata=metadata,
        )
        # super().__init__(ELEM_TYPE_MENUBAR, background_color=COLOR_SYSTEM_DEFAULT, text_color=COLOR_SYSTEM_DEFAULT, size=sz, pad=pad, key=key, visible=visible, font=None, metadata=metadata)

        self.Tearoff = tearoff

        return

    def _MenuItemChosenCallback(self, item_chosen):  # Menu Menu Item Chosen Callback
        """
        Not user callable.  Called when some end-point on the menu (an item) has been clicked.  Send the information back to the application as an event.  Before event can be sent

        :param item_chosen: the text that was clicked on / chosen from the menu
        :type item_chosen:  (str)
        """
        # print('IN MENU ITEM CALLBACK', item_chosen)
        self.MenuItemChosen = item_chosen
        self.ParentForm.LastButtonClicked = item_chosen
        self.ParentForm.FormRemainedOpen = True
        _exit_mainloop(self.ParentForm)

    def update(self, menu_definition=None, visible=None):
        """
        Update a menubar - can change the menu definition and visibility.  The entire menu has to be specified

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param menu_definition: The menu definition list
        :type menu_definition:  List[List[Tuple[str, List[str]]]
        :param visible:         control visibility of element
        :type visible:          (bool)
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Menu.update - The window was closed')
            return

        if menu_definition is not None:
            self.MenuDefinition = copy.deepcopy(menu_definition)
            if self.TKMenu is None:  # if no menu exists, make one
                self.TKMenu = tk.Menu(self.ParentForm.TKroot, tearoff=self.Tearoff, tearoffcommand=self._tearoff_menu_callback)  # create the menubar
            menubar = self.TKMenu
            # Delete all the menu items (assuming 10000 should be a high enough number to cover them all)
            menubar.delete(0, 10000)
            self.Widget = self.TKMenu  # same the new menu so user can access to extend PySimpleGUI
            for menu_entry in self.MenuDefinition:
                baritem = tk.Menu(menubar, tearoff=self.Tearoff, tearoffcommand=self._tearoff_menu_callback)

                if self.BackgroundColor not in (COLOR_SYSTEM_DEFAULT, None):
                    baritem.config(bg=self.BackgroundColor)
                if self.TextColor not in (COLOR_SYSTEM_DEFAULT, None):
                    baritem.config(fg=self.TextColor)
                if self.DisabledTextColor not in (COLOR_SYSTEM_DEFAULT, None):
                    baritem.config(disabledforeground=self.DisabledTextColor)
                if self.Font is not None:
                    baritem.config(font=self.Font)

                if self.Font is not None:
                    baritem.config(font=self.Font)
                pos = menu_entry[0].find(MENU_SHORTCUT_CHARACTER)
                # print(pos)
                if pos != -1:
                    if pos == 0 or menu_entry[0][pos - len(MENU_SHORTCUT_CHARACTER)] != '\\':
                        menu_entry[0] = menu_entry[0][:pos] + menu_entry[0][pos + len(MENU_SHORTCUT_CHARACTER) :]
                if menu_entry[0][0] == MENU_DISABLED_CHARACTER:
                    menubar.add_cascade(label=menu_entry[0][len(MENU_DISABLED_CHARACTER) :], menu=baritem, underline=pos)
                    menubar.entryconfig(menu_entry[0][len(MENU_DISABLED_CHARACTER) :], state='disabled')
                else:
                    menubar.add_cascade(label=menu_entry[0], menu=baritem, underline=pos)

                if len(menu_entry) > 1:
                    AddMenuItem(baritem, menu_entry[1], self)

        if visible is False:
            self.ParentForm.TKroot.configure(menu=[])  # this will cause the menubar to disappear
        elif self.TKMenu is not None:
            self.ParentForm.TKroot.configure(menu=self.TKMenu)
        if visible is not None:
            self._visible = visible

    Update = update
