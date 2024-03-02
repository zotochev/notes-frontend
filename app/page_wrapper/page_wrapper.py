import flet as ft

from config import Config
from event_system import Events
from elements.main_view import MainView
from elements.side_bar import SideBar


class PageWrapper:
    def __init__(self, page: ft.Page, store, event_system):
        self._page = page
        self._store = store
        self._event_system = event_system

        self._main_row = ft.Row(expand=True)
        self._main_row.spacing = 0
        self._main_row.min_width = Config.width
        self._main_row.min_height = Config.height

        self._main_view: MainView | None = None
        self._side_bar: SideBar | None = None
        self._divider: ft.Draggable | None = None

    async def init(self):
        self._main_view = MainView(
            width=Config.width - Config.sidebar_width, parent=self._main_row, page=self._page, store=self._store)
        self._side_bar = SideBar(
            width=Config.sidebar_width, parent=self._main_row, page=self._page, store=self._store)
        await self._side_bar.init()
        self._divider = ft.Draggable(
            content=ft.Container(height=Config.height, width=10, bgcolor=ft.colors.TRANSPARENT))
        self._divider.page = self._page

        self._main_row.controls.append(self._side_bar.get_control())
        self._main_row.controls.append(self._divider)
        self._main_row.controls.append(self._main_view.get_control())

        self._page.on_resize = self._on_page_resize

        await self._page.add_async(
            ft.DragTarget(content=self._main_row, on_accept=self._on_drag_accept)
        )

        self._event_system.subscribe(Events.Page.resize, self._divider_on_page_resize)

    async def _on_page_resize(self, e):
        if e.name != 'resize':
            return
        print('resize', e)
        width, height = [int(float(d)) for d in e.data.split(',')]
        await self._event_system.on_event(Events.Page.resize, width, height)

    async def _divider_on_page_resize(self, _: int, height: int):
        print("divider resize")
        self._divider.height = height
        self._divider.content.height = height
        await self._divider.update_async()

    async def _on_drag_accept(self, e):
        print(e)
        Config.sidebar_width = int(e.x)
        await self._event_system.on_event(Events.Page.resize, self._page.width, self._page.height)
        await self._page.update_async()

