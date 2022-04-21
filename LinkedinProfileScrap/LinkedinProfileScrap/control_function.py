import time

def slow_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(0.5)