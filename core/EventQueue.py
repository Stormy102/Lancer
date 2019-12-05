# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

import queue


class Event(object):

    def __init__(self, service: str = "", port: int = 0, version: str = "", vulnerability: str = ""):
        self.service = service
        self.port = port
        self.version = version
        self.vulnerability = vulnerability


class EventQueue(object):
    event_queue = queue.Queue()

    @staticmethod
    def push(service: str, port: int) -> None:
        EventQueue.event_queue.put(Event(service, port))

    @staticmethod
    def pop() -> Event:
        return EventQueue.event_queue.get()

    @staticmethod
    def events_in_queue() -> bool:
        return EventQueue.event_queue.qsize() > 0
