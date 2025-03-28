import atexit, termios
import sys, os
import time
import logging

old_settings = None
logger = logging.getLogger(__name__)


def init_any_key():
    global old_settings
    old_settings = termios.tcgetattr(sys.stdin)
    new_settings = termios.tcgetattr(sys.stdin)
    new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON)
    new_settings[6][termios.VMIN] = 0   # cc
    new_settings[6][termios.VTIME] = 0  # cc
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_settings)


@atexit.register
def term_any_key():
    global old_settings
    if old_settings:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


class InputReader:
    """Gets a single character from standard input.  Does not echo to the
screen."""

    def __init__(self):
        init_any_key()

    def on_read(self, fn):
        self.fn = fn

    def __call__(self):
        text = ""
        ch = os.read(sys.stdin.fileno(), 1).decode("utf-8")
        while len(ch) > 0:
            logger.debug("%s - %s" % (repr(ch), ord(ch)))
            self.fn(ch)
            ch = os.read(sys.stdin.fileno(), 1).decode("utf-8")

