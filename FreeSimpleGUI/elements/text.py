from __future__ import annotations

import tkinter.font

import FreeSimpleGUI
from FreeSimpleGUI import _get_hidden_master_root
from FreeSimpleGUI import COLOR_SYSTEM_DEFAULT
from FreeSimpleGUI import ELEM_TYPE_TEXT
from FreeSimpleGUI._utils import _error_popup_with_traceback
from FreeSimpleGUI.elements.base import Element


class Text(Element):
    """
    Text - Display some text in the window.  Usually this means a single line of text.  However, the text can also be multiple lines.  If multi-lined there are no scroll bars.
    """

    def __init__(
        self,
        text='',
        size=(None, None),
        s=(None, None),
        auto_size_text=None,
        click_submits=False,
        enable_events=False,
        relief=None,
        font=None,
        text_color=None,
        background_color=None,
        border_width=None,
        justification=None,
        pad=None,
        p=None,
        key=None,
        k=None,
        right_click_menu=None,
        expand_x=False,
        expand_y=False,
        grab=None,
        tooltip=None,
        visible=True,
        metadata=None,
    ):
        """
        :param text:             The text to display. Can include /n to achieve multiple lines.  Will convert (optional) parameter into a string
        :type text:              Any
        :param size:             (w, h) w=characters-wide, h=rows-high. If an int instead of a tuple is supplied, then height is auto-set to 1
        :type size:              (int, int) |  (int, None) | (None, None) | (int, ) | int
        :param s:                Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                 (int, int) |  (int, None) | (None, None) | (int, ) | int
        :param auto_size_text:   if True size of the Text Element will be sized to fit the string provided in 'text' parm
        :type auto_size_text:    (bool)
        :param click_submits:    DO NOT USE. Only listed for backwards compat - Use enable_events instead
        :type click_submits:     (bool)
        :param enable_events:    Turns on the element specific events. Text events happen when the text is clicked
        :type enable_events:     (bool)
        :param relief:           relief style around the text. Values are same as progress meter relief values. Should be a constant that is defined at starting with RELIEF - RELIEF_RAISED, RELIEF_SUNKEN, RELIEF_FLAT, RELIEF_RIDGE, RELIEF_GROOVE, RELIEF_SOLID
        :type relief:            (str)
        :param font:             specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:              (str or (str, int[, str]) or None)
        :param text_color:       color of the text
        :type text_color:        (str)
        :param background_color: color of background
        :type background_color:  (str)
        :param border_width:     number of pixels for the border (if using a relief)
        :type border_width:      (int)
        :param justification:    how string should be aligned within space provided by size. Valid choices = `left`, `right`, `center`
        :type justification:     (str)
        :param pad:              Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:               (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                 (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param key:              Used with window.find_element and with return values to uniquely identify this element to uniquely identify this element
        :type key:               str or int or tuple or object
        :param k:                Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                 str | int | tuple | object
        :param right_click_menu: A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type right_click_menu:  List[List[ List[str] | str ]]
        :param expand_x:         If True the element will automatically expand in the X direction to fill available space
        :type expand_x:          (bool)
        :param expand_y:         If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:          (bool)
        :param grab:             If True can grab this element and move the window around. Default is False
        :type grab:              (bool)
        :param tooltip:          text, that will appear when mouse hovers over the element
        :type tooltip:           (str)
        :param visible:          set visibility state of the element
        :type visible:           (bool)
        :param metadata:         User metadata that can be set to ANYTHING
        :type metadata:          (Any)
        """

        self.DisplayText = str(text)
        self.TextColor = text_color if text_color else FreeSimpleGUI.DEFAULT_TEXT_COLOR
        self.Justification = justification
        self.Relief = relief
        self.ClickSubmits = click_submits or enable_events
        if background_color is None:
            bg = FreeSimpleGUI.DEFAULT_TEXT_ELEMENT_BACKGROUND_COLOR
        else:
            bg = background_color
        self.RightClickMenu = right_click_menu
        self.TKRightClickMenu = None
        self.BorderWidth = border_width
        self.Grab = grab
        key = key if key is not None else k
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y

        super().__init__(
            ELEM_TYPE_TEXT,
            auto_size_text=auto_size_text,
            size=sz,
            background_color=bg,
            font=font if font else FreeSimpleGUI.DEFAULT_FONT,
            text_color=self.TextColor,
            pad=pad,
            key=key,
            tooltip=tooltip,
            visible=visible,
            metadata=metadata,
        )

    def update(self, value=None, background_color=None, text_color=None, font=None, visible=None):
        """
        Changes some of the settings for the Text Element. Must call `Window.Read` or `Window.Finalize` prior

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param value:            new text to show
        :type value:             (Any)
        :param background_color: color of background
        :type background_color:  (str)
        :param text_color:       color of the text
        :type text_color:        (str)
        :param font:             specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:              (str or (str, int[, str]) or None)
        :param visible:          set visibility state of the element
        :type visible:           (bool)
        """

        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Text.update - The window was closed')
            return

        if value is not None:
            self.DisplayText = str(value)
            self.TKStringVar.set(str(value))
        if background_color not in (None, COLOR_SYSTEM_DEFAULT):
            self.TKText.configure(background=background_color)
        if text_color not in (None, COLOR_SYSTEM_DEFAULT):
            self.TKText.configure(fg=text_color)
        if font is not None:
            self.TKText.configure(font=font)
        if visible is False:
            self._pack_forget_save_settings()
        elif visible is True:
            self._pack_restore_settings()
        if visible is not None:
            self._visible = visible

    def get(self):
        """
        Gets the current value of the displayed text

        :return: The current value
        :rtype:  (str)
        """
        try:
            text = self.TKStringVar.get()
        except:
            text = ''
        return text

    @classmethod
    def fonts_installed_list(cls):
        """
        Returns a list of strings that tkinter reports as the installed fonts

        :return:          List of the installed font names
        :rtype:           List[str]
        """
        # A window must exist before can perform this operation. Create the hidden master root if it doesn't exist
        _get_hidden_master_root()

        fonts = list(tkinter.font.families())
        fonts.sort()

        return fonts

    @classmethod
    def char_width_in_pixels(cls, font, character='W'):
        """
        Get the with of the character "W" in pixels for the font being passed in or
        the character of your choosing if "W" is not a good representative character.
        Cannot be used until a window has been created.
        If an error occurs, 0 will be returned
        :param font:      specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike, to be measured
        :type font:       (str or (str, int[, str]) or None)
        :param character: specifies a SINGLE CHARACTER character to measure
        :type character:  (str)
        :return:          Width in pixels of "A"
        :rtype:           (int)
        """
        # A window must exist before can perform this operation. Create the hidden master root if it doesn't exist
        _get_hidden_master_root()

        size = 0
        try:
            size = tkinter.font.Font(font=font).measure(character)  # single character width
        except Exception as e:
            _error_popup_with_traceback('Exception retrieving char width in pixels', e)

        return size

    @classmethod
    def char_height_in_pixels(cls, font):
        """
        Get the height of a string if using the supplied font in pixels.
        Cannot be used until a window has been created.
        If an error occurs, 0 will be returned
        :param font: specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike, to be measured
        :type font:  (str or (str, int[, str]) or None)
        :return:     Height in pixels of "A"
        :rtype:      (int)
        """

        # A window must exist before can perform this operation. Create the hidden master root if it doesn't exist
        _get_hidden_master_root()

        size = 0
        try:
            size = tkinter.font.Font(font=font).metrics('linespace')
        except Exception as e:
            _error_popup_with_traceback('Exception retrieving char height in pixels', e)

        return size

    @classmethod
    def string_width_in_pixels(cls, font, string):
        """
        Get the with of the supplied string in pixels for the font being passed in.
        If an error occurs, 0 will be returned
        :param font:   specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike, to be measured
        :type font:    (str or (str, int[, str]) or None)
        :param string: the string to measure
        :type string:  str
        :return:       Width in pixels of string
        :rtype:        (int)
        """

        # A window must exist before can perform this operation. Create the hidden master root if it doesn't exist
        _get_hidden_master_root()

        size = 0
        try:
            size = tkinter.font.Font(font=font).measure(string)  # string's  width
        except Exception as e:
            _error_popup_with_traceback('Exception retrieving string width in pixels', e)

        return size

    def _print_to_element(
        self,
        *args,
        end=None,
        sep=None,
        text_color=None,
        background_color=None,
        autoscroll=None,
        justification=None,
        font=None,
        append=None,
    ):
        """
        Print like Python normally prints except route the output to a multiline element and also add colors if desired

        :param multiline_element: The multiline element to be output to
        :type multiline_element:  (Multiline)
        :param args:              The arguments to print
        :type args:               List[Any]
        :param end:               The end char to use just like print uses
        :type end:                (str)
        :param sep:               The separation character like print uses
        :type sep:                (str)
        :param text_color:        color of the text
        :type text_color:         (str)
        :param background_color:  The background color of the line
        :type background_color:   (str)
        :param autoscroll:        If True (the default), the element will scroll to bottom after updating
        :type autoscroll:         (bool)
        :param font:              specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike for the value being updated
        :type font:               str | (str, int)
        """
        end_str = str(end) if end is not None else '\n'
        sep_str = str(sep) if sep is not None else ' '

        outstring = ''
        num_args = len(args)
        for i, arg in enumerate(args):
            outstring += str(arg)
            if i != num_args - 1:
                outstring += sep_str
        outstring += end_str
        if append:
            outstring = self.get() + outstring

        self.update(outstring, text_color=text_color, background_color=background_color, font=font)

        try:  # if the element is set to autorefresh, then refresh the parent window
            if self.AutoRefresh:
                self.ParentForm.refresh()
        except:
            pass

    def print(
        self,
        *args,
        end=None,
        sep=None,
        text_color=None,
        background_color=None,
        justification=None,
        font=None,
        colors=None,
        t=None,
        b=None,
        c=None,
        autoscroll=True,
        append=True,
    ):
        """
        Print like Python normally prints except route the output to a multiline element and also add colors if desired

        colors -(str, str) or str.  A combined text/background color definition in a single parameter

        There are also "aliases" for text_color, background_color and colors (t, b, c)
        t - An alias for color of the text (makes for shorter calls)
        b - An alias for the background_color parameter
        c - (str, str) - "shorthand" way of specifying color. (foreground, backgrouned)
        c - str - can also be a string of the format "foreground on background"  ("white on red")

        With the aliases it's possible to write the same print but in more compact ways:
        cprint('This will print white text on red background', c=('white', 'red'))
        cprint('This will print white text on red background', c='white on red')
        cprint('This will print white text on red background', text_color='white', background_color='red')
        cprint('This will print white text on red background', t='white', b='red')

        :param args:             The arguments to print
        :type args:              (Any)
        :param end:              The end char to use just like print uses
        :type end:               (str)
        :param sep:              The separation character like print uses
        :type sep:               (str)
        :param text_color:       The color of the text
        :type text_color:        (str)
        :param background_color: The background color of the line
        :type background_color:  (str)
        :param justification:    text justification. left, right, center. Can use single characters l, r, c. Sets only for this value, not entire element
        :type justification:     (str)
        :param font:             specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike for the args being printed
        :type font:              (str or (str, int[, str]) or None)
        :param colors:           Either a tuple or a string that has both the text and background colors. Or just the text color
        :type colors:            (str) or (str, str)
        :param t:                Color of the text
        :type t:                 (str)
        :param b:                The background color of the line
        :type b:                 (str)
        :param c:                Either a tuple or a string that has both the text and background colors or just tex color (same as the color parm)
        :type c:                 (str) or (str, str)
        :param autoscroll:       If True the contents of the element will automatically scroll as more data added to the end
        :type autoscroll:        (bool)
        """

        kw_text_color = text_color or t
        kw_background_color = background_color or b
        dual_color = colors or c
        try:
            if isinstance(dual_color, tuple):
                kw_text_color = dual_color[0]
                kw_background_color = dual_color[1]
            elif isinstance(dual_color, str):
                if ' on ' in dual_color:  # if has "on" in the string, then have both text and background
                    kw_text_color = dual_color.split(' on ')[0]
                    kw_background_color = dual_color.split(' on ')[1]
                else:  # if no "on" then assume the color string is just the text color
                    kw_text_color = dual_color
        except Exception as e:
            print('* multiline print warning * you messed up with color formatting', e)

        self._print_to_element(
            *args,
            end=end,
            sep=sep,
            text_color=kw_text_color,
            background_color=kw_background_color,
            justification=justification,
            autoscroll=autoscroll,
            font=font,
            append=append,
        )

    Get = get
    Update = update
