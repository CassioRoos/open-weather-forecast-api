import datetime
import time
from functools import partial

from tornado import ioloop


def format_date(format, date):
    return datetime.datetime.fromtimestamp(date).strftime(format)


def wait_a_minute(condition):
    if condition:
        time.sleep(1)


def future_call(method, *args):
    ioloop.IOLoop.current().call_later(0.01, partial(method, *args))
