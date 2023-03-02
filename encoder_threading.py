import threading
import RPi.GPIO as GPIO

# Define the thread that will continuously check rotary encoder
class EncoderThread(threading.Thread):
    def __init__(self, leftPin, rightPin, callback=None, name='rotary-encoder-thread'):
        self.leftPin = leftPin
        self.rightPin = rightPin
        self.value = 0
        self.state = '00'
        self.direction = None
        self.callback = callback
        super(EncoderThread, self).__init__(name=name)
        self.running = True
        self.start()

    def run(self):
        while self.running :
            #check GPIO
            p1 = GPIO.input(self.leftPin)
            p2 = GPIO.input(self.rightPin)
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
            sleep(0.1)
 
    def terminate(self):
        print('terminating thread')
        self.running = False
