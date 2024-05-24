from __future__ import annotations

import inspect
import sys
import traceback


def _create_error_message():
    """
    Creates an error message containing the filename and line number of the users
    code that made the call into PySimpleGUI
    :return: Error string to display with file, line number, and line of code
    :rtype:  str
    """

    called_func = inspect.stack()[1].function
    trace_details = traceback.format_stack()
    error_message = ''
    file_info_pysimplegui = trace_details[-1].split(',')[0]
    for line in reversed(trace_details):
        if line.split(',')[0] != file_info_pysimplegui:
            error_message = line
            break
    if error_message != '':
        error_parts = error_message.split(', ')
        if len(error_parts) < 4:
            error_message = error_parts[0] + '\n' + error_parts[1] + '\n' + ''.join(error_parts[2:])
    return 'The PySimpleGUI internal reporting function is ' + called_func + '\n' + 'The error originated from:\n' + error_message


def _error_popup_with_traceback(title, *args, emoji=None):
    if SUPPRESS_ERROR_POPUPS:
        return
    trace_details = traceback.format_stack()
    error_message = ''
    file_info_pysimplegui = None
    for line in reversed(trace_details):
        if __file__ not in line:
            file_info_pysimplegui = line.split(',')[0]
            error_message = line
            break
    if file_info_pysimplegui is None:
        _error_popup_with_code(title, None, None, 'Did not find your traceback info', *args, emoji=emoji)
        return

    error_parts = None
    if error_message != '':
        error_parts = error_message.split(', ')
        if len(error_parts) < 4:
            error_message = error_parts[0] + '\n' + error_parts[1] + '\n' + ''.join(error_parts[2:])
    if error_parts is None:
        print('*** Error popup attempted but unable to parse error details ***')
        print(trace_details)
        return
    filename = error_parts[0][error_parts[0].index('File ') + 5 :]
    line_num = error_parts[1][error_parts[1].index('line ') + 5 :]
    _error_popup_with_code(title, filename, line_num, error_message, *args, emoji=emoji)


def _error_popup_with_code(title, filename, line_num, *args, emoji=None):
    """
    Makes the error popup window

    :param title:     The title that will be shown in the popup's titlebar and in the first line of the window
    :type title:      str
    :param filename:  The filename to show.. may not be the filename that actually encountered the exception!
    :type filename:   str
    :param line_num:  Line number within file with the error
    :type line_num:   int | str
    :param args:      A variable number of lines of messages
    :type args:       *Any
    :param emoji:     An optional BASE64 Encoded image to shows in the error window
    :type emoji:      bytes
    """
    editor_filename = execute_get_editor()
    emoji_data = emoji if emoji is not None else _random_error_emoji()
    layout = [[Text('ERROR'), Text(title)], [Image(data=emoji_data)]]
    lines = []
    for msg in args:
        if isinstance(msg, Exception):
            lines += [[f'Additional Exception info pased in by PySimpleGUI or user: Error type is: {type(msg).__name__}']]
            lines += [[f'In file {__file__} Line number {msg.__traceback__.tb_lineno}']]
            lines += [[f'{msg}']]
        else:
            lines += [str(msg).split('\n')]
    max_line_len = 0
    for line in lines:
        max_line_len = max(max_line_len, max([len(s) for s in line]))

    layout += [[Text(''.join(line), size=(min(max_line_len, 90), None))] for line in lines]
    layout += [
        [
            Button('Close'),
            Button('Take me to error', disabled=True if not editor_filename else False),
            Button('Kill Application', button_color='white on red'),
        ]
    ]
    if not editor_filename:
        layout += [[Text('Configure editor in the Global settings to enable "Take me to error" feature')]]
    window = Window(title, layout, keep_on_top=True)

    while True:
        event, values = window.read()
        if event in ('Close', WIN_CLOSED):
            break
        if event == 'Kill Application':
            window.close()
            popup_quick_message(
                'KILLING APP!  BYE!',
                font='_ 18',
                keep_on_top=True,
                text_color='white',
                background_color='red',
                non_blocking=False,
            )
            sys.exit()
        if event == 'Take me to error' and filename is not None and line_num is not None:
            execute_editor(filename, line_num)

    window.close()


def _exit_mainloop(exiting_window):
    if exiting_window == Window._window_running_mainloop or Window._root_running_mainloop == Window.hidden_master_root:
        Window._window_that_exited = exiting_window
        if Window._root_running_mainloop is not None:
            Window._root_running_mainloop.quit()
        # print('** Exited window mainloop **')


from FreeSimpleGUI import _random_error_emoji
from FreeSimpleGUI import execute_editor
from FreeSimpleGUI import execute_get_editor
from FreeSimpleGUI import popup_quick_message
from FreeSimpleGUI import SUPPRESS_ERROR_POPUPS
from FreeSimpleGUI import WIN_CLOSED
from FreeSimpleGUI.elements.button import Button
from FreeSimpleGUI.elements.image import Image
from FreeSimpleGUI.elements.text import Text
from FreeSimpleGUI.window import Window
