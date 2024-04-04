
![free_simplegui_logo](https://raw.githubusercontent.com/spyoungtech/FreeSimpleGUI/main/images/for_readme/freesimplegui.png)


[![PyPI Version](https://img.shields.io/pypi/v/freesimpleguiweb.svg?style=for-the-badge)](https://pypi.org/project/FreeSimpleGUIWeb/)

# FreeSimpleGUIWeb

FreeSimpleGUI running in your web browser!

Your source code will work on tkinter, Qt, WxPython and now in a browser (thanks to Remi)


## Primary FreeSimpleGUI Documentation

To get instructions on how use FreeSimpleGUI's APIs, please reference the [main documentation](http://www.FreeSimpleGUI.org).
This Readme is for information ***specific to*** the Web port of FreeSimpleGUI.


## What is FreeSimpleGUIWeb?

FreeSimpleGUIWeb enables you to run your FreeSimpleGUI programs in your web browser.  It utilizes a package called Remi to achieve this amazing package.


## Installation

Installation is quite simple:

`pip install FreeSimpleGUIWeb`

Should this not work, you can copy and paste the file FreeSimpleGUIWeb.py into your application folder.

## Using FreeSimpleGUIWeb

There are a lot of examples in the FreeSimpleGUI Cookbook as well as on the GitHub site.  At the moment very few will work due to the limited number of features of the 0.1.0 release.  It shouldn't be too long before they'll work.

To use FreeSimpleGUIWeb you need to import it:
`import FreeSimpleGUIWeb as sg`

From there follow the code examples in the Cookbook and the Demo Programs.  The only difference in those programs is the import statement.  The remainder of the code should work without modification.


## Requirements

FreeSimpleGUIWeb is based on the Remi project.  You will need to install Remi prior to running FreeSimpleGUIWeb:

`pip install remi`

You can learn more about Remi on its homepage.

https://github.com/dddomodossola/remi

FreeSimpleGUIWeb runs only on Python 3. Legacy Python (2.7) is not supported.


## What Works

* Text Element
* Input Text Element
* Button Element
* Combobox Element
* Checkbox Element
* Listbox Element
* Spinner Element (sorta... numbers 0 to 100 only now)
* Column Element
* Image Element
* Multiline Input Element
* Multiline Output Element
* Output Element (redirect STDOUT)
* Graph Element (your canvas to paint on)
* Table Element (yes, tables! even if limited)
* Window background color
* Element padding
* Read with timeout
* Read with timeout = 0
* Popup Windows
* Multiple windows
* Update methods for many of the elements (Text is 100% complete), others have some of their parameters working.


# License
 GNU Lesser General Public License (LGPL 3) +
