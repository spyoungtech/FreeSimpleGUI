from __future__ import annotations

import textwrap
import tkinter as tk

from FreeSimpleGUI import EVENT_SYSTEM_TRAY_ICON_ACTIVATED  # = '__ACTIVATED__'
from FreeSimpleGUI import EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED  # = '__DOUBLE_CLICKED__'
from FreeSimpleGUI import EVENT_SYSTEM_TRAY_MESSAGE_CLICKED  # = '__MESSAGE_CLICKED__'
from FreeSimpleGUI import SYSTEM_TRAY_MESSAGE_DISPLAY_DURATION_IN_MILLISECONDS  # = 3000  # how long to display the window
from FreeSimpleGUI import SYSTEM_TRAY_MESSAGE_FADE_IN_DURATION  # = 1000  # how long to fade in / fade out the window
from FreeSimpleGUI import SYSTEM_TRAY_MESSAGE_MAX_LINE_LENGTH  # = 50
from FreeSimpleGUI import SYSTEM_TRAY_MESSAGE_TEXT_COLOR  # = '#ffffff'
from FreeSimpleGUI import SYSTEM_TRAY_MESSAGE_WIN_COLOR  # = '#282828'
from FreeSimpleGUI import SYSTEM_TRAY_WIN_MARGINS  # = 160, 60  # from right edge of screen, from bottom of screen
from FreeSimpleGUI import TEXT_LOCATION_TOP_LEFT
from FreeSimpleGUI import TIMEOUT_KEY
from FreeSimpleGUI.elements.graph import Graph
from FreeSimpleGUI.elements.helpers import AddMenuItem
from FreeSimpleGUI.elements.image import Image
from FreeSimpleGUI.window import Window


