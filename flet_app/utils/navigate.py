import flet as ft
import asyncio

previous_index = 0
is_navigate_active = False


async def navigate(page, navigation_bar, main_container, settings_container, pool_container, arbitrage_container, e=None):
    global previous_index
    global is_navigate_active

    if is_navigate_active:
        return
    is_navigate_active = True

    if e == 3:
        new_index = 3
    else:
        new_index = navigation_bar.selected_index

    previous_content = None
    new_content = None
    direction = None

    if previous_index == 0:
        previous_content = main_container
    if previous_index == 1:
        previous_content = pool_container
    if previous_index == 2:
        previous_content = arbitrage_container
    elif previous_index == 3:
        previous_content = settings_container

    if new_index == 0:
        new_content = main_container
    if new_index == 1:
        new_content = pool_container
    if new_index == 2:
        new_content = arbitrage_container
    elif new_index == 3:
        new_content = settings_container

    if new_index > previous_index:
        direction = 3
    if new_index < previous_index:
        direction = -3
    if new_index == previous_index or new_index is None:
        is_navigate_active = False
        return

    if new_index != 3 and previous_index == 3:
        previous_content.offset = ft.transform.Offset(0, 0)
        previous_content.animate_offset = ft.animation.Animation(duration=300,
                                                                 curve=ft.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED)
        page.update()
        await asyncio.sleep(0.5)
        previous_content.offset = ft.transform.Offset(0, direction)
        page.update()
        await asyncio.sleep(0.5)
        previous_content.visible = False
        page.update()
        new_content.visible = True
        new_content.offset = ft.transform.Offset(0, -direction)
        new_content.animate_offset = ft.animation.Animation(duration=300,
                                                            curve=ft.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED)
        page.update()
        await asyncio.sleep(0.5)
        new_content.offset = ft.transform.Offset(0, 0)
        page.update()
        await asyncio.sleep(0.5)
        previous_index = new_index
        is_navigate_active = False
    elif new_index != 3 and previous_index != 3:
        previous_content.offset = ft.transform.Offset(0, 0)
        previous_content.animate_offset = ft.animation.Animation(duration=300,
                                                                 curve=ft.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED)
        page.update()
        await asyncio.sleep(0.5)
        previous_content.offset = ft.transform.Offset(-direction, 0)
        page.update()
        await asyncio.sleep(0.5)
        previous_content.visible = False
        page.update()
        new_content.visible = True
        page.update()
        new_content.offset = ft.transform.Offset(direction, 0)
        page.update()
        new_content.animate_offset = ft.animation.Animation(duration=300,
                                                            curve=ft.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED)
        page.update()
        await asyncio.sleep(0.5)
        page.update()
        new_content.offset = ft.transform.Offset(0, 0)
        page.update()
        await asyncio.sleep(0.5)
        previous_index = new_index
        is_navigate_active = False

    elif new_index == 3 and previous_index !=3:
        previous_content.offset = ft.transform.Offset(0, 0)
        previous_content.animate_offset = ft.animation.Animation(duration=300,
                                                                 curve=ft.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED)
        page.update()
        await asyncio.sleep(0.5)
        previous_content.offset = ft.transform.Offset(0, direction)
        page.update()
        await asyncio.sleep(0.5)
        previous_content.visible = False
        page.update()
        new_content.visible = True
        new_content.offset = ft.transform.Offset(0, -direction)
        new_content.animate_offset = ft.animation.Animation(duration=300,
                                                            curve=ft.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED)
        page.update()
        await asyncio.sleep(0.5)
        new_content.offset = ft.transform.Offset(0, 0)
        page.update()
        await asyncio.sleep(0.5)
        previous_index = new_index
        is_navigate_active = False
