import time


start_time = 0
last_time = 0
IS_QUIET = False


def start():
    global start_time
    global last_time
    start_time = time.process_time()
    last_time = time.process_time()
    print("LOG : START")


def mid(msg):
    if IS_QUIET:
        return
    global last_time
    current = time.process_time()
    total = current - start_time
    delta = current - last_time
    last_time = current
    print(f"LOG : {total:2.5f}s (delta: {delta:2.5f}) : {msg}")


def end():
    end_time = time.process_time()
    total = end_time - start_time
    delta = end_time - last_time
    print(f"LOG : {total:2.5f}s (delta: {delta:2.5f}) : END")

