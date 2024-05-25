from __future__ import annotations

import tkinter as tk


def AddMenuItem(top_menu, sub_menu_info, element, is_sub_menu=False, skip=False, right_click_menu=False):
    """
    Only to be used internally. Not user callable
    :param top_menu:      ???
    :type top_menu:       ???
    :param sub_menu_info: ???
    :type sub_menu_info:
    :param element:       ???
    :type element:        idk_yetReally
    :param is_sub_menu:   (Default = False)
    :type is_sub_menu:    (bool)
    :param skip:          (Default = False)
    :type skip:           (bool)

    """
    return_val = None
    if type(sub_menu_info) is str:
        if not is_sub_menu and not skip:
            pos = sub_menu_info.find(MENU_SHORTCUT_CHARACTER)
            if pos != -1:
                if pos < len(MENU_SHORTCUT_CHARACTER) or sub_menu_info[pos - len(MENU_SHORTCUT_CHARACTER)] != '\\':
                    sub_menu_info = sub_menu_info[:pos] + sub_menu_info[pos + len(MENU_SHORTCUT_CHARACTER) :]
            if sub_menu_info == '---':
                top_menu.add('separator')
            else:
                try:
                    item_without_key = sub_menu_info[: sub_menu_info.index(MENU_KEY_SEPARATOR)]
                except:
                    item_without_key = sub_menu_info

                if item_without_key[0] == MENU_DISABLED_CHARACTER:
                    top_menu.add_command(
                        label=item_without_key[len(MENU_DISABLED_CHARACTER) :],
                        underline=pos - 1,
                        command=lambda: element._MenuItemChosenCallback(sub_menu_info),
                    )
                    top_menu.entryconfig(item_without_key[len(MENU_DISABLED_CHARACTER) :], state='disabled')
                else:
                    top_menu.add_command(
                        label=item_without_key,
                        underline=pos,
                        command=lambda: element._MenuItemChosenCallback(sub_menu_info),
                    )
    else:
        i = 0
        while i < (len(sub_menu_info)):
            item = sub_menu_info[i]
            if i != len(sub_menu_info) - 1:
                if type(sub_menu_info[i + 1]) is list:
                    new_menu = tk.Menu(top_menu, tearoff=element.Tearoff)
                    # if a right click menu, then get styling from the top-level window
                    if right_click_menu:
                        window = element.ParentForm
                        if window.right_click_menu_background_color not in (COLOR_SYSTEM_DEFAULT, None):
                            new_menu.config(bg=window.right_click_menu_background_color)
                            new_menu.config(activeforeground=window.right_click_menu_background_color)
                        if window.right_click_menu_text_color not in (COLOR_SYSTEM_DEFAULT, None):
                            new_menu.config(fg=window.right_click_menu_text_color)
                            new_menu.config(activebackground=window.right_click_menu_text_color)
                        if window.right_click_menu_disabled_text_color not in (COLOR_SYSTEM_DEFAULT, None):
                            new_menu.config(disabledforeground=window.right_click_menu_disabled_text_color)
                        if window.right_click_menu_font is not None:
                            new_menu.config(font=window.right_click_menu_font)
                    else:
                        if element.Font is not None:
                            new_menu.config(font=element.Font)
                        if element.BackgroundColor not in (COLOR_SYSTEM_DEFAULT, None):
                            new_menu.config(bg=element.BackgroundColor)
                            new_menu.config(activeforeground=element.BackgroundColor)
                        if element.TextColor not in (COLOR_SYSTEM_DEFAULT, None):
                            new_menu.config(fg=element.TextColor)
                            new_menu.config(activebackground=element.TextColor)
                        if element.DisabledTextColor not in (COLOR_SYSTEM_DEFAULT, None):
                            new_menu.config(disabledforeground=element.DisabledTextColor)
                        if element.ItemFont is not None:
                            new_menu.config(font=element.ItemFont)
                    return_val = new_menu
                    pos = sub_menu_info[i].find(MENU_SHORTCUT_CHARACTER)
                    if pos != -1:
                        if pos < len(MENU_SHORTCUT_CHARACTER) or sub_menu_info[i][pos - len(MENU_SHORTCUT_CHARACTER)] != '\\':
                            sub_menu_info[i] = sub_menu_info[i][:pos] + sub_menu_info[i][pos + len(MENU_SHORTCUT_CHARACTER) :]
                    if sub_menu_info[i][0] == MENU_DISABLED_CHARACTER:
                        top_menu.add_cascade(
                            label=sub_menu_info[i][len(MENU_DISABLED_CHARACTER) :],
                            menu=new_menu,
                            underline=pos,
                            state='disabled',
                        )
                    else:
                        top_menu.add_cascade(label=sub_menu_info[i], menu=new_menu, underline=pos)
                    AddMenuItem(new_menu, sub_menu_info[i + 1], element, is_sub_menu=True, right_click_menu=right_click_menu)
                    i += 1  # skip the next one
                else:
                    AddMenuItem(top_menu, item, element, right_click_menu=right_click_menu)
            else:
                AddMenuItem(top_menu, item, element, right_click_menu=right_click_menu)
            i += 1
    return return_val


