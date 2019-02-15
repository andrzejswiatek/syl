import cv2

class Painter(object):
    def __init__(self, window_name):
        self.window_name = window_name
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_val, exc_tb):
        cv2.destroyAllWindows()

    def create_track_bar(self, name, value, maximum, handler):
        cv2.createTrackbar(name, self.window_name, value, maximum, handler)

    def draw(self, image):
        cv2.imshow(self.window_name, image)

    def get_value(self, track_bar_name):
        return cv2.getTrackbarPos(track_bar_name, self.window_name)