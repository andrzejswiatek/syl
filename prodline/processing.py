import numpy as np
import cv2

class Processor(object):
    def process(self, image):
        pass

    def apply_parameters(self, **parameters):
        pass

class ColorFilterProcessor(Processor):
    def __init__(self):
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

class LineProcessor(ColorFilterProcessor):
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
        return AggregateProcessor(ColorFilterProcessor(), LineProcessor())

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
        ret, frame = self.cap.read()
        self.painter.assign(frame)
        with self.painter:
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break
                frame = np.rot90(frame)
                self.painter.assign(frame)
                new_frame = self.processor.process(frame)
                self.painter.draw(new_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    