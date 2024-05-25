from __future__ import annotations

import tkinter as tk
from math import floor

from FreeSimpleGUI import COLOR_SYSTEM_DEFAULT
from FreeSimpleGUI import ELEM_TYPE_GRAPH
from FreeSimpleGUI import Element
from FreeSimpleGUI import TEXT_LOCATION_CENTER
from FreeSimpleGUI._utils import _error_popup_with_traceback
from FreeSimpleGUI._utils import _exit_mainloop


class Graph(Element):
    """
    Creates an area for you to draw on.  The MAGICAL property this Element has is that you interact
    with the element using your own coordinate system.  This is an important point!!  YOU define where the location
    is for (0,0).  Want (0,0) to be in the middle of the graph like a math 4-quadrant graph?  No problem!  Set your
    lower left corner to be (-100,-100) and your upper right to be (100,100) and you've got yourself a graph with
    (0,0) at the center.
    One of THE coolest of the Elements.
    You can also use float values. To do so, be sure and set the float_values parameter.
    Mouse click and drag events are possible and return the (x,y) coordinates of the mouse
    Drawing primitives return an "id" that is referenced when you want to operation on that item (e.g. to erase it)
    """

    def __init__(
        self,
        canvas_size,
        graph_bottom_left,
        graph_top_right,
        background_color=None,
        pad=None,
        p=None,
        change_submits=False,
        drag_submits=False,
        enable_events=False,
        motion_events=False,
        key=None,
        k=None,
        tooltip=None,
        right_click_menu=None,
        expand_x=False,
        expand_y=False,
        visible=True,
        float_values=False,
        border_width=0,
        metadata=None,
    ):
        """
        :param canvas_size:       size of the canvas area in pixels
        :type canvas_size:        (int, int)
        :param graph_bottom_left: (x,y) The bottoms left corner of your coordinate system
        :type graph_bottom_left:  (int, int)
        :param graph_top_right:   (x,y) The top right corner of  your coordinate system
        :type graph_top_right:    (int, int)
        :param background_color:  background color of the drawing area
        :type background_color:   (str)
        :param pad:               Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
        :type pad:                (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param p:                 Same as pad parameter.  It's an alias. If EITHER of them are set, then the one that's set will be used. If BOTH are set, pad will be used
        :type p:                  (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
        :param change_submits:    * DEPRICATED DO NOT USE. Use `enable_events` instead
        :type change_submits:     (bool)
        :param drag_submits:      if True and Events are enabled for the Graph, will report Events any time the mouse moves while button down.  When the mouse button is released, you'll get an event = graph key + '+UP' (if key is a string.. if not a string, it'll be made into a tuple)
        :type drag_submits:       (bool)
        :param enable_events:     If True then clicks on the Graph are immediately reported as an event. Use this instead of change_submits
        :type enable_events:      (bool)
        :param motion_events:     If True then if no button is down and the mouse is moved, an event is generated with key = graph key + '+MOVE' (if key is a string, it not a string then a tuple is returned)
        :type motion_events:      (bool)
        :param key:               Value that uniquely identifies this element from all other elements. Used when Finding an element or in return values. Must be unique to the window
        :type key:                str | int | tuple | object
        :param k:                 Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k:                  str | int | tuple | object
        :param tooltip:           text, that will appear when mouse hovers over the element
        :type tooltip:            (str)
        :param right_click_menu:  A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type right_click_menu:   List[List[ List[str] | str ]]
        :param expand_x:          If True the element will automatically expand in the X direction to fill available space
        :type expand_x:           (bool)
        :param expand_y:          If True the element will automatically expand in the Y direction to fill available space
        :type expand_y:           (bool)
        :param visible:           set visibility state of the element (Default = True)
        :type visible:            (bool)
        :param float_values:      If True x,y coordinates are returned as floats, not ints
        :type float_values:       (bool)
        :param border_width:      width of border around element in pixels. Not normally used for Graph Elements
        :type border_width:       (int)
        :param metadata:          User metadata that can be set to ANYTHING
        :type metadata:           (Any)
        """

        self.CanvasSize = canvas_size
        self.BottomLeft = graph_bottom_left
        self.TopRight = graph_top_right
        # self._TKCanvas = None               # type: tk.Canvas
        self._TKCanvas2 = self.Widget = None  # type: tk.Canvas
        self.ChangeSubmits = change_submits or enable_events
        self.DragSubmits = drag_submits
        self.ClickPosition = (None, None)
        self.MouseButtonDown = False
        self.Images = {}
        self.RightClickMenu = right_click_menu
        self.FloatValues = float_values
        self.BorderWidth = border_width
        key = key if key is not None else k
        pad = pad if pad is not None else p
        self.expand_x = expand_x
        self.expand_y = expand_y
        self.motion_events = motion_events

        super().__init__(
            ELEM_TYPE_GRAPH,
            background_color=background_color,
            size=canvas_size,
            pad=pad,
            key=key,
            tooltip=tooltip,
            visible=visible,
            metadata=metadata,
        )
        return

    def _convert_xy_to_canvas_xy(self, x_in, y_in):
        """
        Not user callable.  Used to convert user's coordinates into the ones used by tkinter
        :param x_in: The x coordinate to convert
        :type x_in:  int | float
        :param y_in: The y coordinate to convert
        :type y_in:  int | float
        :return:     (int, int) The converted canvas coordinates
        :rtype:      (int, int)
        """
        if None in (x_in, y_in):
            return None, None
        try:
            scale_x = (self.CanvasSize[0] - 0) / (self.TopRight[0] - self.BottomLeft[0])
            scale_y = (0 - self.CanvasSize[1]) / (self.TopRight[1] - self.BottomLeft[1])
        except:
            scale_x = scale_y = 0

        new_x = 0 + scale_x * (x_in - self.BottomLeft[0])
        new_y = self.CanvasSize[1] + scale_y * (y_in - self.BottomLeft[1])
        return new_x, new_y

    def _convert_canvas_xy_to_xy(self, x_in, y_in):
        """
        Not user callable.  Used to convert tkinter Canvas coords into user's coordinates

        :param x_in: The x coordinate in canvas coordinates
        :type x_in:  (int)
        :param y_in: (int) The y coordinate in canvas coordinates
        :type y_in:
        :return:     The converted USER coordinates
        :rtype:      (int, int) | Tuple[float, float]
        """
        if None in (x_in, y_in):
            return None, None
        scale_x = (self.CanvasSize[0] - 0) / (self.TopRight[0] - self.BottomLeft[0])
        scale_y = (0 - self.CanvasSize[1]) / (self.TopRight[1] - self.BottomLeft[1])

        new_x = x_in / scale_x + self.BottomLeft[0]
        new_y = (y_in - self.CanvasSize[1]) / scale_y + self.BottomLeft[1]
        if self.FloatValues:
            return new_x, new_y
        else:
            return floor(new_x), floor(new_y)

    def draw_line(self, point_from, point_to, color='black', width=1):
        """
        Draws a line from one point to another point using USER'S coordinates. Can set the color and width of line
        :param point_from: Starting point for line
        :type point_from:  (int, int) | Tuple[float, float]
        :param point_to:   Ending point for line
        :type point_to:    (int, int) | Tuple[float, float]
        :param color:      Color of the line
        :type color:       (str)
        :param width:      width of line in pixels
        :type width:       (int)
        :return:           id returned from tktiner or None if user closed the window. id is used when you
        :rtype:            int | None
        """
        if point_from == (None, None):
            return
        converted_point_from = self._convert_xy_to_canvas_xy(point_from[0], point_from[1])
        converted_point_to = self._convert_xy_to_canvas_xy(point_to[0], point_to[1])
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        try:  # in case window was closed with an X
            id = self._TKCanvas2.create_line(converted_point_from, converted_point_to, width=width, fill=color)
        except:
            id = None
        return id

    def draw_lines(self, points, color='black', width=1):
        """
        Draw a series of lines given list of points

        :param points: list of points that define the polygon
        :type points:  List[(int, int) | Tuple[float, float]]
        :param color:  Color of the line
        :type color:   (str)
        :param width:  width of line in pixels
        :type width:   (int)
        :return:       id returned from tktiner or None if user closed the window. id is used when you
        :rtype:        int | None
        """
        converted_points = [self._convert_xy_to_canvas_xy(point[0], point[1]) for point in points]

        try:  # in case window was closed with an X
            id = self._TKCanvas2.create_line(*converted_points, width=width, fill=color)
        except:
            if self._TKCanvas2 is None:
                print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
                print('Call Window.Finalize() prior to this operation')
            id = None
        return id

    def draw_point(self, point, size=2, color='black'):
        """
        Draws a "dot" at the point you specify using the USER'S coordinate system
        :param point: Center location using USER'S coordinate system
        :type point:  (int, int) | Tuple[float, float]
        :param size:  Radius? (Or is it the diameter?) in user's coordinate values.
        :type size:   int | float
        :param color: color of the point to draw
        :type color:  (str)
        :return:      id returned from tkinter that you'll need if you want to manipulate the point
        :rtype:       int | None
        """
        if point == (None, None):
            return
        converted_point = self._convert_xy_to_canvas_xy(point[0], point[1])
        size_converted = self._convert_xy_to_canvas_xy(point[0] + size, point[1])
        size = size_converted[0] - converted_point[0]
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        try:  # needed in case window was closed with an X
            point1 = converted_point[0] - size // 2, converted_point[1] - size // 2
            point2 = converted_point[0] + size // 2, converted_point[1] + size // 2
            id = self._TKCanvas2.create_oval(point1[0], point1[1], point2[0], point2[1], width=0, fill=color, outline=color)
        except:
            id = None
        return id

    def draw_circle(self, center_location, radius, fill_color=None, line_color='black', line_width=1):
        """
        Draws a circle, cenetered at the location provided.  Can set the fill and outline colors
        :param center_location: Center location using USER'S coordinate system
        :type center_location:  (int, int) | Tuple[float, float]
        :param radius:          Radius in user's coordinate values.
        :type radius:           int | float
        :param fill_color:      color of the point to draw
        :type fill_color:       (str)
        :param line_color:      color of the outer line that goes around the circle (sorry, can't set thickness)
        :type line_color:       (str)
        :param line_width:      width of the line around the circle, the outline, in pixels
        :type line_width:       (int)
        :return:                id returned from tkinter that you'll need if you want to manipulate the circle
        :rtype:                 int | None
        """
        if center_location == (None, None):
            return
        converted_point = self._convert_xy_to_canvas_xy(center_location[0], center_location[1])
        radius_converted = self._convert_xy_to_canvas_xy(center_location[0] + radius, center_location[1])
        radius = radius_converted[0] - converted_point[0]
        # radius = radius_converted[1]-5
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        try:  # needed in case the window was closed with an X
            id = self._TKCanvas2.create_oval(
                int(converted_point[0]) - int(radius),
                int(converted_point[1]) - int(radius),
                int(converted_point[0]) + int(radius),
                int(converted_point[1]) + int(radius),
                fill=fill_color,
                outline=line_color,
                width=line_width,
            )
        except:
            id = None
        return id

    def draw_oval(self, top_left, bottom_right, fill_color=None, line_color=None, line_width=1):
        """
        Draws an oval based on coordinates in user coordinate system. Provide the location of a "bounding rectangle"
        :param top_left:     the top left point of bounding rectangle
        :type top_left:      (int, int) | Tuple[float, float]
        :param bottom_right: the bottom right point of bounding rectangle
        :type bottom_right:  (int, int) | Tuple[float, float]
        :param fill_color:   color of the interrior
        :type fill_color:    (str)
        :param line_color:   color of outline of oval
        :type line_color:    (str)
        :param line_width:   width of the line around the oval, the outline, in pixels
        :type line_width:    (int)
        :return:             id returned from tkinter that you'll need if you want to manipulate the oval
        :rtype:              int | None
        """
        converted_top_left = self._convert_xy_to_canvas_xy(top_left[0], top_left[1])
        converted_bottom_right = self._convert_xy_to_canvas_xy(bottom_right[0], bottom_right[1])
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        try:  # in case windows close with X
            id = self._TKCanvas2.create_oval(
                converted_top_left[0],
                converted_top_left[1],
                converted_bottom_right[0],
                converted_bottom_right[1],
                fill=fill_color,
                outline=line_color,
                width=line_width,
            )
        except:
            id = None

        return id

    def draw_arc(self, top_left, bottom_right, extent, start_angle, style=None, arc_color='black', line_width=1, fill_color=None):
        """
        Draws different types of arcs.  Uses a "bounding box" to define location
        :param top_left:     the top left point of bounding rectangle
        :type top_left:      (int, int) | Tuple[float, float]
        :param bottom_right: the bottom right point of bounding rectangle
        :type bottom_right:  (int, int) | Tuple[float, float]
        :param extent:       Andle to end drawing. Used in conjunction with start_angle
        :type extent:        (float)
        :param start_angle:  Angle to begin drawing. Used in conjunction with extent
        :type start_angle:   (float)
        :param style:        Valid choices are One of these Style strings- 'pieslice', 'chord', 'arc', 'first', 'last', 'butt', 'projecting', 'round', 'bevel', 'miter'
        :type style:         (str)
        :param arc_color:    color to draw arc with
        :type arc_color:     (str)
        :param fill_color:   color to fill the area
        :type fill_color:    (str)
        :return:             id returned from tkinter that you'll need if you want to manipulate the arc
        :rtype:              int | None
        """
        converted_top_left = self._convert_xy_to_canvas_xy(top_left[0], top_left[1])
        converted_bottom_right = self._convert_xy_to_canvas_xy(bottom_right[0], bottom_right[1])
        tkstyle = tk.PIESLICE if style is None else style
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        try:  # in case closed with X
            id = self._TKCanvas2.create_arc(
                converted_top_left[0],
                converted_top_left[1],
                converted_bottom_right[0],
                converted_bottom_right[1],
                extent=extent,
                start=start_angle,
                style=tkstyle,
                outline=arc_color,
                width=line_width,
                fill=fill_color,
            )
        except Exception as e:
            print('Error encountered drawing arc.', e)
            id = None
        return id

    def draw_rectangle(self, top_left, bottom_right, fill_color=None, line_color=None, line_width=None):
        """
        Draw a rectangle given 2 points. Can control the line and fill colors

        :param top_left:     the top left point of rectangle
        :type top_left:      (int, int) | Tuple[float, float]
        :param bottom_right: the bottom right point of rectangle
        :type bottom_right:  (int, int) | Tuple[float, float]
        :param fill_color:   color of the interior
        :type fill_color:    (str)
        :param line_color:   color of outline
        :type line_color:    (str)
        :param line_width:   width of the line in pixels
        :type line_width:    (int)
        :return:             int | None id returned from tkinter that you'll need if you want to manipulate the rectangle
        :rtype:              int | None
        """

        converted_top_left = self._convert_xy_to_canvas_xy(top_left[0], top_left[1])
        converted_bottom_right = self._convert_xy_to_canvas_xy(bottom_right[0], bottom_right[1])
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        if line_width is None:
            line_width = 1
        try:  # in case closed with X
            id = self._TKCanvas2.create_rectangle(
                converted_top_left[0],
                converted_top_left[1],
                converted_bottom_right[0],
                converted_bottom_right[1],
                fill=fill_color,
                outline=line_color,
                width=line_width,
            )
        except:
            id = None
        return id

    def draw_polygon(self, points, fill_color=None, line_color=None, line_width=None):
        """
        Draw a polygon given list of points

        :param points:     list of points that define the polygon
        :type points:      List[(int, int) | Tuple[float, float]]
        :param fill_color: color of the interior
        :type fill_color:  (str)
        :param line_color: color of outline
        :type line_color:  (str)
        :param line_width: width of the line in pixels
        :type line_width:  (int)
        :return:           id returned from tkinter that you'll need if you want to manipulate the rectangle
        :rtype:            int | None
        """

        converted_points = [self._convert_xy_to_canvas_xy(point[0], point[1]) for point in points]
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        try:  # in case closed with X
            id = self._TKCanvas2.create_polygon(converted_points, fill=fill_color, outline=line_color, width=line_width)
        except:
            id = None
        return id

    def draw_text(self, text, location, color='black', font=None, angle=0, text_location=TEXT_LOCATION_CENTER):
        """
        Draw some text on your graph.  This is how you label graph number lines for example

        :param text:          text to display
        :type text:           (Any)
        :param location:      location to place first letter
        :type location:       (int, int) | Tuple[float, float]
        :param color:         text color
        :type color:          (str)
        :param font:          specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
        :type font:           (str or (str, int[, str]) or None)
        :param angle:         Angle 0 to 360 to draw the text.  Zero represents horizontal text
        :type angle:          (float)
        :param text_location: "anchor" location for the text. Values start with TEXT_LOCATION_
        :type text_location:  (enum)
        :return:              id returned from tkinter that you'll need if you want to manipulate the text
        :rtype:               int | None
        """
        text = str(text)
        if location == (None, None):
            return
        converted_point = self._convert_xy_to_canvas_xy(location[0], location[1])
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        try:  # in case closed with X
            id = self._TKCanvas2.create_text(
                converted_point[0],
                converted_point[1],
                text=text,
                font=font,
                fill=color,
                angle=angle,
                anchor=text_location,
            )
        except:
            id = None
        return id

    def draw_image(self, filename=None, data=None, location=(None, None)):
        """
        Places an image onto your canvas.  It's a really important method for this element as it enables so much

        :param filename: if image is in a file, path and filename for the image. (GIF and PNG only!)
        :type filename:  (str)
        :param data:     if image is in Base64 format or raw? format then use instead of filename
        :type data:      str | bytes
        :param location: the (x,y) location to place image's top left corner
        :type location:  (int, int) | Tuple[float, float]
        :return:         id returned from tkinter that you'll need if you want to manipulate the image
        :rtype:          int | None
        """
        if location == (None, None):
            return
        if filename is not None:
            image = tk.PhotoImage(file=filename)
        elif data is not None:
            # if type(data) is bytes:
            try:
                image = tk.PhotoImage(data=data)
            except:
                return None  # an error likely means the window has closed so exit
        converted_point = self._convert_xy_to_canvas_xy(location[0], location[1])
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        try:  # in case closed with X
            id = self._TKCanvas2.create_image(converted_point, image=image, anchor=tk.NW)
            self.Images[id] = image
        except:
            id = None
        return id

    def erase(self):
        """
        Erase the Graph - Removes all figures previously "drawn" using the Graph methods (e.g. DrawText)
        """
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        self.Images = {}
        try:  # in case window was closed with X
            self._TKCanvas2.delete('all')
        except:
            pass

    def delete_figure(self, id):
        """
        Remove from the Graph the figure represented by id. The id is given to you anytime you call a drawing primitive

        :param id: the id returned to you when calling one of the drawing methods
        :type id:  (int)
        """
        try:
            self._TKCanvas2.delete(id)
        except:
            print(f'DeleteFigure - bad ID {id}')
        try:
            del self.Images[id]  # in case was an image. If wasn't an image, then will get exception
        except:
            pass

    def update(self, background_color=None, visible=None):
        """
        Changes some of the settings for the Graph Element. Must call `Window.Read` or `Window.Finalize` prior

        Changes will not be visible in your window until you call window.read or window.refresh.

        If you change visibility, your element may MOVE. If you want it to remain stationary, use the "layout helper"
        function "pin" to ensure your element is "pinned" to that location in your layout so that it returns there
        when made visible.

        :param background_color: color of background
        :type background_color:  ???
        :param visible:          control visibility of element
        :type visible:           (bool)
        """
        if not self._widget_was_created():  # if widget hasn't been created yet, then don't allow
            return

        if self._this_elements_window_closed():
            _error_popup_with_traceback('Error in Graph.update - The window was closed')
            return

        if background_color is not None and background_color != COLOR_SYSTEM_DEFAULT:
            self._TKCanvas2.configure(background=background_color)

        if visible is False:
            self._pack_forget_save_settings()
        elif visible is True:
            self._pack_restore_settings()

        if visible is not None:
            self._visible = visible

    def move(self, x_direction, y_direction):
        """
        Moves the entire drawing area (the canvas) by some delta from the current position.  Units are indicated in your coordinate system indicated number of ticks in your coordinate system

        :param x_direction: how far to move in the "X" direction in your coordinates
        :type x_direction:  int | float
        :param y_direction: how far to move in the "Y" direction in your coordinates
        :type y_direction:  int | float
        """
        zero_converted = self._convert_xy_to_canvas_xy(0, 0)
        shift_converted = self._convert_xy_to_canvas_xy(x_direction, y_direction)
        shift_amount = (shift_converted[0] - zero_converted[0], shift_converted[1] - zero_converted[1])
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        self._TKCanvas2.move('all', shift_amount[0], shift_amount[1])

    def move_figure(self, figure, x_direction, y_direction):
        """
        Moves a previously drawn figure using a "delta" from current position

        :param figure:      Previously obtained figure-id. These are returned from all Draw methods
        :type figure:       (id)
        :param x_direction: delta to apply to position in the X direction
        :type x_direction:  int | float
        :param y_direction: delta to apply to position in the Y direction
        :type y_direction:  int | float
        """
        zero_converted = self._convert_xy_to_canvas_xy(0, 0)
        shift_converted = self._convert_xy_to_canvas_xy(x_direction, y_direction)
        shift_amount = (shift_converted[0] - zero_converted[0], shift_converted[1] - zero_converted[1])
        if figure is None:
            print('* move_figure warning - your figure is None *')
            return None
        self._TKCanvas2.move(figure, shift_amount[0], shift_amount[1])

    def relocate_figure(self, figure, x, y):
        """
        Move a previously made figure to an arbitrary (x,y) location. This differs from the Move methods because it
        uses absolute coordinates versus relative for Move

        :param figure: Previously obtained figure-id. These are returned from all Draw methods
        :type figure:  (id)
        :param x:      location on X axis (in user coords) to move the upper left corner of the figure
        :type x:       int | float
        :param y:      location on Y axis (in user coords) to move the upper left corner of the figure
        :type y:       int | float
        """

        # zero_converted = self._convert_xy_to_canvas_xy(0, 0)
        shift_converted = self._convert_xy_to_canvas_xy(x, y)
        # shift_amount = (shift_converted[0] - zero_converted[0], shift_converted[1] - zero_converted[1])
        if figure is None:
            print('*** WARNING - Your figure is None. It most likely means your did not Finalize your Window ***')
            print('Call Window.Finalize() prior to all graph operations')
            return None
        xy = self._TKCanvas2.coords(figure)
        self._TKCanvas2.move(figure, shift_converted[0] - xy[0], shift_converted[1] - xy[1])

    def send_figure_to_back(self, figure):
        """
        Changes Z-order of figures on the Graph.  Sends the indicated figure to the back of all other drawn figures

        :param figure: value returned by tkinter when creating the figure / drawing
        :type figure:  (int)
        """
        self.TKCanvas.tag_lower(figure)  # move figure to the "bottom" of all other figure

    def bring_figure_to_front(self, figure):
        """
        Changes Z-order of figures on the Graph.  Brings the indicated figure to the front of all other drawn figures

        :param figure: value returned by tkinter when creating the figure / drawing
        :type figure:  (int)
        """
        self.TKCanvas.tag_raise(figure)  # move figure to the "top" of all other figures

    def get_figures_at_location(self, location):
        """
        Returns a list of figures located at a particular x,y location within the Graph

        :param location: point to check
        :type location:  (int, int) | Tuple[float, float]
        :return:         a list of previously drawn "Figures" (returned from the drawing primitives)
        :rtype:          List[int]
        """
        x, y = self._convert_xy_to_canvas_xy(location[0], location[1])
        ids = self.TKCanvas.find_overlapping(x, y, x, y)
        return ids

    def get_bounding_box(self, figure):
        """
        Given a figure, returns the upper left and lower right bounding box coordinates

        :param figure: a previously drawing figure
        :type figure:  object
        :return:       upper left x, upper left y, lower right x, lower right y
        :rtype:        Tuple[int, int, int, int] | Tuple[float, float, float, float]
        """
        box = self.TKCanvas.bbox(figure)
        top_left = self._convert_canvas_xy_to_xy(box[0], box[1])
        bottom_right = self._convert_canvas_xy_to_xy(box[2], box[3])
        return top_left, bottom_right

    def change_coordinates(self, graph_bottom_left, graph_top_right):
        """
        Changes the corrdinate system to a new one.  The same 2 points in space are used to define the coorinate
        system - the bottom left and the top right values of your graph.

        :param graph_bottom_left: The bottoms left corner of your coordinate system
        :type graph_bottom_left:  (int, int) (x,y)
        :param graph_top_right:   The top right corner of  your coordinate system
        :type graph_top_right:    (int, int)  (x,y)
        """
        self.BottomLeft = graph_bottom_left
        self.TopRight = graph_top_right

    @property
    def tk_canvas(self):
        """
        Returns the underlying tkiner Canvas widget

        :return: The tkinter canvas widget
        :rtype:  (tk.Canvas)
        """
        if self._TKCanvas2 is None:
            print('*** Did you forget to call Finalize()? Your code should look something like: ***')
            print('*** form = sg.Window("My Form").Layout(layout).Finalize() ***')
        return self._TKCanvas2

    # button release callback
    def button_release_call_back(self, event):
        """
        Not a user callable method.  Used to get Graph click events. Called by tkinter when button is released

        :param event: (event) event info from tkinter. Note not used in this method
        :type event:
        """
        if not self.DragSubmits:
            return  # only report mouse up for drag operations
        self.ClickPosition = self._convert_canvas_xy_to_xy(event.x, event.y)
        self.ParentForm.LastButtonClickedWasRealtime = False
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = '__GRAPH__'  # need to put something rather than None
        _exit_mainloop(self.ParentForm)
        if isinstance(self.ParentForm.LastButtonClicked, str):
            self.ParentForm.LastButtonClicked = self.ParentForm.LastButtonClicked + '+UP'
        else:
            self.ParentForm.LastButtonClicked = (self.ParentForm.LastButtonClicked, '+UP')
        self.MouseButtonDown = False

    # button callback
    def button_press_call_back(self, event):
        """
        Not a user callable method.  Used to get Graph click events. Called by tkinter when button is released

        :param event: (event) event info from tkinter. Contains the x and y coordinates of a click
        :type event:
        """

        self.ClickPosition = self._convert_canvas_xy_to_xy(event.x, event.y)
        self.ParentForm.LastButtonClickedWasRealtime = self.DragSubmits
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = '__GRAPH__'  # need to put something rather than None
        _exit_mainloop(self.ParentForm)
        self.MouseButtonDown = True

    def _update_position_for_returned_values(self, event):
        """
        Updates the variable that's used when the values dictionary is returned from a window read.

        Not called by the user.  It's called from another method/function that tkinter calledback

        :param event: (event) event info from tkinter. Contains the x and y coordinates of a click
        :type event:
        """
        """
        Updates the variable that's used when the values dictionary is returned from a window read.

        Not called by the user.  It's called from another method/function that tkinter calledback

        :param event: (event) event info from tkinter. Contains the x and y coordinates of a click
        :type event:
        """

        self.ClickPosition = self._convert_canvas_xy_to_xy(event.x, event.y)

    # button callback
    def motion_call_back(self, event):
        """
        Not a user callable method.  Used to get Graph mouse motion events. Called by tkinter when mouse moved

        :param event: (event) event info from tkinter. Contains the x and y coordinates of a mouse
        :type event:
        """

        if not self.MouseButtonDown and not self.motion_events:
            return
        self.ClickPosition = self._convert_canvas_xy_to_xy(event.x, event.y)
        self.ParentForm.LastButtonClickedWasRealtime = self.DragSubmits
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = '__GRAPH__'  # need to put something rather than None
        if self.motion_events and not self.MouseButtonDown:
            if isinstance(self.ParentForm.LastButtonClicked, str):
                self.ParentForm.LastButtonClicked = self.ParentForm.LastButtonClicked + '+MOVE'
            else:
                self.ParentForm.LastButtonClicked = (self.ParentForm.LastButtonClicked, '+MOVE')
        _exit_mainloop(self.ParentForm)

    BringFigureToFront = bring_figure_to_front
    ButtonPressCallBack = button_press_call_back
    ButtonReleaseCallBack = button_release_call_back
    DeleteFigure = delete_figure
    DrawArc = draw_arc
    DrawCircle = draw_circle
    DrawImage = draw_image
    DrawLine = draw_line
    DrawOval = draw_oval
    DrawPoint = draw_point
    DrawPolygon = draw_polygon
    DrawLines = draw_lines
    DrawRectangle = draw_rectangle
    DrawText = draw_text
    GetFiguresAtLocation = get_figures_at_location
    GetBoundingBox = get_bounding_box
    Erase = erase
    MotionCallBack = motion_call_back
    Move = move
    MoveFigure = move_figure
    RelocateFigure = relocate_figure
    SendFigureToBack = send_figure_to_back
    TKCanvas = tk_canvas
    Update = update
