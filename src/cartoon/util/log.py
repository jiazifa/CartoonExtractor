#! -*- coding: utf-8 -*-

import os, sys
import time


def sprint(text: str, *colors) -> str:
    return text


def println(text: str, *colors):
    sys.stdout.write(sprint(text, *colors) + "\n")


def print_err(text: str, *colors):
    sys.stderr.write(sprint(text, *colors) + "\n")


def print_log(text: str, *colors):
    sys.stderr.write(sprint(text, *colors) + "\n")


def i(message: str):
    print_log(message)


def yes_or_no(message: str) -> bool:
    ans = str(input("%s (y/N)" % message)).lower().strip()
    if ans == "y":
        return True
    return False


class SimpleProgressBar:

    _displayed: bool = False
    _received: int = 0
    _speed: str = '0'
    _bar: str = ""

    def __init__(self, totol_size: int):
        self.totol_size = totol_size
        self.last_updated = time.time()

        totol = round(self.totol_size / (1024 * 1024), 1)
        percent = (self._received + 0.01) / totol

        self._bar = "{percent}%% {recv}/{totol}MB"

    def update(self):
        self._displayed = True
        perecent = round(self._received * 100 / self.totol_size, 1)

        bar = self._bar.format(
            percent=str(perecent),
            recv=str(self._received),
            totol=str(self.totol_size)
        )
        sys.stdout.write("\r" + bar + "\r")
        sys.stdout.flush()

    def update_received(self, n: int):
        self._received += n
        time_diff = time.time() - self.last_updated
        bytes_ps = n / time_diff if time_diff else 0

        if bytes_ps > 1024**3:
            self._speed = "{:>4.0f} GB/s".format(bytes_ps / 1024**3)
        elif bytes_ps >= 1024**2:
            self.speed = '{:4.0f} MB/s'.format(bytes_ps / 1024**2)
        elif bytes_ps >= 1024:
            self.speed = '{:4.0f} kB/s'.format(bytes_ps / 1024)
        else:
            self.speed = '{:4.0f}  B/s'.format(bytes_ps)
        self.last_updated = time.time()
        self.update()

    def update_piece(self, n: int):
        self.current_piece = n

    def done(self):
        if self._displayed:
            print()
            self._displayed = False


class CountProgressBar:
    _displayed: bool = False
    _received: int = 0
    _speed: str = '0'
    _bar: str = ""

    def __init__(self, totol_count: int):
        self.totol_count = totol_count

        percent = (self._received + 0.01) / totol_count

        self._bar = "{percent}%% {recv}/{totol}"

    def update(self):
        self._displayed = True
        perecent = round(self._received * 100 / self.totol_size, 1)

        bar = self._bar.format(
            percent=str(perecent),
            recv=str(self._received),
            totol=str(self.totol_size)
        )
        sys.stdout.write("\r" + bar + "\r")
        sys.stdout.flush()

    def update_received(self, n: int):
        self._received += n
        self.update()

    def done(self):
        if self._displayed:
            print()
            self._displayed = False