_tray_icon_error = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAA3NCSVQICAjb4U/gAAAACXBIWXMAAADlAAAA5QGP5Zs8AAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAIpQTFRF////20lt30Bg30pg4FJc409g4FBe4E9f4U9f4U9g4U9f4E9g31Bf4E9f4E9f4E9f4E9f4E9f4FFh4Vdm4lhn42Bv5GNx5W575nJ/6HqH6HyI6YCM6YGM6YGN6oaR8Kev9MPI9cbM9snO9s3R+Nfb+dzg+d/i++vt/O7v/fb3/vj5//z8//7+////KofnuQAAABF0Uk5TAAcIGBktSYSXmMHI2uPy8/XVqDFbAAAA8UlEQVQ4y4VT15LCMBBTQkgPYem9d9D//x4P2I7vILN68kj2WtsAhyDO8rKuyzyLA3wjSnvi0Eujf3KY9OUP+kno651CvlB0Gr1byQ9UXff+py5SmRhhIS0oPj4SaUUCAJHxP9+tLb/ezU0uEYDUsCc+l5/T8smTIVMgsPXZkvepiMj0Tm5txQLENu7gSF7HIuMreRxYNkbmHI0u5Hk4PJOXkSMz5I3nyY08HMjbpOFylF5WswdJPmYeVaL28968yNfGZ2r9gvqFalJNUy2UWmq1Wa7di/3Kxl3tF1671YHRR04dWn3s9cXRV09f3vb1fwPD7z9j1WgeRgAAAABJRU5ErkJggg=='
_tray_icon_success = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAA3NCSVQICAjb4U/gAAAACXBIWXMAAAEKAAABCgEWpLzLAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAHJQTFRF////ZsxmbbZJYL9gZrtVar9VZsJcbMRYaMZVasFYaL9XbMFbasRZaMFZacRXa8NYasFaasJaasFZasJaasNZasNYasJYasJZasJZasJZasJZasJZasJYasJZasJZasJZasJZasJaasJZasJZasJZasJZ2IAizQAAACV0Uk5TAAUHCA8YGRobHSwtPEJJUVtghJeYrbDByNjZ2tvj6vLz9fb3/CyrN0oAAADnSURBVDjLjZPbWoUgFIQnbNPBIgNKiwwo5v1fsQvMvUXI5oqPf4DFOgCrhLKjC8GNVgnsJY3nKm9kgTsduVHU3SU/TdxpOp15P7OiuV/PVzk5L3d0ExuachyaTWkAkLFtiBKAqZHPh/yuAYSv8R7XE0l6AVXnwBNJUsE2+GMOzWL8k3OEW7a/q5wOIS9e7t5qnGExvF5Bvlc4w/LEM4Abt+d0S5BpAHD7seMcf7+ZHfclp10TlYZc2y2nOqc6OwruxUWx0rDjNJtyp6HkUW4bJn0VWdf/a7nDpj1u++PBOR694+Ftj/8PKNdnDLn/V8YAAAAASUVORK5CYII='
_tray_icon_halt = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAANswNuMPDO8HBO8FCe0HCu4IBu4IB+oLDeoLDu8JC+wKCu4JDO4LDOwKEe4OEO4OEeUQDewQDe0QDucVEuYcG+ccHOsQFuwWHe4fH/EGAvMEBfMFBvAHBPMGBfEGBvYCAfYDAvcDA/cDBPcDBfUDBvYEAPYEAfYEAvYEA/QGAPQGAfQGAvYEBPUEBvYFB/QGBPQGBfQHB/EFCvIHCPMHCfIHC/IFDfMHDPQGCPQGCfQGCvEIBPIIBfAIB/UIB/QICPYICfoBAPoBAfoBAvsBA/kCAPkCAfkCAvkCA/oBBPkCBPkCBfkCBvgCB/gEAPkEAfgEAvkEA/gGAfkGAvkEBPgEBfkEBv0AAP0AAfwAAvwAA/wCAPwCAfwCAvwCA/wABP0ABfwCBfwEAPwFA/ASD/ESFPAUEvAUE/EXFvAdH+kbIOobIeofIfEfIOcmKOohIukgJOggJesiKuwiKewoLe0tLO0oMOQ3OO43Oew4OfAhIPAhIfAiIPEiI+dDRe9ES+lQTOdSWupSUOhTUehSV+hUVu1QUO1RUe1SV+tTWe5SWOxXWOpYV+pZWelYXexaW+xaXO9aX+lZYeNhYOxjZ+lna+psbOttbehsbupscepucuxtcuxucep3fet7e+p/ffB6gOmKiu2Iie2Sk+2Qle2QluySlOyTleuYmvKFivCOjgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIxGNZsAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAACVElEQVQ4T22S93PTMBhADQdl791SSsuRARTKKHsn+STZBptAi6zIacous+w9yyxl7z1T1h8ptHLhrrzLD5+/987R2XZElZ/39tZsbGg42NdvF4pqcGMs4XEcozAB/oQeu6wGr5fkAZcKOUIIRgQXR723wgaXt/NSgcwlO1r3oARkATfhbmNMMCnlMZdz5J8RN9fVhglS5JA/pJUOJiYXoShCkz/flheDvpzlBCBmya5KcDG1sMSB+r/VQtG+YoFXlwN0Us4yeBXujPmWCOqNlVwX5zHntLH5iQ420YiqX9pqTZFSCrBGBc+InBUDAsbwLRlMC40fGJT8YLRwfnhY3v6/AUtDc9m5z0tRJBOAvHUaFchdY6+zDzEghHv1tUnrNCaIOw84Q2WQmkeO/Xopj1xFBREFr8ZZjuRhA++PEB+t05ggwBucpbH8i/n5C1ZU0EEEmRZnSMxoIYcarKigA0Cb1zpHAyZnGj21xqICAA9dcvo4UgEdZ41FBZSTzEOn30f6QeE3Vhl0gLN+2RGDzZPMHLHKoAO3MFy+ix4sDxFlvMXfrdNgFezy7qrXPaaJg0u27j5nneKrCjJ4pf4e3m4DVMcjNNNKxWnpo6jtnfnkunExB4GbuGKk5FNanpB1nJCjCsThJPAAJ8lVdSF5sSrklM2ZqmYdiC40G7Dfnhp57ZsQz6c3hylEO6ZoZQJxqiVgbhoQK3T6AIgU4rbjxthAPF6NAwAOAcS+ixlp/WBFJRDi0fj2RtcjWRwif8Qdu/w3EKLcu3/YslnrZzwo24UQQvwFCrp/iM1NnHwAAAAASUVORK5CYII='
_tray_icon_notallowed = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAAPcICPcLC/cMDPcQEPcSEvcXF/cYGPcaGvcbG/ccHPgxMfgyMvg0NPg5Ofg6Ovg7O/hBQfhCQvlFRflGRvljY/pkZPplZfpnZ/p2dgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMgEwNYAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAABE0lEQVQ4T4WT65bDIAiExWbbtN0m3Uua+P4P6g4jGtN4NvNL4DuCCC5WWobe++uwmEmtwNxJUTebcwWCt5jJBwsYcKf3NE4hTOOJxj1FEnBTz4NH6qH2jUcCGr/QLLpkQgHe/6VWJXVqFgBB4yI/KVCkBCoFgPrPHw0CWbwCL8RibBFwzQDQH62/QeAtHQBeADUIDbkF/UnmnkB1ixtERrN3xCgyuF5kMntHTCJXh2vyv+wIdMhvgTeCQJ0C2hBMgSKfZlM1wSLXZ5oqgs8sjSpaCQ2VVlfKhLU6fdZGSvyWz9JMb+NE4jt/Nwfm0yJZSkBpYDg7TcJGrjm0Z7jK0B6P/fHiHK8e9Pp/eSmuf1+vf4x/ralnCN9IrncAAAAASUVORK5CYII='
_tray_icon_stop = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAANsAANsBAdsCAtwEBNwFBdwHB9wICNwLC90MDN0NDd0PD90REd0SEt4TE94UFN4WFt4XF94ZGeAjI+AlJeEnJ+EpKeEqKuErK+EsLOEuLuIvL+IyMuIzM+M1NeM2NuM3N+M6OuM8POQ9PeQ+PuQ/P+RAQOVISOVJSeVKSuZLS+ZOTuZQUOZRUedSUudVVehbW+lhYeljY+poaOtvb+twcOtxcetzc+t0dOx3d+x4eOx6eu19fe1+fu2AgO2Cgu6EhO6Ghu6Hh+6IiO6Jie+Kiu+Li++MjO+Nje+Oju+QkPCUlPCVlfKgoPKkpPKlpfKmpvOrq/SurvSxsfSysvW4uPW6uvW7u/W8vPa9vfa+vvbAwPbCwvfExPfFxffGxvfHx/fIyPfJyffKyvjLy/jNzfjQ0PjR0fnS0vnU1PnY2Pvg4Pvi4vvj4/vl5fvm5vzo6Pzr6/3u7v3v7/3x8f3z8/309P719f729v739/74+P75+f76+v77+//8/P/9/f/+/v///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPHCyoUAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAABnUlEQVQ4T33S50PTQBgG8D6lzLbsIUv2kD0FFWTvPWTvISDIUBGV1ecvj+8luZTR9P1wSe755XK5O4+hK4gn5bc7DcMBz/InQoMXeVjY4FXuCAtEyLUwQcTcFgq45JYQ4JqbwhMtV8IjeUJDjQ+5paqCyG9srEsGgoUlpeXpIjxA1nfyi2+Jqmo7Q9JeV+ODerpvBQTM8/ySzQ3t+xxoL7h7nJve5jd85M7wJq9McHaT8o6TwBTfIIfHQGzoAZ/YiSTSq8D5dSDQVqFADrJ5KFMLPaKLHQiQMQoscClezdgCB4CXD/jM90izR8g85UaKA3YAn4AejhV189acA5LX+DVOg00gnvfoVX/BRQsgbplNGqzLusgIffx1tDchiyRgdRbVHNdgRRZHQD9H1asm+PMzYyYMtoBU/sYgRxxgrmGtBRL/cnf5RL4zzCEHZF2QE14LoOWf6B9vMcJBG/iBxKo8dVtYnyStv6yuUq7FLfmqTzbLEOFest1GNGEemCjCPnKuwjm0LsLMbRBJWLkGr4WdO+Cl0HkYPBc6N4z//HcQqVwcOuIAAAAASUVORK5CYII='
_tray_icon_exclamation = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAAN0zM900NN01Nd02Nt03N944ON45Od46Ot47O98/P99BQd9CQt9DQ+FPT+JSUuJTU+JUVOJVVeJWVuNbW+ReXuVjY+Zra+dxceh4eOl7e+l8fOl+ful/f+qBgeqCguqDg+qFheuJieuLi+yPj+yQkO2Wlu+cnO+hofGqqvGtrfre3vrf3/ri4vvn5/75+f76+v/+/v///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMQ8SQkAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAABJElEQVQ4T4WS63KCMBBGsyBai62X0otY0aq90ZZa3v/dtpvsJwTijOfXt7tnILOJYY9tNonjNCtQOlqhuKKG0RrNVjgkmIHBHgMId+h7zHSiwg2a9FNVVYScupETmjkd67o+CWpYwft+R6CpCgeUlq5AOyf45+8JsRUKFI6eQLkI3n5CIREBUekLxGaLpATCymRISiAszARJCYSxiZGUQKDLQoqgnPnFhUPOTWeRoZD3FvVZlmVHkE2OEM9iV71GVoZDBGUpAg9QWN5/jx+Ilsi9hz0q4VHOWD+hEF70yc1QEr1a4Q0F0S3eJDfLuv8T4QEFXduZE1rj+et7g6hzCDxF08N+X4DAu+6lUSTnc5wE5tx73ckSTV8QVoux3N88Rykw/wP3i+vwPKk17AAAAABJRU5ErkJggg=='
_tray_icon_none = None

