
class LineArea(object):
    def __init__(self):
        self.contours = []
        self.left_top = None
        self.right_top = None
        self.left_bottom = None
        self.right_bottom = None
        self.left_most = None
        self.right_most = None
        self.top_most = None
        self.bottom_most = None
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None

class Line(object):
    def __init__(self):
        self.area_top = LineArea()
        self.area_bottom = LineArea()