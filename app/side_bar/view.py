import flet as ft

from config import Config
from event_system import Events, event_system
from store.data_store import DataStore
from .item import SideBarItem, Item


class SideBar:
    def __init__(self, width: int, parent: ft.Row, page: ft.Page, store: DataStore):
        self._page: ft.Page = page
        self._parent = parent
        self._store = store

        self._header = ft.Container(bgcolor=ft.colors.GREEN_100, height=Config.header_height, on_click=self._on_header_click)
        self._new_item = ft.Container(bgcolor=ft.colors.BROWN_200, height=Config.header_height, on_click=self._on_new_item_click)

        self._side_bar_items = []
        self._list_view = ft.ListView(
            controls=[],
        )
        self._items_column = ft.Column(
            controls=[self._list_view],
            scroll=ft.ScrollMode.ALWAYS,
            auto_scroll=True,
        )
        self._column = ft.Column(controls=[
                self._header,
                self._new_item,
                # self._list_view,
                self._items_column,
            ],
            spacing=0,
        )

        self._control = ft.Container(
            content=self._column,
            width=width,
            height=parent.height,
            bgcolor=ft.colors.TEAL_50,
        )

        event_system.subscribe(Events.Page.resize, self.on_page_resize)

    async def init(self):
        items = await self._store.get_items()

        self._side_bar_items = [
            SideBarItem(
                item,
                page=self._page,
                color=ft.colors.CYAN_200,
            )
            for item in items
        ]
        self._list_view.controls = [
            item.get_control()
            for item in self._side_bar_items
        ]

    async def on_page_resize(self, _: int, height: int):
        offset = Config.header_height * 2

        self._control.width \
            = self._column.width \
            = self._header.width \
            = self._list_view.width \
            = Config.sidebar_width
        self._control.height = self._column.height = height

        self._header.height = Config.header_height
        self._new_item.height = Config.header_height
        self._list_view.height = self._control.height - offset

        await self._page.update_async()

    async def _on_new_item_click(self, e):
        new_item = Item(title='new item', data='')

        new_item = await self._store.add_item(new_item)

        new_sidebar_item = SideBarItem(
            new_item,
            page=self._page,
            color=ft.colors.CYAN_200,
        )
        self._side_bar_items.append(new_sidebar_item)
        self._list_view.controls.append(new_sidebar_item.get_control())
        await self._page.update_async()

    async def _on_header_click(self, e):
        print('header', e)

    def get_control(self) -> ft.Control:
        return self._control

