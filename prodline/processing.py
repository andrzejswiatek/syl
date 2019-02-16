import numpy as np
import cv2
from skimage import img_as_float
from skimage.feature import canny
from skimage.color import rgb2grey
from skimage.transform import (probabilistic_hough_line)

from prodline.context import DrawingContext


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

    def apply_parameters(self, **parameters):
        pass

    def process(self, thresh):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [c for c in contours if c.size > 200]
        self.contours = contours
        rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
        contours_top = []
        contours_bottom = []
        for c in contours:
            left_most = tuple(c[c[:, :, 0].argmin()][0])
            right_most = tuple(c[c[:, :, 0].argmax()][0])
            top_most = tuple(c[c[:, :, 1].argmin()][0])
            bottom_most = tuple(c[c[:, :, 1].argmax()][0])

            if left_most[1] > thresh.shape[1]/2:
                contours_bottom.append(c)
            else:
                contours_top.append(c)
            if left_most[0] > 0:
                left_most = (0, left_most[1])
            if right_most[0] < thresh.shape[1]:
                right_most = (thresh.shape[1], right_most[1])

            left_top = (min(0, left_most[0]), top_most[1])
            right_top = (max(thresh.shape[1], right_most[0]), top_most[1])
            left_bottom = (min(0, left_most[0]), bottom_most[1])
            right_bottom = (max(thresh.shape[1], right_most[0]), bottom_most[1])
            print(left_most, right_most, top_most, bottom_most)

            cv2.circle(rgb, left_top, 8, (0, 0, 255), -1)
            cv2.circle(rgb, right_top, 8, (0, 0, 255), -1)
            cv2.circle(rgb, left_bottom, 8, (0, 0, 255), -1)
            cv2.circle(rgb, right_bottom, 8, (0, 0, 255), -1)

            cv2.line(rgb, left_top, right_top, (255, 255, 0), 2)
            cv2.line(rgb, left_bottom, right_bottom, (255, 255, 0), 2)

            cv2.putText(rgb, 'TM', top_most, cv2.FONT_HERSHEY_SIMPLEX ,1., (0, 255, 255))
            cv2.putText(rgb, 'RM', right_most, cv2.FONT_HERSHEY_SIMPLEX, 1., (0, 255, 255))
            cv2.putText(rgb, 'BM', bottom_most, cv2.FONT_HERSHEY_SIMPLEX, 1., (0, 255, 255))
            cv2.putText(rgb, 'LM', left_most, cv2.FONT_HERSHEY_SIMPLEX, 1., (0, 255, 255))

            cv2.circle(rgb, left_most, 8, (0, 255, 255), -1)
            cv2.circle(rgb, right_most, 8, (0, 255, 255), -1)
            cv2.circle(rgb, top_most, 8, (0, 255, 255), -1)
            cv2.circle(rgb, bottom_most, 8, (0, 255, 255), -1)
        cv2.drawContours(rgb, contours_top, -1, (0, 255, 0), 2)
        cv2.drawContours(rgb, contours_bottom, -1, (255, 0, 255), 2)

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
                #new_frame = self.processor.process(frame)
                #self.painter.draw(new_frame)
                #self.painter.draw(frame)
                self.painter.on_change(0)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    