import cv2
from drawing import painting
from prodline import processing

serialize_file = 'D:\\Repositories\\GITSYL\\syl\\values.pickle'
image = cv2.imread('images/tasma.jpg')

processor = processing.ProcessorFactory().create()
painter = painting.Painter('Monitoring linii produkcyjnej', serialize_file, processor)
painter.assign(image)

def main():
    with painter:
        painter.draw(image)
        painter.on_change(0)
        cv2.waitKey(0)

if __name__ == "__main__":
    main()
