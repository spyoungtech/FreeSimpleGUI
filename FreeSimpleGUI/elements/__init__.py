from .button import Button
from .button import ButtonMenu
from .checkbox import Checkbox
from .combo import Combo
from .frame import Frame
from .graph import Graph
from .image import Image
from .input import Input
from .list_box import Listbox
from .multiline import Multiline
from .option_menu import OptionMenu
from .progress_bar import ProgressBar
from .radio import Radio
from .spin import Spin
from .status_bar import StatusBar
from .text import Text

# TODO: document aliases in respective classes

# Input aliases
In = Input
InputText = Input
I = Input  # noqa

# Combo aliases
InputCombo = Combo
DropDown = InputCombo
Drop = InputCombo
DD = Combo

# Option menu aliases
InputOptionMenu = OptionMenu


# listbox aliases
LBox = Listbox
LB = Listbox


# radio aliases
R = Radio
Rad = Radio

# Checkbox aliases
CB = Checkbox
CBox = Checkbox
Check = Checkbox


Sp = Spin  # type: Spin


ML = Multiline
MLine = Multiline

# -------------------------  Text Element lazy functions  ------------------------- #

Txt = Text  # type: Text
T = Text  # type: Text

SBar = StatusBar


# -------------------------  Button lazy functions  ------------------------- #
B = Button
Btn = Button


BMenu = ButtonMenu
BM = ButtonMenu

Im = Image


PBar = ProgressBar
Prog = ProgressBar
Progress = ProgressBar

G = Graph


Fr = Frame


VSeperator = VerticalSeparator
VSeparator = VerticalSeparator
VSep = VerticalSeparator


HSeparator = HorizontalSeparator
HSep = HorizontalSeparator

SGrip = Sizegrip
