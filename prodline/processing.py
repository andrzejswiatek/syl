import numpy as np
import cv2

class Processor(object):
    def __init__(self, input_image):
        self.input_image = input_image
        self.hsv = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2HSV)

    def apply_color_filter_using(self, rgb_start, rgb_end):
        lower = np.array(rgb_start, dtype="uint8")
        upper = np.array(rgb_end, dtype="uint8")
        mask = cv2.inRange(self.hsv, lower, upper)
        output = cv2.bitwise_and(self.input_image, self.input_image, mask=mask)
        return output

    def find_contours(self):
        pass