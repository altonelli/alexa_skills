import time
import random
import threading
from copy import copy

import pigpio

from constants import *
from rgb import RGB, RGBColor
from light_values import *

PINS = RGB(r=R_PIN, g=G_PIN, b=B_PIN)

OFF = RGBColor(r=0, g=0, b=0)

class Light(object):
    """Lights object to maintian logic of the state of the lights and
    Gpio ports
    """
    def __init__(self):
        super(Light, self).__init__()
        # Core attributes
        self.brightness = 100
        self.mode = STATIC
        self.power_state = "OFF"
        self.color = copy(NATURALISH)

        # Color/Brightness adjustment attributes
        self.display_brightness = 100
        self.display_color = RGBColor(r=self.color.r,
                                      g=self.color.g,
                                      b=self.color.b)
        # GPIO initialization
        self.pi = pigpio.pi()
        self.lock = threading.Lock()
        self.wave_thread = threading.Thread(self._wave())
        self.wave_thread.start()

    def current_settings(self):
        return {
                   'power_state': self.power_state,
                   'brightness': self.brightness,
                   'mode': self.mode
               }

    def needs_updating(self, light_data):
        self.lock.acquire()
        brightness = self.brightness
        mode = self.mode
        power_state = self.power_state
        self.lock.release()
        if light_data.get('brightness') != brightness \
        or light_data.get('mode') != mode \
        or light_data.get('power_state') != power_state:
            return True
        return False

    def update_lights(self, light_data):
        self.lock.acquire()
        self.display_brightness = self.brightness
        self.brightness = light_data.get('brightness')
        self.mode = light_data.get('mode')
        self.power_state = light_data.get('power_state')
        self.lock.release()
        self._update_board()

    def _update_board(self):
        self.lock.acquire()
        power_state = self.power_state
        self.lock.release()
        if power_state == "ON":
            # Case where called on
            self._update_mode()
            self._update_brightness()
        else:
            # Case where called off
            self.lock.acquire()
            self.display_color.copy_disp_values(OFF)
            self.lock.release()
            self._update_color()

    def _update_brightness(self):
        """
        Updates the display brightness incrementally. This will
        effect all Modes.

        If the Mode is on STATIC or not in WAVE it will also
        fade and adjust the color.
        """
        while self.display_brightness != self.brightness:
            if self.mode != WAVE:
                self._reset_disp_color_and_brightness(True)
                self._update_color()
            # adjust previous brightness to +/- 1
            self._adj_disp_brightness()
            time.sleep(DURATION_OF_STEP)
        if self.mode != WAVE:
            # True up color to brightness adjustment
            self._reset_disp_color_and_brightness()
            self._update_color()

    def _update_mode(self):
        self.lock.acquire()
        mode = self.mode
        self.lock.release()
        while self.mode == WAVE:
            self.wave_thread.join()
        # Reset to original color, and current brightness after WAVE Mode
        self._reset_disp_color_and_brightness()
        self._update_color()

    def _adj_disp_brightness(self):
        self.lock.acquire()
        remaining_adjustment = self.brightness - self.display_brightness
        self.display_brightness = self.display_brightness + \
            (remaining_adjustment) / abs(remaining_adjustment)
        self.lock.release()

    def _reset_disp_color_and_brightness(self, display_brightness=False):
        self.lock.acquire()
        self.display_color.reset_color()
        if display_brightness:
            self.display_color.adjust_brightness(self.display_brightness)
        else:
            self.display_color.adjust_brightness(self.brightness)
        self.lock.release()

    def _update_color(self):
        """
        Updates the LED colors on the lights through the GPIO Pins with
        the pigpio library.
        """
        self.lock.acquire()
        self.pi.set_PWM_dutycycle(PINS.r, self.display_color.display_r)
        self.pi.set_PWM_dutycycle(PINS.g, self.display_color.display_g)
        self.pi.set_PWM_dutycycle(PINS.b, self.display_color.display_b)
        self.lock.release()

    def _wave(self):
        rgb_colors = get_rgb_color_list()
        self.lock.acquire()
        mode = self.mode
        power_state = self.power_state
        self.lock.release()
        while mode == WAVE and power_state == "ON":
            # Get new color and adjust its brightness to be current
            rand_int = random.randint(0, len(rgb_colors) - 1)
            next_color = rgb_colors[rand_int]
            next_color.reset_color()
            self.lock.acquire()
            next_color.adjust_brightness(self.display_brightness)
            self.lock.release()
            # Incrementally adjust the color of the wave
            color_adjs = self.display_color.get_color_adjustments(next_color)
            for step in range(0, NUM_OF_STEPS):
                self.display_color.adjust_color(r=color_adjs[0],
                                                g=color_adjs[1],
                                                b=color_adjs[2])
                self._update_color()
                time.sleep(DURATION_OF_STEP)
            # True up final color fo wave
            self.display_color.copy_disp_values(next_color)
            self._update_color()
            self.lock.acquire()
            mode = self.mode
            self.lock.release()
            time.sleep(DURATION_OF_STEP)
        self.lock.acquire()
        self._update_board()
        self.lock.release()
        return 0



def get_rgb_color_list():
    rgbs = [NATURALISH, OVERCAST_SKY, CANDLE, SODIUM_VAPOR,
            HIGH_PRESSURE_SODIUM, TUNGSTEN_40W]
    rgb_colors = []
    for rgb in rgbs:
        rgb_color = RGBColor(r=rgb.r,
                             g=rgb.g,
                             b=rgb.b)
        rgb_colors.append(rgb_color)
    return rgb_colors


if __name__ == '__main__':
    light = Light()
    light._update_board()
    time.sleep(3)
    light_data_0 = {
        'power_state': "ON",
        'brightness': 100,
        'mode': STATIC
    }
    print(light_data_0)
    light.update_lights(light_data_0)
    time.sleep(1)
    light_data_1 = {
        'power_state': "ON",
        'brightness': 50,
        'mode': WAVE
    }
    print(light_data_1)
    light.update_lights(light_data_1)
    time.sleep(1)
    light_data_2 = {
        'power_state': "ON",
        'brightness': 10,
        'mode': STATIC
    }
    print(light_data_2)
    light.update_lights(light_data_2)
    time.sleep(1)
    light_data_3 = {
        'power_state': "ON",
        'brightness': 100,
        'mode': STATIC
    }
    print(light_data_3)
    light.update_lights(light_data_3)
    time.sleep(1)
    light_data_4 = {
        'power_state': "ON",
        'brightness': 100,
        'mode': WAVE
    }
    print(light_data_4)
    light.update_lights(light_data_4)
    time.sleep(30)
    light_data_5 = {
        'power_state': "ON",
        'brightness': 50,
        'mode': WAVE
    }
    print(light_data_5)
    light.update_lights(light_data_5)
    time.sleep(30)
    light_data_6 = {
        'power_state': "OFF",
        'brightness': 50,
        'mode': WAVE
    }
    print(light_data_6)
    light.update_lights(light_data_6)
    time.sleep(3)
    light_data_7 = {
        'power_state': "ON",
        'brightness': 50,
        'mode': WAVE
    }
    print(light_data_7)
    light.update_lights(light_data_7)
    time.sleep(30)
    light_data_8 = {
        'power_state': "OFF",
        'brightness': 50,
        'mode': WAVE
    }
    print(light_data_8)
    light.update_lights(light_data_8)
