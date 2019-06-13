#!/usr/bin/env python3
# coding=utf-8

from threading import RLock, Condition


class CountDownLatch(object):
    def __init__(self, count):
        self._count = count
        self._count_lock = RLock()

        self._wait_lock = RLock()
        self._condition = Condition(self._wait_lock)

    def count_down(self, n=1):
        with self._count_lock:
            if self._count >= n:
                self._count -= n
            else:
                raise RuntimeError("count exceeded")
        if self._count == 0:
            with self._condition:
                self._condition.notify()

    def wait(self):
        with self._condition:
            self._condition.wait()

    def count(self):
        return self._count
