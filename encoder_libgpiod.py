# Class to monitor a rotary encoder and update a value.  You can either read the value when you need it, by calling getValue(), or
# you can configure a callback which will be called whenever the value changes.

import gpiod
import sys

class Encoder:

    def __init__(self, callback=None):
        self.leftPin = leftPin
        self.rightPin = rightPin
        self.value = 0
        self.state = '00'
        self.direction = None
        self.callback = callback
        self.chip = gpiod.Chip("gpiochip1")
        self.lines = self.chip.get_lines([3, 20])

        self.lines.request(consumer="customer", type=gpiod.LINE_REQ_EV_BOTH_EDGES)
        
    def run(self):
        try:
            while True:
                ev_lines = self.lines.event_wait(sec=1)
                if ev_lines:
                    for line in ev_lines:
                        event = line.event_read()
                        self.print_event(event)
                self.transitionOccurred()   
        except KeyboardInterrupt:
             chip.close()
            sys.exit(130)

    def transitionOccurred(self):
        #self.lines.release()
        #self.lines.request(consumer="customer", type=gpiod.LINE_REQ_DIR_IN)

        p1 = self.lines[0].get_value()
        p2 = self.lines[1].get_value()
        newState = "{}{}".format(p1, p2)

        if self.state == "00": # Resting position
            if newState == "01": # Turned right 1
                self.direction = "R"
            elif newState == "10": # Turned left 1
                self.direction = "L"

        elif self.state == "01": # R1 or L3 position
            if newState == "11": # Turned right 1
                self.direction = "R"
            elif newState == "00": # Turned left 1
                if self.direction == "L":
                    self.value = self.value - 1
                    if self.callback is not None:
                        self.callback(self.value, self.direction)

        elif self.state == "10": # R3 or L1
            if newState == "11": # Turned left 1
                self.direction = "L"
            elif newState == "00": # Turned right 1
                if self.direction == "R":
                    self.value = self.value + 1
                    if self.callback is not None:
                        self.callback(self.value, self.direction)

        else: # self.state == "11"
            if newState == "01": # Turned left 1
                self.direction = "L"
            elif newState == "10": # Turned right 1
                self.direction = "R"
            elif newState == "00": # Skipped an intermediate 01 or 10 state, but if we know direction then a turn is complete
                if self.direction == "L":
                    self.value = self.value - 1
                    if self.callback is not None:
                        self.callback(self.value, self.direction)
                elif self.direction == "R":
                    self.value = self.value + 1
                    if self.callback is not None:
                        self.callback(self.value, self.direction)
                
        self.state = newState
        #self.lines.release()
        #self.lines.request(consumer="customer", type=gpiod.LINE_REQ_EV_BOTH_EDGES)

    def getValue(self):
        return self.value
    
    def print_event(event):
        if event.type == gpiod.LineEvent.RISING_EDGE:
            evstr = ' RISING EDGE'
        elif event.type == gpiod.LineEvent.FALLING_EDGE:
            evstr = 'FALLING EDGE'
        else:
            raise TypeError('Invalid event type')

        print('event: {} offset: {} timestamp: [{}.{}]'.format(evstr,
                                                             event.source.offset(),
                                                             event.sec, event.nsec))
