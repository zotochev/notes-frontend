from datetime import datetime

import flet as ft
from pydantic import BaseModel

from event_system import event_system, Events


class Item(BaseModel):
    id: int | None = None
    title: str
    data: str
    order: int = 0


class SideBarItem:
    def __init__(self, item: Item, color: str, page: ft.Page):
        self._page = page
        self._item = item

        self._button = ft.IconButton(
            icon=ft.icons.BRIGHTNESS_1,
            on_click=self._on_click_button,
        )
        self._text = ft.TextField(value=self._item.title, height=30, content_padding=ft.padding.all(0), disabled=True)

        self._row = ft.Row(controls=[
            self._button,
            self._text,
        ])

        self._control = ft.Container(
            content=self._row,
            bgcolor=color,
            on_click=self._on_click_item,
            on_long_press=self._on_long_click_item,
        )
        event_system.subscribe(Events.SideBar.Item.item_clicked, self._on_other_item_clicked)

    def get_control(self):
        return self._control

    async def _on_click_button(self, _):
        await event_system.on_event(Events.SideBar.Item.button_clicked, self._item)
        await self._page.update_async(self._control)

    async def _on_other_item_clicked(self, item: Item):
        if self._item.id != item.id:
            self._control.bgcolor = ft.colors.CYAN_200
        else:
            self._control.bgcolor = ft.colors.BLUE_200
        await self._page.update_async()

    async def _on_click_item(self, _):
        await event_system.on_event(Events.SideBar.Item.item_clicked, self._item)
        await self._page.update_async(self._control)

    async def _on_long_click_item(self, e):
        print(e)
