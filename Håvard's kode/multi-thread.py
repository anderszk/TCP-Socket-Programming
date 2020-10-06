"""
An Example of using multi-threading in Python
"""

import threading
import time


def print_time(delay, iterations, thread_name):
    """
    An entry-point for a thread. Simulates long operation in iterations. Prints time in every iteration.
    :param delay: How long each iteration should be, in seconds
    :param iterations: How many iterations to run
    :param thread_name: The name of the thread running this code, used for printing
    :return:
    """
    for i in range(iterations):
        print("%s: %s" % (thread_name, time.ctime()))
        time.sleep(delay)


if __name__ == "__main__":
    # The main entry point of the "application". Starts several threads with different arguments
    t1 = threading.Thread(target=print_time, args=(0.5, 20, "Speedy Gonzales"))
    t2 = threading.Thread(target=print_time, args=(2, 5, "Slowpoke"))
    t3 = threading.Thread(target=print_time, args=(1, 10, "Thread #3"))
    t1.start()
    t2.start()
    t3.start()