#ll /dev/input/by-path/
# Rotary encoder using evdev
# Add to /boot/config.txt
# dtoverlay=rotary-encoder,pin_a=20,pin_b=21,relative_axis=1,steps-per-period=2
# Tweak pins and steps to match the encoder
# 클래스로 만들고 while문 함수 추가해서 threading하기
# import threading
# # Create the thread
#my_thread = threading.Thread(target=my_encoder.watch)

# Launch the thread
#my_thread.start()
 
import evdev
 
class EncoderEvdev:
  def __init__(self, callback=None):
    self.d = evdev.InputDevice('/dev/input/by-path/platform-rotary@14-event')
    print('Rotary encoder device: {}'.format(d.name))
    self.callback = callback
    self.position = 0
    
  def run(self):
    self.d.grab()
    while 1:
      for e in self.d.read_loop():

          print('Event: {}'.format(e))
          if e.type == evdev.ecodes.EV_REL:
              self.position += e.value
              print('Position: {}'.format(self.position))

              if(e.value > 0):
                self.callback(self.positon, "R")
              elif(e.value < 0):
                self.callback(self.positon, "L")
    self.d.ungrab()
