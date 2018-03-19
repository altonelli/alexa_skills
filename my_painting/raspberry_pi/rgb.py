from constants import *

class RGB(object):
    def __init__(self, r, g, b):
        super(RGB, self).__init__()
        self.r = r
        self.g = g
        self.b = b

class RGBColor(RGB):
    def __init__(self, r, g, b):
        super(RGBColor, self).__init__(r, g, b)
        self.display_r = self.r
        self.display_g = self.g
        self.display_b = self.b

    def adjust_brightness(self, brightness):
        self.display_r = int(self.r * (brightness / 100))
        self.display_g = int(self.g * (brightness / 100))
        self.display_b = int(self.b * (brightness / 100))

    def adjust_color(self, r, g, b):
        self.display_r = int(self.r + r)
        self.display_g = int(self.g + g)
        self.display_b = int(self.b + b)

    def get_color_adjustments(self, rgb_color):
        r_adjust = int((rgb.display_r - self.display_r) / NUM_OF_STEPS)
        g_adjust = int((rgb.display_g - self.display_g) / NUM_OF_STEPS)
        b_adjust = int((rgb.display_b - self.display_b) / NUM_OF_STEPS)
        return (r_adjust, g_adjust, b_adjust)

    def copy_disp_values(self, rgb_color):
        self.display_r = rgb_color.display_r
        self.display_g = rgb_color.display_g
        self.display_b = rgb_color.display_b

    def reset_color(self):
        self.display_r = self.r
        self.display_g = self.g
        self.display_b = self.b