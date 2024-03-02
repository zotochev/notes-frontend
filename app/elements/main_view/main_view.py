import flet as ft

from config import Config
from event_system import event_system, Events
from store.data_store import DataStore


class MainView:
    def __init__(self, width: int, parent: ft.Row, page: ft.Page, store: DataStore):
        self._page = page
        self._store = store
        self._active_item = None

        self._parent = parent

        self._header = ft.Container(bgcolor=ft.colors.GREEN_200)
        self._text = ft.TextField(multiline=True, on_blur=self.on_blur)
        self._column = ft.Column(controls=[
                self._header,
                self._text,
            ],
            spacing=0,
        )

        self._control = ft.Container(
            content=self._column,
            width=width,
            height=parent.height,
            bgcolor=ft.colors.AMBER_50,
        )

        event_system.subscribe(Events.Page.resize, self.on_page_resize)
        event_system.subscribe(Events.SideBar.Item.item_clicked, self.on_side_view_item_clicked)

    async def on_page_resize(self, width: int, height: int):
        self._control.width = width - Config.sidebar_width
        self._control.height = height

        self._column.width = self._header.width = self._control.width
        self._column.height = self._control.height
        self._header.height = Config.header_height
        self._text.width = self._control.width
        self._text.height = self._control.height

        await self._page.update_async()

    async def on_side_view_item_clicked(self, item):
        self._text.value = item.data
        self._active_item = item
        await self._page.update_async()

    async def on_change(self, e):
        if e.name not in ('change',) or self._active_item is None:
            return

        self._active_item.data = e.data
        await self._store.put_item(self._active_item)

    async def on_blur(self, e):
        if e.name not in ('blur',) or self._active_item is None:
            return

        self._active_item.data = e.control.value
        await self._store.put_item(self._active_item)

    def get_control(self) -> ft.Control:
        return self._control
