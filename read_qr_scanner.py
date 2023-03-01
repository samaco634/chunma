from pynput import keyboard

scannedInput = []

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        scannedInput.append(key.char)
    except AttributeError:
        if key == keyboard.Key.enter:
            # Stop listener
            return False
def getScannedString():
    scannedInput.clear()
    # Collect events until released

    with keyboard.Listener(
            on_press=on_press    
            ) as listener:
        listener.join()


    return ''.join(scannedInput)

if __name__ ==   "__main__":
    while True:
        print(getScannedString())

