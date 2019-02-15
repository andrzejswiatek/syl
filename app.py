import cv2
from drawing import painting
from prodline import processing

image = cv2.imread('images/tasma.jpg')

processor = processing.Processor(image)
painter = painting.Painter('Image')

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

def on_change(val):
    rgb_begin = [painter.get_value(track_bar_rgb_min_red[0]),
                 painter.get_value(track_bar_rgb_min_green[0]),
                 painter.get_value(track_bar_rgb_min_blue[0])]
    rgb_end = [painter.get_value(track_bar_rgb_max_red[0]),
                 painter.get_value(track_bar_rgb_max_green[0]),
                 painter.get_value(track_bar_rgb_max_blue[0])]
    out = processor.apply_color_filter_using(rgb_begin, rgb_end)
    painter.draw(out)

for bar in track_bars:
    painter.create_track_bar(bar[0], bar[1], 255, on_change)

with painter:
    on_change(0)
    cv2.waitKey(0)


