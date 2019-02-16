import numpy as np
import cv2
from skimage.feature import canny
from skimage.transform import (probabilistic_hough_line)
from prodline.context import DrawingContext
from prodline.measurement import Line


class Processor(object):
    def process(self, image):
        pass

    def apply_parameters(self, **parameters):
        pass

class ColorFilterProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.lower = np.array([40, 40, 70], dtype="uint8")
        self.upper = np.array([100, 210, 210], dtype="uint8")

    def apply_parameters(self, **parameters):
        rgb_begin = parameters.get('rgb_begin')
        rgb_end = parameters.get('rgb_end')
        if rgb_begin is not None:
            self.lower = np.array(rgb_begin, dtype="uint8")
        if rgb_end is not None:
            self.upper = np.array(rgb_end, dtype="uint8")


    def process(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower, self.upper)
        output = cv2.bitwise_and(image, image, mask=mask)
        return output

class LineProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.min_line_length = 100
        self.max_line_length = 200
        self.max_line_gap = 10
        self.aperture_size = 5

    def apply_parameters(self, **parameters):
        self.min_line_length = parameters.get('min_line_length', self.min_line_length)
        self.max_line_length = parameters.get('max_line_length', self.max_line_length)
        self.max_line_gap = parameters.get('max_line_gap', self.max_line_gap)
        self.aperture_size = parameters.get('aperture_size', self.aperture_size)

    def process(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, self.min_line_length, self.max_line_length, apertureSize=self.aperture_size)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, self.min_line_length, self.max_line_gap)
        if lines is not None:
            for x1, y1, x2, y2 in lines[0]:
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return image

class EdgesProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.max_line_length = 100
        self.max_line_gap = 50
        self.canny_sigma = 1

    def apply_parameters(self, **parameters):
        self.max_line_length = parameters.get('max_line_length', self.max_line_length)
        self.max_line_gap = parameters.get('max_line_gap', self.max_line_gap)
        self.canny_sigma = parameters.get('canny_sigma', self.canny_sigma)

    def process(self, image):
        edges = canny(image, self.canny_sigma)
        lines = probabilistic_hough_line(edges, line_length=self.max_line_length, line_gap=self.max_line_gap)
        for line in lines:
            p0, p1 = line
            cv2.line(image, (p0[0], p1[0]), (p0[1], p1[1]), (0, 255, 0), 2)
        return image

class ThresholdProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.threshold_val = 127
        self.threshold_max = 255
        self.threshold_method = cv2.THRESH_BINARY

    def apply_parameters(self, **parameters):
        self.threshold_val = parameters.get('threshold_val', self.threshold_val)
        self.threshold_max = parameters.get('threshold_max', self.threshold_max)

    def process(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, self.threshold_val, self.threshold_max, self.threshold_method)
        return thresh

class ContourProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.contours = None
        self.min_contour_size = 100
        self.contour_sizes = {}
        self.draw_contours = False

    def apply_parameters(self, **parameters):
        pass

    def __assign(self, thresh, c, area):
        if c.size < self.contour_sizes.get(area, 0):
            return
        self.contour_sizes[area] = c.size
        area.contours.append(c)
        area.left_most = tuple(c[c[:, :, 0].argmin()][0])
        area.right_most = tuple(c[c[:, :, 0].argmax()][0])
        area.top_most = tuple(c[c[:, :, 1].argmin()][0])
        area.bottom_most = tuple(c[c[:, :, 1].argmax()][0])
        if area.left_most[0] > 0:
            area.left_most = (0, area.left_most[1])
        if area.right_most[0] < thresh.shape[1]:
            area.right_most = (thresh.shape[1], area.right_most[1])
        area.left_top = (min(0, area.left_most[0]), area.top_most[1])
        area.right_top = (max(thresh.shape[1], area.right_most[0]), area.top_most[1])
        area.left_bottom = (min(0, area.left_most[0]), area.bottom_most[1])
        area.right_bottom = (max(thresh.shape[1], area.right_most[0]), area.bottom_most[1])

    def __get_line_information(self, contours, thresh):
        line = Line()
        for c in contours:
            left_most = tuple(c[c[:, :, 0].argmin()][0])
            if left_most[1] > thresh.shape[1] / 2:
                self.__assign(thresh, c, line.area_top)
            else:
                self.__assign(thresh, c, line.area_bottom)
        return line

    def __draw_area(self, rgb, area, color):
        cv2.circle(rgb, area.left_top, 8, color, -1)
        cv2.circle(rgb, area.right_top, 8, color, -1)
        cv2.circle(rgb, area.left_bottom, 8, color, -1)
        cv2.circle(rgb, area.right_bottom, 8, color, -1)

        cv2.line(rgb, area.left_top, area.right_top, color, 2)
        cv2.line(rgb, area.left_bottom, area.right_bottom, color, 2)

        nc = (200, 200, 50)
        cv2.putText(rgb, 'TM', area.top_most, cv2.FONT_HERSHEY_SIMPLEX, 1., nc)
        cv2.putText(rgb, 'RM', area.right_most, cv2.FONT_HERSHEY_SIMPLEX, 1., nc)
        cv2.putText(rgb, 'BM', area.bottom_most, cv2.FONT_HERSHEY_SIMPLEX, 1., nc)
        cv2.putText(rgb, 'LM', area.left_most, cv2.FONT_HERSHEY_SIMPLEX, 1., nc)

        cv2.circle(rgb, area.left_most, 8, nc, -1)
        cv2.circle(rgb, area.right_most, 8, nc, -1)
        cv2.circle(rgb, area.top_most, 8, nc, -1)
        cv2.circle(rgb, area.bottom_most, 8, nc, -1)
        if self.draw_contours:
            cv2.drawContours(rgb, area.contours, -1, color, 2)

    def process(self, thresh):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [c for c in contours if c.size > self.min_contour_size]
        self.contours = contours
        rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
        line = self.__get_line_information(contours, thresh)
        self.__draw_area(rgb, line.area_bottom, (255, 255, 0))
        self.__draw_area(rgb, line.area_top, (255, 0, 255))

        return rgb

class AggregateProcessor(Processor):
    def __init__(self, *processors):
        self.processors = processors

    def process(self, image):
        output = image
        for processor in self.processors:
            output = processor.process(output)
        return output

    def apply_parameters(self, **parameters):
        for processor in self.processors:
            processor.apply_parameters(**parameters)

class ProcessorFactory(object):
    def create(self):
        return AggregateProcessor(
            ColorFilterProcessor(),
            ThresholdProcessor(),
            ContourProcessor()
        )

class VideoProcessor(object):
    def __init__(self, video_file, processor, painter):
        self.video_file = video_file
        self.processor = processor
        self.painter = painter

    def __enter__(self):
        self.cap = cv2.VideoCapture(self.video_file)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cap.release()
        cv2.destroyAllWindows()

    def process(self):
        with self.painter:
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break
                frame = np.rot90(frame)
                DrawingContext.image = frame
                self.painter.on_change(0)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    