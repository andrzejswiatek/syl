import numpy as np
import cv2

class ImageProcessor(object):
    def apply_color_filter_using(self, input_image, rgb_start, rgb_end):
        hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)
        lower = np.array(rgb_start, dtype="uint8")
        upper = np.array(rgb_end, dtype="uint8")
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(input_image, input_image, mask=mask)
        return output

    def find_contours(self):
        pass
    
class VideoProcessor(object):
    def __init__(self, video_file, processor, painter):
        self.painter = painter
        self.processor = processor
        self.video_file = video_file
        self.initialized = False

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
                self.painter.draw(frame)
                self.painter.on_change_value(self.processor, 0)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    