from __future__ import annotations

import tkinter as tk

import FreeSimpleGUI
from FreeSimpleGUI import ELEM_TYPE_INPUT_SLIDER
from FreeSimpleGUI import Element
from FreeSimpleGUI._utils import _error_popup_with_traceback
from FreeSimpleGUI._utils import _exit_mainloop


class Slider(Element):
    """
    A slider, horizontal or vertical
    """

    def __init__(
        self,
        range=(None, None),
        default_value=None,
        resolution=None,
        tick_interval=None,
        orientation=None,
        disable_number_display=False,
        border_width=None,
        relief=None,
        change_submits=False,
        enable_events=False,
        disabled=False,
        size=(None, None),
        s=(None, None),
        font=None,
        background_color=None,
        text_color=None,
        trough_color=None,
        key=None,
        k=None,
        pad=None,
        p=None,
        expand_x=False,
        expand_y=False,
        tooltip=None,
        visible=True,
        metadata=None,
    ):
        """
        :param range:                  slider's range (min value, max value)
        :type range:                   (int, int) | Tuple[float, float]
        :param default_value:          starting value for the slider
        :type default_value:           int | float
        :param resolution:             the smallest amount the slider can be moved
        :type resolution:              int | float
        :param tick_interval:          how often a visible tick should be shown next to slider
        :type tick_interval:           int | float
        :param orientation:            'horizontal' or 'vertical' ('h' or 'v' also work)
        :type orientation:             (str)
        :param disable_number_display: if True no number will be displayed by the Slider Element
        :type disable_number_display:  (bool)
        :param border_width:           width of border around element in pixels
        :type border_width:            (int)
        :param relief:                 relief style. Use constants - RELIEF_RAISED RELIEF_SUNKEN RELIEF_FLAT RELIEF_RIDGE RELIEF_GROOVE RELIEF_SOLID
        :type relief:                  str | None
        :param change_submits:         * DEPRICATED DO NOT USE. Use `enable_events` instead
        :type change_submits:          (bool)
        :param enable_events:          If True then moving the slider will generate an Event
        :type enable_events:           (bool)
        :param disabled:               set disable state for element
        :type disabled:                (bool)
        :param size:                   (l=length chars/rows, w=width pixels)
        :type size:                    (int, int)
        :param s:                      Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                       (int, int)  | (None, None)
        :param font:                   specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:                    (str or (str, int[, str]) or None)
        :param background_color:       color of slider's background
        :type background_color:        (str)
        :param text_color:             color of the slider's text
        :type text_color:              (str)
        :param trough_color:           color of the slider's trough
        :type trough_color:            (str)
        :param key:                    Value that uniquely identifies this element from all other elements. Used when Finding an element or in return values. Must be unique to the window
        :type key:                     str | int | tuple | object
        :param k:                      Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                       str | int | tuple | object
        :param pad:                    Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:                     (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                      Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                       (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param expand_x:               If True the element will automatically expand in the X direction to fill available space
        :type expand_x:                (bool)
        :param expand_y:               If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:                (bool)
        :param tooltip:                text, that will appear when mouse hovers over the element
        :type tooltip:                 (str)
        :param visible:                set visibility state of the element
        :type visible:                 (bool)
        :param metadata:               User metadata that can be set to ANYTHING
        :type metadata:                (Any)
        """

        self.TKScale = self.Widget = None  # type: tk.Scale
        self.Range = (1, 10) if range == (None, None) else range
        self.DefaultValue = self.Range[0] if default_value is None else default_value
        self.Orientation = orientation if orientation else FreeSimpleGUI.DEFAULT_SLIDER_ORIENTATION
        self.BorderWidth = border_width if border_width else FreeSimpleGUI.DEFAULT_SLIDER_BORDER_WIDTH
        self.Relief = relief if relief else FreeSimpleGUI.DEFAULT_SLIDER_RELIEF
        self.Resolution = 1 if resolution is None else resolution
        self.ChangeSubmits = change_submits or enable_events
        self.Disabled = disabled
        self.TickInterval = tick_interval
        self.DisableNumericDisplay = disable_number_display
        self.TroughColor = trough_color or FreeSimpleGUI.DEFAULT_SCROLLBAR_COLOR
        sz = size if size != (None, None) else s
        temp_size = sz
        if temp_size == (None, None):
            temp_size = (20, 20) if self.Orientation.startswith('h') else (8, 20)
        key = key if key is not None else k
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y

        super().__init__(
            ELEM_TYPE_INPUT_SLIDER,
            size=temp_size,
            font=font,
            background_color=background_color,
            text_color=text_color,
            key=key,
            pad=pad,
            tooltip=tooltip,
            visible=visible,
            metadata=metadata,
        )
        return

    def update(self, value=None, range=(None, None), disabled=None, visible=None):
        """
        Changes some of the settings for the Slider Element. Must call `Window.Read` or `Window.Finalize` prior

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param value:    sets current slider value
        :type value:     int | float
        :param range:    Sets a new range for slider
        :type range:     (int, int) | Tuple[float, float
        :param disabled: disable or enable state of the element
        :type disabled:  (bool)
        :param visible:  control visibility of element
        :type visible:   (bool)
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Slider.update - The window was closed')
            return

        if range != (None, None):
            self.TKScale.config(from_=range[0], to_=range[1])
        if value is not None:
            try:
                self.TKIntVar.set(value)
            except:
                pass
            self.DefaultValue = value
        if disabled is True:
            self.TKScale['state'] = 'disabled'
        elif disabled is False:
            self.TKScale['state'] = 'normal'
        self.Disabled = disabled if disabled is not None else self.Disabled

        if visible is False:
            self._pack_forget_save_settings()
        elif visible is True:
            self._pack_restore_settings()

        if visible is not None:
            self._visible = visible

    def _SliderChangedHandler(self, event):
        """
        Not user callable.  Callback function for when slider is moved.

        :param event: (event) the event data provided by tkinter. Unknown format. Not used.
        :type event:
        """

        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = ''
        self.ParentForm.FormRemainedOpen = True
        _exit_mainloop(self.ParentForm)

    Update = update
