import cv2
import pickle
import os
from prodline.context import DrawingContext


class Painter(object):
    track_bar_rgb_min_red = ("rgb_min_red", 40, (0, 255))
    track_bar_rgb_min_green = ("rgb_min_green", 40, (0, 255))
    track_bar_rgb_min_blue = ("rgb_min_blue", 70, (0, 255))
    track_bar_rgb_max_red = ("rgb_max_red", 100, (0, 255))
    track_bar_rgb_max_green = ("rgb_max_green", 210, (0, 255))
    track_bar_rgb_max_blue = ("rgb_max_blue", 210, (0, 255))

    track_bar_min_line_length = ('min_line_length', 100, (0, 800))
    track_bar_max_line_length = ('max_line_length', 200, (0, 800))
    track_bar_max_line_gap = ('max_line_gap', 10, (10, 100))
    track_bar_aperture_size = ('aperture_size', 5, (3, 7))

    track_bar_threshold_val = ('threshold_val', 100, (0, 255))
    track_bar_threshold_max = ('threshold_max', 255, (0, 255))

    track_bars = [track_bar_rgb_min_red,
                  track_bar_rgb_min_green,
                  track_bar_rgb_min_blue,
                  track_bar_rgb_max_red,
                  track_bar_rgb_max_green,
                  track_bar_rgb_max_blue,
                  track_bar_min_line_length,
                  track_bar_max_line_length,
                  track_bar_max_line_gap,
                  track_bar_aperture_size,
                  track_bar_threshold_val,
                  track_bar_threshold_max
                  ]

    def __init__(self, window_name, serialize_file, processor):
        self.processor = processor
        self.serialize_file = serialize_file
        self.window_name = window_name
        self.input_window_name = 'Obraz wejsciowy'
        self.parameter_window = 'Parametry'
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.namedWindow(self.input_window_name, cv2.WINDOW_NORMAL)
        cv2.namedWindow(self.parameter_window, cv2.WINDOW_GUI_NORMAL)

    def __enter__(self):
        self.__add_track_bars()
        self.__load_values()
        self.on_change(0)

    def __exit__(self, exc_type, exc_val, exc_tb):
        cv2.destroyAllWindows()

    def create_track_bar(self, name, value, maximum, handler):
        cv2.createTrackbar(name, self.parameter_window, value, maximum, handler)

    def draw(self, image):
        cv2.imshow(self.window_name, image)
        cv2.imshow(self.input_window_name, DrawingContext.image)

    def get_value(self, track_bar_name):
        result = cv2.getTrackbarPos(track_bar_name, self.parameter_window)
        return result

    def set_value(self, track_bar_name, value):
        return cv2.setTrackbarPos(track_bar_name, self.parameter_window, value)

    def __save_values(self):
        values = {}
        for bar in Painter.track_bars:
            bar_name = bar[0]
            result = self.get_value(bar_name)
            values[bar_name] = result
        with open(self.serialize_file, 'wb') as f:
            pickle.dump(values, f)

    def __load_values(self):
        if not os.path.exists(self.serialize_file):
            return
        with open(self.serialize_file, 'rb') as f:
            values = pickle.load(f)
        for value in values:
            self.set_value(value, values[value])

    def __add_track_bars(self):
        for bar in Painter.track_bars:
            self.create_track_bar(bar[0], bar[2][0], bar[2][1], self.on_change)

    def on_change(self, value):
        self.__on_change_value(value)

    def __on_change_value(self, val):
        if DrawingContext.image is None:
            return
        rgb_begin = [self.get_value(Painter.track_bar_rgb_min_red[0]),
                     self.get_value(Painter.track_bar_rgb_min_green[0]),
                     self.get_value(Painter.track_bar_rgb_min_blue[0])]
        rgb_end = [self.get_value(Painter.track_bar_rgb_max_red[0]),
                   self.get_value(Painter.track_bar_rgb_max_green[0]),
                   self.get_value(Painter.track_bar_rgb_max_blue[0])]

        min_line_length = self.get_value(Painter.track_bar_min_line_length[0])
        max_line_length = self.get_value(Painter.track_bar_max_line_length[0])
        max_line_gap = self.get_value(Painter.track_bar_max_line_gap[0])
        aperture_size = self.get_value(Painter.track_bar_aperture_size[0])

        threshold_val = self.get_value(Painter.track_bar_threshold_val[0])
        threshold_max = self.get_value(Painter.track_bar_threshold_max[0])

        self.processor.apply_parameters(
            rgb_begin=rgb_begin,
            rgb_end=rgb_end,
            min_line_length=min_line_length,
            max_line_length=max_line_length,
            max_line_gap=max_line_gap,
            aperture_size=aperture_size,
            threshold_val=threshold_val,
            threshold_max=threshold_max
        )

        out = self.processor.process(DrawingContext.image)
        self.__save_values()
        self.draw(out)
