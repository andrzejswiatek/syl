import cv2
from drawing import painting
from prodline import processing

serialize_file = 'D:\\Repositories\\GITSYL\\syl\\values.pickle'
image = cv2.imread('images/tasma.jpg')

def on_change(val):
    painter.on_change_value(processor, val)

processor = processing.ImageProcessor()
painter = painting.Painter('Image', serialize_file, on_change)

def main():
    with painter:
        painter.draw(image)
        on_change(0)
        cv2.waitKey(0)

if __name__ == "__main__":
    main()
