from __future__ import annotations

import time
import tkinter as tk
import warnings

from FreeSimpleGUI import ELEM_TYPE_IMAGE
from FreeSimpleGUI._utils import _error_popup_with_traceback
from FreeSimpleGUI.elements.base import Element


class Image(Element):
    """
    Image Element - show an image in the window. Should be a GIF or a PNG only
    """

    def __init__(
        self,
        source=None,
        filename=None,
        data=None,
        background_color=None,
        size=(None, None),
        s=(None, None),
        pad=None,
        p=None,
        key=None,
        k=None,
        tooltip=None,
        subsample=None,
        zoom=None,
        right_click_menu=None,
        expand_x=False,
        expand_y=False,
        visible=True,
        enable_events=False,
        metadata=None,
    ):
        """
        :param source:           A filename or a base64 bytes. Will automatically detect the type and fill in filename or data for you.
        :type source:            str | bytes | None
        :param filename:         image filename if there is a button image. GIFs and PNGs only.
        :type filename:          str | None
        :param data:             Raw or Base64 representation of the image to put on button. Choose either filename or data
        :type data:              bytes | str | None
        :param background_color: color of background
        :type background_color:
        :param size:             (width, height) size of image in pixels
        :type size:              (int, int)
        :param s:                Same as size parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, size will be used
        :type s:                 (int, int)  | (None, None) | int
        :param pad:              Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:               (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                 (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param key:              Used with window.find_element and with return values to uniquely identify this element to uniquely identify this element
        :type key:               str | int | tuple | object
        :param k:                Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                 str | int | tuple | object
        :param tooltip:          text, that will appear when mouse hovers over the element
        :type tooltip:           (str)
        :param subsample:        amount to reduce the size of the image. Divides the size by this number. 2=1/2, 3=1/3, 4=1/4, etc
        :type subsample:         (int)
        :param zoom:             amount to increase the size of the image.
        :type zoom:              (int)
        :param right_click_menu: A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type right_click_menu:  List[List[ List[str] | str ]]
        :param expand_x:         If True the element will automatically expand in the X direction to fill available space
        :type expand_x:          (bool)
        :param expand_y:         If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:          (bool)
        :param visible:          set visibility state of the element
        :type visible:           (bool)
        :param enable_events:    Turns on the element specific events. For an Image element, the event is "image clicked"
        :type enable_events:     (bool)
        :param metadata:         User metadata that can be set to ANYTHING
        :type metadata:          (Any)
        """

        if source is not None:
            if isinstance(source, bytes):
                data = source
            elif isinstance(source, str):
                filename = source
            else:
                warnings.warn(f'Image element - source is not a valid type: {type(source)}', UserWarning)

        self.Filename = filename
        self.Data = data
        self.Widget = self.tktext_label = None  # type: tk.Label
        self.BackgroundColor = background_color
        if data is None and filename is None:
            self.Filename = ''
        self.EnableEvents = enable_events
        self.RightClickMenu = right_click_menu
        self.AnimatedFrames = None
        self.CurrentFrameNumber = 0
        self.TotalAnimatedFrames = 0
        self.LastFrameTime = 0
        self.ImageSubsample = subsample
        self.zoom = int(zoom) if zoom is not None else None

        self.Source = filename if filename is not None else data
        key = key if key is not None else k
        sz = size if size != (None, None) else s
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y

        super().__init__(
            ELEM_TYPE_IMAGE,
            size=sz,
            background_color=background_color,
            pad=pad,
            key=key,
            tooltip=tooltip,
            visible=visible,
            metadata=metadata,
        )
        return

    def update(self, source=None, filename=None, data=None, size=(None, None), subsample=None, zoom=None, visible=None):
        """
        Changes some of the settings for the Image Element. Must call `Window.Read` or `Window.Finalize` prior.
        To clear an image that's been displayed, call with NONE of the options set.  A blank update call will
        delete the previously shown image.

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param source:   A filename or a base64 bytes. Will automatically detect the type and fill in filename or data for you.
        :type source:    str | bytes | None
        :param filename: filename to the new image to display.
        :type filename:  (str)
        :param data:     Base64 encoded string OR a tk.PhotoImage object
        :type data:      str | tkPhotoImage
        :param size:     (width, height) size of image in pixels
        :type size:      Tuple[int,int]
        :param subsample: amount to reduce the size of the image. Divides the size by this number. 2=1/2, 3=1/3, 4=1/4, etc
        :type subsample: (int)
        :param zoom:     amount to increase the size of the image
        :type zoom:      (int)
        :param visible:  control visibility of element
        :type visible:   (bool)
        """

        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Image.update - The window was closed')
            return

        if source is not None:
            if isinstance(source, bytes):
                data = source
            elif isinstance(source, str):
                filename = source
            else:
                warnings.warn(f'Image element - source is not a valid type: {type(source)}', UserWarning)

        image = None
        if filename is not None:
            try:
                image = tk.PhotoImage(file=filename)
                if subsample is not None:
                    image = image.subsample(subsample)
                if zoom is not None:
                    image = image.zoom(int(zoom))
            except Exception as e:
                _error_popup_with_traceback('Exception updating Image element', e)

        elif data is not None:
            # if type(data) is bytes:
            try:
                image = tk.PhotoImage(data=data)
                if subsample is not None:
                    image = image.subsample(subsample)
                if zoom is not None:
                    image = image.zoom(int(zoom))
            except Exception:
                image = data
                # return  # an error likely means the window has closed so exit

        if image is not None:
            self.tktext_label.configure(image='')  # clear previous image
            if self.tktext_label.image is not None:
                del self.tktext_label.image
            if type(image) is not bytes:
                width, height = (
                    size[0] if size[0] is not None else image.width(),
                    size[1] if size[1] is not None else image.height(),
                )
            else:
                width, height = size
            try:  # sometimes crashes if user closed with X
                self.tktext_label.configure(image=image, width=width, height=height)
            except Exception as e:
                _error_popup_with_traceback('Exception updating Image element', e)
            self.tktext_label.image = image
        if visible is False:
            self._pack_forget_save_settings()
        elif visible is True:
            self._pack_restore_settings()

        # if everything is set to None, then delete the image
        if filename is None and image is None and visible is None and size == (None, None):
            # Using a try because the image may have been previously deleted and don't want an error if that's happened
            try:
                self.tktext_label.configure(image='', width=1, height=1, bd=0)
                self.tktext_label.image = None
            except:
                pass

        if visible is not None:
            self._visible = visible

    def update_animation(self, source, time_between_frames=0):
        """
        Show an Animated GIF. Call the function as often as you like. The function will determine when to show the next frame and will automatically advance to the next frame at the right time.
        NOTE - does NOT perform a sleep call to delay
        :param source:              Filename or Base64 encoded string containing Animated GIF
        :type source:               str | bytes | None
        :param time_between_frames: Number of milliseconds to wait between showing frames
        :type time_between_frames:  (int)
        """

        if self.Source != source:
            self.AnimatedFrames = None
            self.Source = source

        if self.AnimatedFrames is None:
            self.TotalAnimatedFrames = 0
            self.AnimatedFrames = []
            # Load up to 1000 frames of animation.  stops when a bad frame is returns by tkinter
            for i in range(1000):
                if type(source) is not bytes:
                    try:
                        self.AnimatedFrames.append(tk.PhotoImage(file=source, format='gif -index %i' % (i)))
                    except Exception:
                        break
                else:
                    try:
                        self.AnimatedFrames.append(tk.PhotoImage(data=source, format='gif -index %i' % (i)))
                    except Exception:
                        break
            self.TotalAnimatedFrames = len(self.AnimatedFrames)
            self.LastFrameTime = time.time()
            self.CurrentFrameNumber = -1  # start at -1 because it is incremented before every frame is shown
        # show the frame

        now = time.time()

        if time_between_frames:
            if (now - self.LastFrameTime) * 1000 > time_between_frames:
                self.LastFrameTime = now
                self.CurrentFrameNumber = (self.CurrentFrameNumber + 1) % self.TotalAnimatedFrames
            else:  # don't reshow the frame again if not time for new frame
                return
        else:
            self.CurrentFrameNumber = (self.CurrentFrameNumber + 1) % self.TotalAnimatedFrames
        image = self.AnimatedFrames[self.CurrentFrameNumber]
        try:  # needed in case the window was closed with an "X"
            self.tktext_label.configure(image=image, width=image.width(), heigh=image.height())
        except Exception as e:
            print('Exception in update_animation', e)

    def update_animation_no_buffering(self, source, time_between_frames=0):
        """
        Show an Animated GIF. Call the function as often as you like. The function will determine when to show the next frame and will automatically advance to the next frame at the right time.
        NOTE - does NOT perform a sleep call to delay

        :param source:              Filename or Base64 encoded string containing Animated GIF
        :type source:               str | bytes
        :param time_between_frames: Number of milliseconds to wait between showing frames
        :type time_between_frames:  (int)
        """

        if self.Source != source:
            self.AnimatedFrames = None
            self.Source = source
            self.frame_num = 0

        now = time.time()

        if time_between_frames:
            if (now - self.LastFrameTime) * 1000 > time_between_frames:
                self.LastFrameTime = now
            else:  # don't reshow the frame again if not time for new frame
                return

        # read a frame
        while True:
            if type(source) is not bytes:
                try:
                    self.image = tk.PhotoImage(file=source, format='gif -index %i' % (self.frame_num))
                    self.frame_num += 1
                except:
                    self.frame_num = 0
            else:
                try:
                    self.image = tk.PhotoImage(data=source, format='gif -index %i' % (self.frame_num))
                    self.frame_num += 1
                except:
                    self.frame_num = 0
            if self.frame_num:
                break

        try:  # needed in case the window was closed with an "X"
            self.tktext_label.configure(image=self.image, width=self.image.width(), heigh=self.image.height())

        except:
            pass

    Update = update
    UpdateAnimation = update_animation