def button_color_to_tuple(color_tuple_or_string, default=(None, None)):
    """
    Convert a color tuple or color string into 2 components and returns them as a tuple
    (Text Color, Button Background Color)
    If None is passed in as the first parameter, then the theme's button color is
    returned

    :param color_tuple_or_string: Button color - tuple or a simplied color string with word "on" between color
    :type  color_tuple_or_string: str | (str, str)
    :param default:               The 2 colors to use if there is a problem. Otherwise defaults to the theme's button color
    :type  default:               (str, str)
    :return:                      (str | (str, str)
    :rtype:                       str | (str, str)
    """
    if default == (None, None):
        color_tuple = _simplified_dual_color_to_tuple(color_tuple_or_string, default=theme_button_color())
    elif color_tuple_or_string == COLOR_SYSTEM_DEFAULT:
        color_tuple = (COLOR_SYSTEM_DEFAULT, COLOR_SYSTEM_DEFAULT)
    else:
        color_tuple = _simplified_dual_color_to_tuple(color_tuple_or_string, default=default)

    return color_tuple


def _simplified_dual_color_to_tuple(color_tuple_or_string, default=(None, None)):
    """
    Convert a color tuple or color string into 2 components and returns them as a tuple
    (Text Color, Button Background Color)
    If None is passed in as the first parameter, theme_

    :param color_tuple_or_string: Button color - tuple or a simplied color string with word "on" between color
    :type  color_tuple_or_string: str | (str, str} | (None, None)
    :param default:               The 2 colors to use if there is a problem. Otherwise defaults to the theme's button color
    :type  default:               (str, str)
    :return:                      (str | (str, str)
    :rtype:                       str | (str, str)
    """
    if color_tuple_or_string is None or color_tuple_or_string == (None, None):
        color_tuple_or_string = default
    if color_tuple_or_string == COLOR_SYSTEM_DEFAULT:
        return (COLOR_SYSTEM_DEFAULT, COLOR_SYSTEM_DEFAULT)
    text_color = background_color = COLOR_SYSTEM_DEFAULT
    try:
        if isinstance(color_tuple_or_string, (tuple, list)):
            if len(color_tuple_or_string) >= 2:
                text_color = color_tuple_or_string[0] or default[0]
                background_color = color_tuple_or_string[1] or default[1]
            elif len(color_tuple_or_string) == 1:
                background_color = color_tuple_or_string[0] or default[1]
        elif isinstance(color_tuple_or_string, str):
            color_tuple_or_string = color_tuple_or_string.lower()
            split_colors = color_tuple_or_string.split(' on ')
            if len(split_colors) >= 2:
                text_color = split_colors[0].strip() or default[0]
                background_color = split_colors[1].strip() or default[1]
            elif len(split_colors) == 1:
                split_colors = color_tuple_or_string.split('on')
                if len(split_colors) == 1:
                    text_color, background_color = default[0], split_colors[0].strip()
                else:
                    split_colors = split_colors[0].strip(), split_colors[1].strip()
                    text_color = split_colors[0] or default[0]
                    background_color = split_colors[1] or default[1]
                    # text_color, background_color = color_tuple_or_string, default[1]
            else:
                text_color, background_color = default
        else:
            if not SUPPRESS_ERROR_POPUPS:
                _error_popup_with_traceback('** Badly formatted dual-color... not a tuple nor string **', color_tuple_or_string)
            else:
                print('** Badly formatted dual-color... not a tuple nor string **', color_tuple_or_string)
            text_color, background_color = default
    except Exception as e:
        if not SUPPRESS_ERROR_POPUPS:
            _error_popup_with_traceback('** Badly formatted button color **', color_tuple_or_string, e)
        else:
            print('** Badly formatted button color... not a tuple nor string **', color_tuple_or_string, e)
        text_color, background_color = default
    if isinstance(text_color, int):
        text_color = '#%06X' % text_color
    if isinstance(background_color, int):
        background_color = '#%06X' % background_color
    # print('converted button color', color_tuple_or_string, 'to', (text_color, background_color))

    return (text_color, background_color)


from FreeSimpleGUI._utils import _error_popup_with_traceback
from FreeSimpleGUI import COLOR_SYSTEM_DEFAULT
from FreeSimpleGUI import MENU_DISABLED_CHARACTER
from FreeSimpleGUI import MENU_KEY_SEPARATOR
from FreeSimpleGUI import MENU_SHORTCUT_CHARACTER
from FreeSimpleGUI import SUPPRESS_ERROR_POPUPS
from FreeSimpleGUI import theme_button_color
