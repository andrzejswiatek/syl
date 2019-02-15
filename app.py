from drawing import painting
from prodline import processing
import cv2

processor =  processing.ImageProcessor()
serialize_file = 'D:\\Repositories\\GITSYL\\syl\\values.pickle'
def on_change(val):
    painter.on_change_value(processor, val)

painter = painting.Painter('Image', serialize_file, on_change)
video_processor = processing.VideoProcessor(r'D:\Projekty\MachineLearning\Sylwek\tasma.mp4', processor, painter)

with video_processor:
    video_processor.process()

