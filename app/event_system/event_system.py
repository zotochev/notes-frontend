import inspect
import logging
from typing import Callable


class EventSystem:
    def __init__(self):
        self._events: dict[str, list[Callable]] = {}

    def subscribe(self, name, handler):
        if name not in self._events:
            self._events[name] = []
        if handler in self._events[name]:
            logging.warning(f'{self.__class__.__name__}.subscribe: {name} already has {handler} as subscriber.')
            return

        self._events[name].append(handler)

    def unsubscribe(self, name, handler):
        if name not in self._events:
            logging.warning(f'{self.__class__.__name__}.unsubscribe: event {name} was never registered')

        if handler not in self._events[name]:
            logging.warning(f'{self.__class__.__name__}.unsubscribe: {handler} is not subscribed for {name}')

        self._events[name].remove(handler)

    async def on_event(self, name, *args):
        if name not in self._events:
            logging.warning(f'{self.__class__.__name__}.on_event: {name} is not registered')
            return

        for handler in self._events[name]:
            try:
                c = handler(*args)
                if inspect.iscoroutine(c):
                    await c
            except Exception as e:
                logging.error(f'{self.__class__.__name__}.on_event({name}): failed to call handler {handler}({args}): {e.__class__.__name__}: {e}')

