import asyncio

from event_system import event_system

from page_wrapper import PageWrapper
from elements.side_bar import Item
from store import Store

from config import Config

import flet as ft


async def get_store() -> Store:
    store = Store()

    await store.add_item(Item(title='item 0', data='value 0'))
    await store.add_item(Item(title='item 1', data='value 1'))
    await store.add_item(Item(title='item 2', data='value 2'))
    await store.add_item(Item(title='item 3', data='value 3'))

    return store


async def main(page: ft.Page):

    page.window_width = Config.width
    page.window_height = Config.height
    page.window_min_width = Config.width
    page.window_min_height = Config.height
    page.spacing = 0
    page.padding = ft.padding.all(0)

    store = await get_store()

    page_wrapper = PageWrapper(page, store, event_system)
    await page_wrapper.init()


if __name__ == '__main__':
    asyncio.run(ft.app_async(main))
