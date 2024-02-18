from .data_store import DataStore


class MemoryStore(DataStore):
    def __init__(self):
        self._store = {}

    async def get_item(self, id_: int):
        self._store.get(id_)

    async def put_item(self, item):
        assert item.id in self._store, f"{item.id} not in the store."

        self._store[item.id] = item

    async def del_item(self, id_: int):
        return self._store.pop(id, None)

    async def get_items(self):
        return list(self._store.values())

    async def add_item(self, item):
        assert item.id not in self._store, f"{item.id} already in store."
        assert item.id is None

        item.id = max(self._store.keys(), default=-1) + 1
        item.order = max((i.order for i in self._store.values()), default=-1) + 1

        self._store[item.id] = item
        return item
