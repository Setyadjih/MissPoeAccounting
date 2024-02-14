from datetime import datetime

from nicegui import ui

class AppPage():
    def __init__(self):

        with ui.grid(columns=2):
            with ui.column() as left:
                with ui.input('Date', value = datetime.today().strftime("%Y-%m-%d")).classes("w-full") as date:
                    with date.add_slot('append'):
                        ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
                    with ui.menu() as menu:
                        ui.date().bind_value(date)

                ui.select([], label="Vendor").classes("w-full")
                category_select = ui.select([], label="Category").classes("w-full")
                item_select = ui.select([], label="Item").classes("w-full")

                with ui.grid(columns=2):
                    ui.input(label="Quantity")
                    quantity_unit = ui.select([], label="Unit")

                ui.input(label="Harga")
                with ui.grid(columns=2):
                    ui.input(label="Isi")
                    ui.select([], label="Isi Unit")
                ui.input("Merek")
                ui.separator()
                with ui.row().classes(".justify-items-end"):
                    ui.button("Add").props("color=green")

            with ui.column() as right:
                # ui.table()
                ui.label("Test")


AppPage()

ui.run(host='localhost', port=8080)
