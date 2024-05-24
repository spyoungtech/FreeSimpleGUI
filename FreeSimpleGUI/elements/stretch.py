from __future__ import annotations

from FreeSimpleGUI.elements.text import Text


def Push(background_color=None):
    """
    Acts like a Stretch element found in the Qt port.
    Used in a Horizontal fashion.  Placing one on each side of an element will enter the element.
    Place one to the left and the element to the right will be right justified.  See VStretch for vertical type
    :param background_color: color of background may be needed because of how this is implemented
    :type background_color:  (str)
    :return:                 (Text)
    """
    return Text(font='_ 1', background_color=background_color, pad=(0, 0), expand_x=True)


def VPush(background_color=None):
    """
    Acts like a Stretch element found in the Qt port.
    Used in a Vertical fashion.
    :param background_color: color of background may be needed because of how this is implemented
    :type background_color:  (str)
    :return:                 (Text)
    """
    return Text(font='_ 1', background_color=background_color, pad=(0, 0), expand_y=True)
