import threading
# Define the thread that will continuously pull frames from the camera
class EncoderThread(threading.Thread):
    def __init__(self, web_driver, name='rotary-encoder-thread'):
        self.web_driver = web_driver
        super(EncoderThread, self).__init__(name=name)
        self.running = True
        self.start()

    def run(self):
        #check GPIO
 
    def terminate(self):
        print('terminating thread')
        self.running = False
