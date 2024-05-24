from __future__ import annotations

from FreeSimpleGUI import ELEM_TYPE_SIZEGRIP
from FreeSimpleGUI import Element
from FreeSimpleGUI import theme_background_color


class Sizegrip(Element):
    """
    Sizegrip element will be added to the bottom right corner of your window.
    It should be placed on the last row of your window along with any other elements on that row.
    The color will match the theme's background color.
    """

    def __init__(self, background_color=None, pad=None, p=(0, 0), key=None, k=None):
        """
        Sizegrip Element
        :param background_color: color to use for the background of the grip
        :type background_color:  str
        :param pad:   Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:    (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:     Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:      (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param key:   Value that uniquely identifies this element from all other elements. Used when Finding an element or in return values. Must be unique to the window
        :type key:    str | int | tuple | object
        :param k:     Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:      str | int | tuple | object
        """

        bg = background_color if background_color is not None else theme_background_color()
        pad = pad if pad is not None else p
        key = key if key is not None else k

        super().__init__(ELEM_TYPE_SIZEGRIP, background_color=bg, key=key, pad=pad)