from FreeSimpleGUI import SYSTEM_TRAY_MESSAGE_ICON_INFORMATION
from FreeSimpleGUI import SYSTEM_TRAY_MESSAGE_ICON_WARNING
from FreeSimpleGUI import SYSTEM_TRAY_MESSAGE_ICON_CRITICAL
from FreeSimpleGUI import SYSTEM_TRAY_MESSAGE_ICON_NOICON


class SystemTray:
    """
    A "Simulated System Tray" that duplicates the API calls available to PySimpleGUIWx and PySimpleGUIQt users.

    All of the functionality works. The icon is displayed ABOVE the system tray rather than inside of it.
    """

    def __init__(self, menu=None, filename=None, data=None, data_base64=None, tooltip=None, metadata=None):
        """
        SystemTray - create an icon in the system tray
        :param menu:        Menu definition. Example - ['UNUSED', ['My', 'Simple', '---', 'Menu', 'Exit']]
        :type menu:         List[List[List[str] or str]]
        :param filename:    filename for icon
        :type filename:     (str)
        :param data:        in-ram image for icon (same as data_base64 parm)
        :type data:         (bytes)
        :param data_base64: base-64 data for icon
        :type data_base64:  (bytes)
        :param tooltip:     tooltip string
        :type tooltip:      (str)
        :param metadata:    User metadata that can be set to ANYTHING
        :type metadata:     (Any)
        """
        self._metadata = None
        self.Menu = menu
        self.TrayIcon = None
        self.Shown = False
        self.MenuItemChosen = TIMEOUT_KEY
        self.metadata = metadata
        self.last_message_event = None

        screen_size = Window.get_screen_size()

        if filename:
            image_elem = Image(filename=filename, background_color='red', enable_events=True, tooltip=tooltip, key='-IMAGE-')
        elif data_base64:
            image_elem = Image(data=data_base64, background_color='red', enable_events=True, tooltip=tooltip, key='-IMAGE-')
        elif data:
            image_elem = Image(data=data, background_color='red', enable_events=True, tooltip=tooltip, key='-IMAGE-')
        else:
            image_elem = Image(background_color='red', enable_events=True, tooltip=tooltip, key='-IMAGE-')
        layout = [
            [image_elem],
        ]
        self.window = Window(
            'Window Title',
            layout,
            element_padding=(0, 0),
            margins=(0, 0),
            grab_anywhere=True,
            no_titlebar=True,
            transparent_color='red',
            keep_on_top=True,
            right_click_menu=menu,
            location=(screen_size[0] - 100, screen_size[1] - 100),
            finalize=True,
        )

        self.window['-IMAGE-'].bind('<Double-Button-1>', '+DOUBLE_CLICK')

    @property
    def metadata(self):
        """
        Metadata is an SystemTray property that you can use at any time to hold any value
        :return: the current metadata value
        :rtype:  (Any)
        """
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        """
        Metadata is an SystemTray property that you can use at any time to hold any value
        :param value: Anything you want it to be
        :type value:  (Any)
        """
        self._metadata = value

    def read(self, timeout=None):
        """
        Reads the context menu
        :param timeout: Optional.  Any value other than None indicates a non-blocking read
        :type timeout:
        :return:
        :rtype:
        """
        if self.last_message_event != TIMEOUT_KEY and self.last_message_event is not None:
            event = self.last_message_event
            self.last_message_event = None
            return event
        event, values = self.window.read(timeout=timeout)
        if event.endswith('DOUBLE_CLICK'):
            return EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED
        elif event == '-IMAGE-':
            return EVENT_SYSTEM_TRAY_ICON_ACTIVATED

        return event

    def hide(self):
        """
        Hides the icon
        """
        self.window.hide()

    def un_hide(self):
        """
        Restores a previously hidden icon
        """
        self.window.un_hide()

    def show_message(
        self,
        title,
        message,
        filename=None,
        data=None,
        data_base64=None,
        messageicon=None,
        time=(SYSTEM_TRAY_MESSAGE_FADE_IN_DURATION, SYSTEM_TRAY_MESSAGE_DISPLAY_DURATION_IN_MILLISECONDS),
    ):
        """
        Shows a balloon above icon in system tray
        :param title:       Title shown in balloon
        :type title:        str
        :param message:     Message to be displayed
        :type message:      str
        :param filename:    Optional icon filename
        :type filename:     str
        :param data:        Optional in-ram icon
        :type data:         b''
        :param data_base64: Optional base64 icon
        :type data_base64:  b''
        :param time:        Amount of time to display message in milliseconds. If tuple, first item is fade in/out duration
        :type time:         int | (int, int)
        :return:            The event that happened during the display such as user clicked on message
        :rtype:             Any
        """

        if isinstance(time, tuple):
            fade_duration, display_duration = time
        else:
            fade_duration = SYSTEM_TRAY_MESSAGE_FADE_IN_DURATION
            display_duration = time

        user_icon = data_base64 or filename or data or messageicon

        event = self.notify(title, message, icon=user_icon, fade_in_duration=fade_duration, display_duration_in_ms=display_duration)
        self.last_message_event = event
        return event

    def close(self):
        """
        Close the system tray window
        """
        self.window.close()

    def update(
        self,
        menu=None,
        tooltip=None,
        filename=None,
        data=None,
        data_base64=None,
    ):
        """
        Updates the menu, tooltip or icon
        :param menu:        menu defintion
        :type menu:         ???
        :param tooltip:     string representing tooltip
        :type tooltip:      ???
        :param filename:    icon filename
        :type filename:     ???
        :param data:        icon raw image
        :type data:         ???
        :param data_base64: icon base 64 image
        :type data_base64:  ???
        """
        # Menu
        if menu is not None:
            top_menu = tk.Menu(self.window.TKroot, tearoff=False)
            AddMenuItem(top_menu, menu[1], self.window['-IMAGE-'])
            self.window['-IMAGE-'].TKRightClickMenu = top_menu

        if filename:
            self.window['-IMAGE-'].update(filename=filename)
        elif data_base64:
            self.window['-IMAGE-'].update(data=data_base64)
        elif data:
            self.window['-IMAGE-'].update(data=data)

        if tooltip:
            self.window['-IMAGE-'].set_tooltip(tooltip)

    @classmethod
    def notify(
        cls,
        title,
        message,
        icon=_tray_icon_success,
        display_duration_in_ms=SYSTEM_TRAY_MESSAGE_DISPLAY_DURATION_IN_MILLISECONDS,
        fade_in_duration=SYSTEM_TRAY_MESSAGE_FADE_IN_DURATION,
        alpha=0.9,
        location=None,
    ):
        """
        Displays a "notification window", usually in the bottom right corner of your display.  Has an icon, a title, and a message
        The window will slowly fade in and out if desired.  Clicking on the window will cause it to move through the end the current "phase". For example, if the window was fading in and it was clicked, then it would immediately stop fading in and instead be fully visible.  It's a way for the user to quickly dismiss the window.
        :param title:                  Text to be shown at the top of the window in a larger font
        :type title:                   (str)
        :param message:                Text message that makes up the majority of the window
        :type message:                 (str)
        :param icon:                   A base64 encoded PNG/GIF image or PNG/GIF filename that will be displayed in the window
        :type icon:                    bytes | str
        :param display_duration_in_ms: Number of milliseconds to show the window
        :type display_duration_in_ms:  (int)
        :param fade_in_duration:       Number of milliseconds to fade window in and out
        :type fade_in_duration:        (int)
        :param alpha:                  Alpha channel. 0 - invisible 1 - fully visible
        :type alpha:                   (float)
        :param location:               Location on the screen to display the window
        :type location:                (int, int)
        :return:                       (int) reason for returning
        :rtype:                        (int)
        """

        messages = message.split('\n')
        full_msg = ''
        for m in messages:
            m_wrap = textwrap.fill(m, SYSTEM_TRAY_MESSAGE_MAX_LINE_LENGTH)
            full_msg += m_wrap + '\n'
        message = full_msg[:-1]

        win_msg_lines = message.count('\n') + 1

        screen_res_x, screen_res_y = Window.get_screen_size()
        win_margin = SYSTEM_TRAY_WIN_MARGINS  # distance from screen edges
        win_width, win_height = 364, 66 + (14.8 * win_msg_lines)

        layout = [
            [
                Graph(
                    canvas_size=(win_width, win_height),
                    graph_bottom_left=(0, win_height),
                    graph_top_right=(win_width, 0),
                    key='-GRAPH-',
                    background_color=SYSTEM_TRAY_MESSAGE_WIN_COLOR,
                    enable_events=True,
                )
            ]
        ]

        win_location = location if location is not None else (screen_res_x - win_width - win_margin[0], screen_res_y - win_height - win_margin[1])
        window = Window(
            title,
            layout,
            background_color=SYSTEM_TRAY_MESSAGE_WIN_COLOR,
            no_titlebar=True,
            location=win_location,
            keep_on_top=True,
            alpha_channel=0,
            margins=(0, 0),
            element_padding=(0, 0),
            grab_anywhere=True,
            finalize=True,
        )

        window['-GRAPH-'].draw_rectangle(
            (win_width, win_height),
            (-win_width, -win_height),
            fill_color=SYSTEM_TRAY_MESSAGE_WIN_COLOR,
            line_color=SYSTEM_TRAY_MESSAGE_WIN_COLOR,
        )
        if type(icon) is bytes:
            window['-GRAPH-'].draw_image(data=icon, location=(20, 20))
        elif icon is not None:
            window['-GRAPH-'].draw_image(filename=icon, location=(20, 20))
        window['-GRAPH-'].draw_text(
            title,
            location=(64, 20),
            color=SYSTEM_TRAY_MESSAGE_TEXT_COLOR,
            font=('Helvetica', 12, 'bold'),
            text_location=TEXT_LOCATION_TOP_LEFT,
        )
        window['-GRAPH-'].draw_text(
            message,
            location=(64, 44),
            color=SYSTEM_TRAY_MESSAGE_TEXT_COLOR,
            font=('Helvetica', 9),
            text_location=TEXT_LOCATION_TOP_LEFT,
        )
        window['-GRAPH-'].set_cursor('hand2')

        if fade_in_duration:
            for i in range(1, int(alpha * 100)):  # fade in
                window.set_alpha(i / 100)
                event, values = window.read(timeout=fade_in_duration // 100)
                if event != TIMEOUT_KEY:
                    window.set_alpha(1)
                    break
            if event != TIMEOUT_KEY:
                window.close()
                return EVENT_SYSTEM_TRAY_MESSAGE_CLICKED if event == '-GRAPH-' else event
            event, values = window(timeout=display_duration_in_ms)
            if event == TIMEOUT_KEY:
                for i in range(int(alpha * 100), 1, -1):  # fade out
                    window.set_alpha(i / 100)
                    event, values = window.read(timeout=fade_in_duration // 100)
                    if event != TIMEOUT_KEY:
                        break
        else:
            window.set_alpha(alpha)
            event, values = window(timeout=display_duration_in_ms)
        window.close()

        return EVENT_SYSTEM_TRAY_MESSAGE_CLICKED if event == '-GRAPH-' else event

    Close = close
    Hide = hide
    Read = read
    ShowMessage = show_message
    UnHide = un_hide
    Update = update
