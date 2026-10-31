
import time

def start_step():
    return time.monotonic()

def finish_step(start_time):
    elapsed = time.monotonic() - start_time
    return round(elapsed, 2)