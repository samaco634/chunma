# GPIO used PD30

import gpiod
import time

chip = gpiod.Chip('gpiochip2')
line = gpiod.find_line("PD4")
lines = chip.get_lines([line.offset()])
lines.request(consumer='foobar', type=gpiod.LINE_REQ_DIR_IN)

chip2 = gpiod.Chip('gpiochip1')
line2 = gpiod.find_line("PC4")
lines2 = chip.get_lines([line.offset()])
lines2.request(consumer='foobar', type=gpiod.LINE_REQ_DIR_IN)


while True:
    print("{}{}".format(lines.get_values(), lines2.get_values())
    time.sleep(1)
    print("{}{}".format(lines.get_values(), lines2.get_values())
    time.sleep(1)
