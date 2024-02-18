from abc import abstractmethod, ABC


class DataStore(ABC):

    @abstractmethod
    async def add_item(self, item) -> 'Item':
        pass

    @abstractmethod
    async def get_item(self, id_: int):
        pass

    @abstractmethod
    async def put_item(self, item):
        pass

    @abstractmethod
    async def del_item(self, id_: int):
        pass

    @abstractmethod
    async def get_items(self):
        pass
