
![free_simplegui_logo](https://raw.githubusercontent.com/spyoungtech/FreeSimpleGUI/main/images/for_readme/freesimplegui.png)


[![PyPI Version](https://img.shields.io/pypi/v/freesimpleguiwx.svg?style=for-the-badge)](https://pypi.org/project/FreeSimpleGUIWx/)


# FreeSimpleGUIWx

The WxPython port of FreeSimpleGUI

## Primary FreeSimpleGUI Documentation

To get instructions on how use FreeSimpleGUI's APIs, please reference the [main documentation](http://www.FreeSimpleGUI.org).
This Readme is for information ***specific to*** the WxPython port of FreeSimpleGUI.


## Why Use FreeSimpleGUIWx Over The Other Ports?

FreeSimpleGUIWx brings the number of FreeSimpleGUI ports to 3.

Why use FreeSimpleGUIWx over FreeSimpleGUIQt FreeSimpleGUI (tkinter version)?

There are a couple of easy reasons to use FreeSimpleGUIWx over FreeSimpleGUIQt. One is footprint.  PyInstaller EXE for FreeSimpleGUIWx is 9 MB, on Qt it's 240 MB.  Another is cool widgets.

WxPython has some nice advanced widgets that will be offered though FreeSimpleGUIWx, hopefully sooner than later.

The System Tray feature works well with a feature set identical to FreeSimpleGUIQt.  If you are looking for a System Tray feature, FreeSimpleGUIWx is recommended over FreeSimpleGUIQt ; the primary reason being size of the WxPython framework versus the size of Qt.  They both give you very similar features.  They look and behave in an ***identical*** fashion when using FreeSimpleGUI.  That's the beauty of the PSG SDK, the function calls are the same for all implementations of FreeSimpleGUI.  The source code is highly portable between the GUI frameworks.

This simple list is another way of looking at the question....

1.  It's simple and easy to program GUIs
2.  You can move between the GUI frameworks tkinter, Qt and WxPython by changing a single line of code, the import statement.
3.  Get the same custom layout and access to the same widgets but in a simple, easy to use and understand interface.
4.  It's fun to program GUIs again



## What Works

Remember, these are Engineering Releases.  Not all features are complete, but generally speaking those that are marked as completed and working are working quite well.  It's not an "Engineering Quality".  The completed features are at about a Beta level.

### Ready to use

#### Elements

* Text
* Input Text
* Buttons including file/folder browse
* Input multiline
* Output multiline
* Output
* Columns
* Frames - except cannot set colors yet
* Progress Meters
* Checkbox
* Radio Button
* Combobox
* Spinner
* Vertical and Horizontal Separators


#### Features

* System Tray
* Debug Print
* Invisible/Visible Elements
* All Popups
* Check box
* Keyboard key events
* Mouse wheel events
* Multiple windows
* Read with timeout
* Background images
* One Line Progress Meter (tm)
* Auto-closing windows
* No titlebar windows
* Grab anywhere windows
* Alpha channel
* Window size
* Window disappear/reappear
* Get screen size
* Get window location
* Change window size
* Window move
* Window minimize
* Window maximize
* Window Disable
* Window Enable
* Window Hide
* Window UnHide
* Window Bring to front
* Look and Feel settings
* Default Icon
* Base64 Icons
* PEP8 bindings for all element methods and functions


It won't take long to poke at these and hit errors.  For example, the code to do Button Updates is not complete.  Most of the time you won't be doing this.

Due to the small size of the development team, features may feel a little "thin" for a while.  The idea is to implement with enough depth that 80% of the uses are covered.  It's a multi-pass, iterative approach.

If you, the reader, are having problems or have hit a spot where something is not yet implemented, then open an Issue.  They are often completed in a day.  This process of users pushing the boundaries is what drives the priorities for development.  It's "real world" kinds of problems that have made FreeSimpleGUI what it is today.



## SystemTray

This was the first fully functioning feature of FreeSimpleGUIWx.  Previously only the Qt port supported the System Tray.  Why use Wx?  The footprint is much much smaller.  An EXE file created using PyInstaller is 9 MB for FreeSimpleGUIWx, when using Qt it's 240 MB.

Now it's possible to "tack on" the System Tray to your FreeSimpleGUI application.

If you're unable to upgrade to Qt but want the System Tray feature, then adding FreeSimpleGUIWx to your project may be the way to go.

You can mix your System Tray's event loop with your normal Window event loop by adding a timeout to both your Window.Read call and your SystemTray.Read call.

### Source code compatibility

FreeSimpleGUIWx's System Tray feature has been tested against the same FreeSimpleGUIQt feature.  As long as you don't use features that are not yet supported you'll find your source code will run on either FreeSimpleGUIQt or FreeSimpleGUIWx by changing the import statement.


## System Tray Design Pattern

Here is a design pattern you can use to get a jump-start.

This program will create a system tray icon and perform a blocking Read.

```python
import FreeSimpleGUIWx as sg

tray = sg.SystemTray(menu=['menu', ['Open', ['&Save::KEY', '---', 'Issues', '!Disabled'], 'E&xit']],
                     filename=r'C:\Python\PycharmProjects\GooeyGUI\default_icon.ico')
tray.ShowMessage('My Message', 'The tray icon is up and runnning!')
while True:
    event = tray.Read()
    print(event)
    if event == 'Exit':
        break
```


## Menu Definitions

See the original, full documentation for FreeSimpleGUI to get an understanding of how menus are defined.


## SystemTray Methods

### Read - Read the context menu or check for events

```python
def Read(timeout=None)
    '''
 Reads the context menu
 :param timeout: Optional.  Any value other than None indicates a non-blocking read
 :return:   String representing meny item chosen. None if nothing read.
    '''
```
The `timeout` parameter specifies how long to wait for an event to take place.  If nothing happens within the timeout period, then a "timeout event" is returned.  These types of reads make it possible to run asynchronously.  To run non-blocked, specify `timeout=0`on the Read call (not yet supported).

Read returns the menu text, complete with key, for the menu item chosen.  If you specified `Open::key` as the menu entry, and the user clicked on `Open`, then you will receive the string `Open::key` upon completion of the Read.

#### Read special return values

In addition to Menu Items, the Read call can return several special values.    They include:

EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED - Tray icon was double clicked
EVENT_SYSTEM_TRAY_ICON_ACTIVATED - Tray icon was single clicked
EVENT_SYSTEM_TRAY_MESSAGE_CLICKED - a message balloon was clicked
TIMEOUT_KEY is returned if no events are available if the timeout value is set in the Read call


### ShowMessage

Just like Qt, you can create a pop-up message.  Unlike Qt, you cannot set your own custom icon in the message, at least you can't at the moment.

The preset `messageicon` values are:

    SYSTEM_TRAY_MESSAGE_ICON_INFORMATION
    SYSTEM_TRAY_MESSAGE_ICON_WARNING
    SYSTEM_TRAY_MESSAGE_ICON_CRITICAL
    SYSTEM_TRAY_MESSAGE_ICON_NOICON

```python
ShowMessage(title, message, filename=None, data=None, data_base64=None, messageicon=None, time=10000):
    '''
 Shows a balloon above icon in system tray
 :param title:  Title shown in balloon
 :param message: Message to be displayed
 :param filename: Optional icon filename
 :param data: Optional in-ram icon
 :param data_base64: Optional base64 icon
 :param time: How long to display message in milliseconds  :return:
 '''
```

### Update

You can update any of these items within a SystemTray object
* Menu definition
* Icon (not working yet)
* Tooltip

 Change them all or just 1.

```python
Update(menu=None, tooltip=None,filename=None, data=None, data_base64=None,)
    '''
 Updates the menu, tooltip or icon
 :param menu: menu defintion
 :param tooltip: string representing tooltip
 :param filename:  icon filename
 :param data:  icon raw image
 :param data_base64: icon base 64 image
 :return:
 '''
```
## Menus with Keys

You can add a key to your menu items.  To do so, you add :: and the key value to the end of your menu definition.

`menu_def = ['File', ['Hide::key', '&Open::key', '&Save',['1', '2', ['a','b']], '&Properties', 'E&xit']]`

The menu definition adds a key "key" to the menu entries Hide and Open.

If you want to change the separator characters from :: top something else,change the variable `MENU_KEY_SEPARATOR`

When a menu item has a key and it is chosen, then entire string is returned.  If Hide were selected, then Hide::key would be returned from the Read.  Note that the shortcut character & is NOT returned from Reads.


# License
 GNU Lesser General Public License (LGPL 3) +
