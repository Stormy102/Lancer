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
        """
        Add an event to the queue
        :param service: The service to add to the queue
        :param port: The port to add to the queue
        """
        EventQueue.event_queue.put(Event(service, port))

    @staticmethod
    def pop() -> Event:
        """
        Pops the next event out of the queue
        :return: The retrieved Event
        """
        return EventQueue.event_queue.get()

    @staticmethod
    def events_in_queue() -> bool:
        """
        Check if there are any events still in the queue
        :return: True if events remain, false if not
        """
        return EventQueue.event_queue.qsize() > 0
