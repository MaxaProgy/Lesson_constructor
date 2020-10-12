class Normalize():
    def __init__(self, window):
        self.init_width = 1920
        self.init_height = 1030

        self.width_windows = window.geometry.width()
        self.height_windows = window.geometry.height()

    def normal_xy(self, x, y):
        return int(self.width_windows / self.init_width * x), int(self.height_windows / self.init_height * y)

    def normal_prop_xy(self, x, y):
        return int(self.width_windows / self.init_width * x), int(self.width_windows / self.init_width * y)

    def normal_font(self, font):
        return str(int(self.width_windows / self.init_width  * font))