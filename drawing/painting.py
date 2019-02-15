import cv2
import pickle
import os

class Painter(object):
    track_bar_rgb_min_red = ("rgb_min_red", 40)
    track_bar_rgb_min_green = ("rgb_min_green", 40)
    track_bar_rgb_min_blue = ("rgb_min_blue", 70)
    track_bar_rgb_max_red = ("rgb_max_red", 100)
    track_bar_rgb_max_green = ("rgb_max_green", 210)
    track_bar_rgb_max_blue = ("rgb_max_blue", 210)

    track_bars = [track_bar_rgb_min_red,
                  track_bar_rgb_min_green,
                  track_bar_rgb_min_blue,
                  track_bar_rgb_max_red,
                  track_bar_rgb_max_green,
                  track_bar_rgb_max_blue]

    def __init__(self, window_name, serialize_file, on_change):
        self.image = None
        self.on_change = on_change
        self.serialize_file = serialize_file
        self.window_name = window_name
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

    def __enter__(self):
        self.add_track_bars()
        self.load_values()

    def __exit__(self, exc_type, exc_val, exc_tb):
        cv2.destroyAllWindows()

    def create_track_bar(self, name, value, maximum, handler):
        cv2.createTrackbar(name, self.window_name, value, maximum, handler)

    def draw(self, image):
        self.image = image
        cv2.imshow(self.window_name, self.image)

    def get_value(self, track_bar_name):
        result = cv2.getTrackbarPos(track_bar_name, self.window_name)
        return result

    def set_value(self, track_bar_name, value):
        return cv2.setTrackbarPos(track_bar_name, self.window_name, value)

    def save_values(self):
        values = {}
        for bar in Painter.track_bars:
            bar_name = bar[0]
            result = self.get_value(bar_name)
            values[bar_name] = result
        with open(self.serialize_file, 'wb') as f:
            pickle.dump(values, f)

    def load_values(self):
        if not os.path.exists(self.serialize_file):
            return
        with open(self.serialize_file, 'rb') as f:
            values = pickle.load(f)
        for value in values:
            self.set_value(value, values[value])

    def add_track_bars(self):
        for bar in Painter.track_bars:
            self.create_track_bar(bar[0], bar[1], 255, self.on_change)

    def on_change_value(self, processor, val):
        if self.image is None:
            return
        rgb_begin = [self.get_value(Painter.track_bar_rgb_min_red[0]),
                     self.get_value(Painter.track_bar_rgb_min_green[0]),
                     self.get_value(Painter.track_bar_rgb_min_blue[0])]
        rgb_end = [self.get_value(Painter.track_bar_rgb_max_red[0]),
                   self.get_value(Painter.track_bar_rgb_max_green[0]),
                   self.get_value(Painter.track_bar_rgb_max_blue[0])]
        out = processor.apply_color_filter_using(self.image, rgb_begin, rgb_end)
        self.save_values()
        self.draw(out)
