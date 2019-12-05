# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.EventQueue import EventQueue, Event

import pytest
import queue


@pytest.mark.core
def test_event():
    event: Event = Event(service="ftp", port=21, version="cpe:2.3:a:microsoft:iis", vulnerability="")
    assert event
    assert event.service == "ftp"
    assert event.port == 21


@pytest.mark.core
def test_eventqueue_push():
    EventQueue.event_queue = queue.Queue()
    EventQueue.push("ftp", 21)
    event = EventQueue.event_queue.get()
    assert event.service == "ftp"
    assert event.port == 21


@pytest.mark.core
def test_eventqueue_pop():
    EventQueue.event_queue = queue.SimpleQueue()
    EventQueue.event_queue.put(Event("ftp", 21))
    EventQueue.event_queue.put(Event("http", 80))

    event = EventQueue.pop()
    assert event.service == "ftp"
    assert event.port == 21
    popped_event = EventQueue.event_queue.get()
    assert popped_event.service != "ftp"
    assert popped_event.service != 21
