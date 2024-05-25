from __future__ import annotations

import sys
import tkinter as tk

import FreeSimpleGUI
from FreeSimpleGUI import _print_to_element
from FreeSimpleGUI import COLOR_SYSTEM_DEFAULT
from FreeSimpleGUI import ELEM_TYPE_INPUT_MULTILINE
from FreeSimpleGUI._utils import _error_popup_with_traceback
from FreeSimpleGUI.elements.base import Element
from FreeSimpleGUI.window import Window


class Multiline(Element):
    """
    Multiline Element - Display and/or read multiple lines of text.  This is both an input and output element.
    Other PySimpleGUI ports have a separate MultilineInput and MultilineOutput elements.  May want to split this
    one up in the future too.
    """

    def __init__(
        self,
        default_text='',
        enter_submits=False,
        disabled=False,
        autoscroll=False,
        autoscroll_only_at_bottom=False,
        border_width=None,
        size=(None, None),
        s=(None, None),
        auto_size_text=None,
        background_color=None,
        text_color=None,
        selected_text_color=None,
        selected_background_color=None,
        horizontal_scroll=False,
        change_submits=False,
        enable_events=False,
        do_not_clear=True,
        key=None,
        k=None,
        write_only=False,
        auto_refresh=False,
        reroute_stdout=False,
        reroute_stderr=False,
        reroute_cprint=False,
        echo_stdout_stderr=False,
        focus=False,
        font=None,
        pad=None,
        p=None,
        tooltip=None,
        justification=None,
        no_scrollbar=False,
        wrap_lines=None,
        sbar_trough_color=None,
        sbar_background_color=None,
        sbar_arrow_color=None,
        sbar_width=None,
        sbar_arrow_width=None,
        sbar_frame_color=None,
        sbar_relief=None,
        expand_x=False,
        expand_y=False,
        rstrip=True,
        right_click_menu=None,
        visible=True,
        metadata=None,
    ):
        """
        :param default_text:                 Initial text to show
        :type default_text:                  (Any)
        :param enter_submits:                if True, the Window.read call will return is enter key is pressed in this element
        :type enter_submits:                 (bool)
        :param disabled:                     set disable state
        :type disabled:                      (bool)
        :param autoscroll:                   If True the contents of the element will automatically scroll as more data added to the end
        :type autoscroll:                    (bool)
        :param autoscroll_only_at_bottom:    If True the contents of the element will automatically scroll only if the scrollbar is at the bottom of the multiline
        :type autoscroll_only_at_bottom:     (bool)
        :param border_width:                 width of border around element in pixels
        :type border_width:                  (int)
        :param size:                         (w, h) w=characters-wide, h=rows-high. If an int instead of a tuple is supplied, then height is auto-set to 1
        :type size:                          (int, int)  | (None, None) | int
        :param s:                            Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                             (int, int)  | (None, None) | int
        :param auto_size_text:               if True will size the element to match the length of the text
        :type auto_size_text:                (bool)
        :param background_color:             color of background
        :type background_color:              (str)
        :param text_color:                   color of the text
        :type text_color:                    (str)
        :param selected_text_color:          Color of text when it is selected (using mouse or control+A, etc)
        :type selected_text_color:           (str)
        :param selected_background_color:    Color of background when it is selected (using mouse or control+A, etc)
        :type selected_background_color:     (str)
        :param horizontal_scroll:            Controls if a horizontal scrollbar should be shown.  If True a horizontal scrollbar will be shown in addition to vertical
        :type horizontal_scroll:             (bool)
        :param change_submits:               DO NOT USE. Only listed for backwards compat - Use enable_events instead
        :type change_submits:                (bool)
        :param enable_events:                If True then any key press that happens when the element has focus will generate an event.
        :type enable_events:                 (bool)
        :param do_not_clear:                 if False the element will be cleared any time the Window.read call returns
        :type do_not_clear:                  (bool)
        :param key:                          Used with window.find_element and with return values to uniquely identify this element to uniquely identify this element
        :type key:                           str | int | tuple | object
        :param k:                            Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                             str | int | tuple | object
        :param write_only:                   If True then no entry will be added to the values dictionary when the window is read
        :type write_only:                    bool
        :param auto_refresh:                 If True then anytime the element is updated, the window will be refreshed so that the change is immediately displayed
        :type auto_refresh:                  (bool)
        :param reroute_stdout:               If True then all output to stdout will be output to this element
        :type reroute_stdout:                (bool)
        :param reroute_stderr:               If True then all output to stderr will be output to this element
        :type reroute_stderr:                (bool)
        :param reroute_cprint:               If True your cprint calls will output to this element. It's the same as you calling cprint_set_output_destination
        :type reroute_cprint:                (bool)
        :param echo_stdout_stderr:           If True then output to stdout and stderr will be output to this element AND also to the normal console location
        :type echo_stdout_stderr:            (bool)
        :param focus:                        if True initial focus will go to this element
        :type focus:                         (bool)
        :param font:                         specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:                          (str or (str, int[, str]) or None)
        :param pad:                          Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:                           (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                            Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                             (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param tooltip:                      text, that will appear when mouse hovers over the element
        :type tooltip:                       (str)
        :param justification:                text justification. left, right, center. Can use single characters l, r, c.
        :type justification:                 (str)
        :param no_scrollbar:                 If False then a vertical scrollbar will be shown (the default)
        :type no_scrollbar:                  (bool)
        :param wrap_lines:                   If True, the lines will be wrapped automatically. Other parms affect this setting, but this one will override them all. Default is it does nothing and uses previous settings for wrapping.
        :type wrap_lines:                    (bool)
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
        :param expand_x:                     If True the element will automatically expand in the X direction to fill available space
        :type expand_x:                      (bool)
        :param expand_y:                     If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:                      (bool)
        :param rstrip:                       If True the value returned in will have whitespace stripped from the right side
        :type rstrip:                        (bool)
        :param right_click_menu:             A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type right_click_menu:              List[List[ List[str] | str ]]
        :param visible:                      set visibility state of the element
        :type visible:                       (bool)
        :param metadata:                     User metadata that can be set to ANYTHING
        :type metadata:                      (Any)
        """

        self.DefaultText = str(default_text)
        self.EnterSubmits = enter_submits
        bg = background_color if background_color else FreeSimpleGUI.DEFAULT_INPUT_ELEMENTS_COLOR
        self.Focus = focus
        self.do_not_clear = do_not_clear
        fg = text_color if text_color is not None else FreeSimpleGUI.DEFAULT_INPUT_TEXT_COLOR
        self.selected_text_color = selected_text_color
        self.selected_background_color = selected_background_color
        self.Autoscroll = autoscroll
        self.Disabled = disabled
        self.ChangeSubmits = change_submits or enable_events
        self.RightClickMenu = right_click_menu
        self.BorderWidth = border_width if border_width is not None else FreeSimpleGUI.DEFAULT_BORDER_WIDTH
        self.TagCounter = 0
        self.TKText = self.Widget = None  # type: tk.Text
        self.element_frame = None  # type: tk.Frame
        self.HorizontalScroll = horizontal_scroll
        self.tags = set()
        self.WriteOnly = write_only
        self.AutoRefresh = auto_refresh
        key = key if key is not None else k
        self.reroute_cprint = reroute_cprint
        self.echo_stdout_stderr = echo_stdout_stderr
        self.Justification = 'left' if justification is None else justification
        self.justification_tag = self.just_center_tag = self.just_left_tag = self.just_right_tag = None
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y
        self.rstrip = rstrip
        self.wrap_lines = wrap_lines
        self.reroute_stdout = reroute_stdout
        self.reroute_stderr = reroute_stderr
        self.no_scrollbar = no_scrollbar
        self.hscrollbar = None  # The horizontal scrollbar
        self.auto_scroll_only_at_bottom = autoscroll_only_at_bottom
        sz = size if size != (None, None) else s

        super().__init__(
            ELEM_TYPE_INPUT_MULTILINE,
            size=sz,
            auto_size_text=auto_size_text,
            background_color=bg,
            text_color=fg,
            key=key,
            pad=pad,
            tooltip=tooltip,
            font=font or FreeSimpleGUI.DEFAULT_FONT,
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

    def update(
        self,
        value=None,
        disabled=None,
        append=False,
        font=None,
        text_color=None,
        background_color=None,
        text_color_for_value=None,
        background_color_for_value=None,
        visible=None,
        autoscroll=None,
        justification=None,
        font_for_value=None,
    ):
        """
        Changes some of the settings for the Multiline Element. Must call `Window.read` or set finalize=True when creating window.

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param value:                      new text to display
        :type value:                       (Any)
        :param disabled:                   disable or enable state of the element
        :type disabled:                    (bool)
        :param append:                     if True then new value will be added onto the end of the current value. if False then contents will be replaced.
        :type append:                      (bool)
        :param font:                       specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike for the entire element
        :type font:                        (str or (str, int[, str]) or None)
        :param text_color:                 color of the text
        :type text_color:                  (str)
        :param background_color:           color of background
        :type background_color:            (str)
        :param text_color_for_value:       color of the new text being added (the value paramter)
        :type text_color_for_value:        (str)
        :param background_color_for_value: color of the new background of the text being added (the value paramter)
        :type background_color_for_value:  (str)
        :param visible:                    set visibility state of the element
        :type visible:                     (bool)
        :param autoscroll:                 if True then contents of element are scrolled down when new text is added to the end
        :type autoscroll:                  (bool)
        :param justification:              text justification. left, right, center. Can use single characters l, r, c. Sets only for this value, not entire element
        :type justification:               (str)
        :param font_for_value:             specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike for the value being updated
        :type font_for_value:              str | (str, int)
        """

        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            # _error_popup_with_traceback('Error in Multiline.update - The window was closed')
            return

        if autoscroll is not None:
            self.Autoscroll = autoscroll
        current_scroll_position = self.TKText.yview()[1]

        if justification is not None:
            if justification.startswith('l'):
                just_tag = 'left'
            if justification.startswith('r'):
                just_tag = 'right'
            if justification.startswith('c'):
                just_tag = 'center'
        else:
            just_tag = self.justification_tag

        tag = None
        if value is not None:
            value = str(value)
            if background_color_for_value is not None or text_color_for_value is not None or font_for_value is not None:
                try:
                    tag = 'Multiline(' + str(text_color_for_value) + ',' + str(background_color_for_value) + ',' + str(font_for_value) + ')'
                    if tag not in self.tags:
                        self.tags.add(tag)
                    if background_color_for_value is not None:
                        self.TKText.tag_configure(tag, background=background_color_for_value)
                    if text_color_for_value is not None:
                        self.TKText.tag_configure(tag, foreground=text_color_for_value)
                    if font_for_value is not None:
                        self.TKText.tag_configure(tag, font=font_for_value)
                except Exception as e:
                    print('* Multiline.update - bad color likely specified:', e)
            if self.Disabled:
                self.TKText.configure(state='normal')
            try:
                if not append:
                    self.TKText.delete('1.0', tk.END)
                if tag is not None or just_tag is not None:
                    self.TKText.insert(tk.END, value, (just_tag, tag))
                else:
                    self.TKText.insert(tk.END, value)
            except Exception as e:
                print('* Error setting multiline *', e)
            if self.Disabled:
                self.TKText.configure(state='disabled')
            self.DefaultText = value

        if self.Autoscroll:
            if not self.auto_scroll_only_at_bottom or (self.auto_scroll_only_at_bottom and current_scroll_position == 1.0):
                self.TKText.see(tk.END)
        if disabled is True:
            self.TKText.configure(state='disabled')
        elif disabled is False:
            self.TKText.configure(state='normal')
        self.Disabled = disabled if disabled is not None else self.Disabled

        if background_color not in (None, COLOR_SYSTEM_DEFAULT):
            self.TKText.configure(background=background_color)
        if text_color not in (None, COLOR_SYSTEM_DEFAULT):
            self.TKText.configure(fg=text_color)
        if font is not None:
            self.TKText.configure(font=font)

        if visible is False:
            self._pack_forget_save_settings(alternate_widget=self.element_frame)
        elif visible is True:
            self._pack_restore_settings(alternate_widget=self.element_frame)

        if self.AutoRefresh and self.ParentForm:
            try:  # in case the window was destroyed
                self.ParentForm.refresh()
            except:
                pass
        if visible is not None:
            self._visible = visible

    def get(self):
        """
        Return current contents of the Multiline Element

        :return: current contents of the Multiline Element (used as an input type of Multiline
        :rtype:  (str)
        """
        value = str(self.TKText.get(1.0, tk.END))
        if self.rstrip:
            return value.rstrip()
        return value

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

        _print_to_element(
            self,
            *args,
            end=end,
            sep=sep,
            text_color=kw_text_color,
            background_color=kw_background_color,
            justification=justification,
            autoscroll=autoscroll,
            font=font,
        )

    def reroute_stdout_to_here(self):
        """
        Sends stdout (prints) to this element
        """
        # if nothing on the stack, then need to save the very first stdout
        if len(Window._rerouted_stdout_stack) == 0:
            Window._original_stdout = sys.stdout
        Window._rerouted_stdout_stack.insert(0, (self.ParentForm, self))
        sys.stdout = self

    def reroute_stderr_to_here(self):
        """
        Sends stderr to this element
        """
        if len(Window._rerouted_stderr_stack) == 0:
            Window._original_stderr = sys.stderr
        Window._rerouted_stderr_stack.insert(0, (self.ParentForm, self))
        sys.stderr = self

    def restore_stdout(self):
        """
        Restore a previously re-reouted stdout back to the original destination
        """
        Window._restore_stdout()

    def restore_stderr(self):
        """
        Restore a previously re-reouted stderr back to the original destination
        """
        Window._restore_stderr()

    def write(self, txt):
        """
        Called by Python (not tkinter?) when stdout or stderr wants to write

        :param txt: text of output
        :type txt:  (str)
        """
        try:
            self.update(txt, append=True)
            # if need to echo, then send the same text to the destinatoin that isn't thesame as this one
            if self.echo_stdout_stderr:
                if sys.stdout != self:
                    sys.stdout.write(txt)
                elif sys.stderr != self:
                    sys.stderr.write(txt)
        except:
            pass

    def flush(self):
        """
        Flush parameter was passed into a print statement.
        For now doing nothing.  Not sure what action should be taken to ensure a flush happens regardless.
        """
        # try:
        #     self.previous_stdout.flush()
        # except:
        #     pass
        return

    def set_ibeam_color(self, ibeam_color=None):
        """
        Sets the color of the I-Beam that is used to "insert" characters. This is oftens called a "Cursor" by
        many users.  To keep from being confused with tkinter's definition of cursor (the mouse pointer), the term
        ibeam is used in this case.
        :param ibeam_color: color to set the "I-Beam" used to indicate where characters will be inserted
        :type ibeam_color:  (str)
        """

        if not self._widget_was_created():
            return
        if ibeam_color is not None:
            try:
                self.Widget.config(insertbackground=ibeam_color)
            except Exception:
                _error_popup_with_traceback(
                    'Error setting I-Beam color in set_ibeam_color',
                    'The element has a key:',
                    self.Key,
                    'The color passed in was:',
                    ibeam_color,
                )

    def __del__(self):
        """
        AT ONE TIME --- If this Widget is deleted, be sure and restore the old stdout, stderr
        Now the restore is done differently. Do not want to RELY on Python to call this method
        in order for stdout and stderr to be restored.  Instead explicit restores are called.

        """

        return

    Get = get
    Update = update


class Output(Multiline):
    """
    Output Element - a multi-lined text area to where stdout, stderr, cprint are rerouted.

    The Output Element is now based on the Multiline Element.  When you make an Output Element, you're
    creating a Multiline Element with some specific settings set:
        auto_refresh = True
        auto_scroll = True
        reroute_stdout = True
        reroute_stderr = True
        reroute_cprint = True
        write_only = True

    If you choose to use a Multiline element to replace an Output element, be sure an turn on the write_only paramter in the Multiline
    so that an item is not included in the values dictionary on every window.read call
    """

    def __init__(
        self,
        size=(None, None),
        s=(None, None),
        background_color=None,
        text_color=None,
        pad=None,
        p=None,
        autoscroll_only_at_bottom=False,
        echo_stdout_stderr=False,
        font=None,
        tooltip=None,
        key=None,
        k=None,
        right_click_menu=None,
        expand_x=False,
        expand_y=False,
        visible=True,
        metadata=None,
        wrap_lines=None,
        horizontal_scroll=None,
        sbar_trough_color=None,
        sbar_background_color=None,
        sbar_arrow_color=None,
        sbar_width=None,
        sbar_arrow_width=None,
        sbar_frame_color=None,
        sbar_relief=None,
    ):
        """
        :param size:                        (w, h) w=characters-wide, h=rows-high. If an int instead of a tuple is supplied, then height is auto-set to 1
        :type size:                         (int, int)  | (None, None) | int
        :param s:                           Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                            (int, int)  | (None, None) | int
        :param background_color:            color of background
        :type background_color:             (str)
        :param text_color:                  color of the text
        :type text_color:                   (str)
        :param pad:                         Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:                          (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                           Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                            (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param autoscroll_only_at_bottom:   If True the contents of the element will automatically scroll only if the scrollbar is at the bottom of the multiline
        :type autoscroll_only_at_bottom:    (bool)
        :param echo_stdout_stderr:          If True then output to stdout will be output to this element AND also to the normal console location
        :type echo_stdout_stderr:           (bool)
        :param font:                        specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:                         (str or (str, int[, str]) or None)
        :param tooltip:                     text, that will appear when mouse hovers over the element
        :type tooltip:                      (str)
        :param key:                         Used with window.find_element and with return values to uniquely identify this element to uniquely identify this element
        :type key:                          str | int | tuple | object
        :param k:                           Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                            str | int | tuple | object
        :param right_click_menu:            A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type right_click_menu:             List[List[ List[str] | str ]]
        :param expand_x:                    If True the element will automatically expand in the X direction to fill available space
        :type expand_x:                     (bool)
        :param expand_y:                    If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:                     (bool)
        :param visible:                     set visibility state of the element
        :type visible:                      (bool)
        :param metadata:                    User metadata that can be set to ANYTHING
        :type metadata:                     (Any)
        :param wrap_lines:                  If True, the lines will be wrapped automatically. Other parms affect this setting, but this one will override them all. Default is it does nothing and uses previous settings for wrapping.
        :type wrap_lines:                   (bool)
        :param horizontal_scroll:           Controls if a horizontal scrollbar should be shown. If True, then line wrapping will be off by default
        :type horizontal_scroll:            (bool)
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

        super().__init__(
            size=size,
            s=s,
            background_color=background_color,
            autoscroll_only_at_bottom=autoscroll_only_at_bottom,
            text_color=text_color,
            pad=pad,
            p=p,
            echo_stdout_stderr=echo_stdout_stderr,
            font=font,
            tooltip=tooltip,
            wrap_lines=wrap_lines,
            horizontal_scroll=horizontal_scroll,
            key=key,
            k=k,
            right_click_menu=right_click_menu,
            write_only=True,
            reroute_stdout=True,
            reroute_stderr=True,
            reroute_cprint=True,
            autoscroll=True,
            auto_refresh=True,
            expand_x=expand_x,
            expand_y=expand_y,
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
