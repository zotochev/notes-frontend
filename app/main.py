import asyncio

from event_system import event_system, Events

from main_view import MainView
from side_bar import SideBar, Item
from store import Store

from config import Config

import flet as ft


WIDTH = 640
HEIGHT = 360
SIDE_BAR_WIDTH = 200


async def get_store() -> Store:
    store = Store()

    await store.add_item(Item(title='item 0', data='value 0'))
    await store.add_item(Item(title='item 1', data='value 1'))
    await store.add_item(Item(title='item 2', data='value 2'))
    await store.add_item(Item(title='item 3', data='value 3'))

    return store


async def main(page: ft.Page):

    page.window_width = WIDTH
    page.window_height = HEIGHT
    page.window_min_width = WIDTH
    page.window_min_height = HEIGHT
    page.spacing = 0
    page.padding = ft.padding.all(0)

    main_row = ft.Row(expand=True)
    main_row.spacing = 0
    main_row.width = WIDTH
    main_row.height = HEIGHT

    store = await get_store()

    main_view = MainView(width=WIDTH - Config.sidebar_width, parent=main_row, page=page, store=store)
    side_bar = SideBar(width=Config.sidebar_width, parent=main_row, page=page, store=store)
    await side_bar.init()

    main_row.controls.append(side_bar.get_control())
    main_row.controls.append(main_view.get_control())

    async def on_resize(e):
        if e.name != 'resize':
            return
        width, height = [int(float(d)) for d in e.data.split(',')]
        await event_system.on_event(Events.Page.resize, width, height)

    page.on_resize = on_resize

    await page.add_async(main_row)


if __name__ == '__main__':
    asyncio.run(ft.app_async(main))
