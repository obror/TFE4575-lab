import pya
import numpy as np


class Point:
    """Class Representing a Point in 2D Space"""

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def offset_y(self, dy: int):
        """returns a new point offset by dy in y direction"""
        return Point(self.x, self.y + dy)

    def offset_x(self, dx: int):
        """returns a new point offset by dx in x direction"""
        return Point(self.x + dx, self.y)

    def offset(self, dx: int, dy: int):
        """returns a new point offset by dx in x direction and dy in y direction"""
        return Point(self.x + dx, self.y + dy)


class MyBox(pya.Box):
    """Class that wraps pya.Box so that it accepts a point reprecenting lower left corner, and a width and height"""

    def __init__(self, lower_left_pos: Point, width: int, height: int) -> None:

        self.lower_left_pos = lower_left_pos
        self.width = width
        self.height = height

        super().__init__(
            self.lower_left_pos.x,
            self.lower_left_pos.y,
            self.lower_left_pos.x + self.width,
            self.lower_left_pos.y + self.height,
        )


class Finger:
    """Class that represents a single finger on a LED hand. Defined by its lower left position and width and height"""

    def __init__(self, start_point: Point, width: int, height: int) -> None:

        self.start_point: Point = start_point
        self.width: int = width
        self.height: int = height

    def draw(self, top, layer) -> None:
        """Draws the finger at the given top and layer"""
        top.shapes(layer).insert(MyBox(self.start_point, self.width, self.height))


class Hand:
    """A class that represents a full hand LED."""

    def __init__(
        self,
        top,
        layer,
        start_pos: Point,
        finger_width: int,
        finger_pitch: int,
        width: int,
        height: int,
        scale: int,
    ) -> None:
        self.top = top
        self.layer = layer
        self.start_pos: Point = start_pos
        self.finger_width: int = finger_width
        self.finger_pitch: int = finger_pitch
        self.width: int = width
        self.height: int = height
        self.vertical_bus_width: int = 30 * scale
        self.horizontal_bus_height: int = 50 * scale

    def draw_base(self):
        """Draws the base horizontal bus bar and vertical bussbar with parameters that are fixed in __init__"""
        self.top.shapes(self.layer).insert(
            MyBox(self.start_pos, self.width, self.horizontal_bus_height)
        )
        self.top.shapes(self.layer).insert(
            MyBox(
                self.start_pos.offset_x(self.width / 2 - self.vertical_bus_width / 2),
                self.vertical_bus_width,
                self.height,
            )
        )

    def draw_fingers(self):
        """Calculates how many fingers fit on the LED, and draws them"""
        num_fingers = int(
            (self.height - self.horizontal_bus_height)
            / (self.finger_width + self.finger_pitch)
        )

        for i in range(num_fingers):

            finger_pos = self.start_pos.offset_y(
                i * (self.finger_width + self.finger_pitch)
                + self.horizontal_bus_height
                + self.finger_pitch
            )

            finger = Finger(finger_pos, self.width, self.finger_width)
            finger.draw(self.top, self.layer)

    def draw(self):
        """Method that draws the entire LED hand"""
        self.draw_base()
        self.draw_fingers()


if __name__ == "__main__":

    layout = pya.Layout()

    top = layout.create_cell("TOP")
    layer = layout.layer(1, 0)

    scale = 1000

    LED_widht = 1000 * scale  # microns
    LED_heigth = 1000 * scale  # microns

    LED_spacing_x = 600 * scale  # microns
    LED_spacing_y = 1200 * scale  # microns

    finger_widths = np.array([4, 4.5, 5, 5.5]) * scale  # microns
    finger_pitches = np.array([50, 100, 150, 200]) * scale  # microns

    startpos = Point(0, 0)

    for x in range(4):
        for y in range(4):

            hand_point = startpos.offset(
                x * (LED_widht + LED_spacing_x), y * (LED_heigth + LED_spacing_y)
            )

            finger_width = finger_widths[y]
            finger_pitch = finger_pitches[x]

            single_hand = Hand(
                top,
                layer,
                hand_point,
                finger_width,
                finger_pitch,
                LED_widht,
                LED_heigth,
                scale,
            )

            single_hand.draw()

    layout.write(
        "/Users/anders/Documents/Skole/5.host/Lab/FordypningLab/LED_Design.gds"
    )
