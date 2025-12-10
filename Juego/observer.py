from collections import defaultdict
from typing import Callable, Any

class EventBus:
    def __init__(self):
        self._subs = defaultdict(list)

    def subscribe(self, event_name: str, handler: Callable[[Any], None]):
        self._subs[event_name].append(handler)
        return handler

    def unsubscribe(self, event_name: str, handler: Callable[[Any], None]):
        if handler in self._subs[event_name]:
            self._subs[event_name].remove(handler)

    def publish(self, event_name: str, payload: Any = None):
        for h in list(self._subs[event_name]):
            try:
                h(payload)
            except Exception:
                import traceback
                traceback.print_exc()
