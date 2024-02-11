import flet as ft
from views.registro import registro_view
from views.ingreso import ingreso_view
from views.tareas import tareas_view
from views.logout import logout_view 
from views.categorias import categorias_view

def main(page: ft.Page):
    page.title = "Aplicación Flet con Registro, Ingreso, Gestión de Tareas y Categorías"

    main_content = ft.Column(alignment=ft.MainAxisAlignment.START, expand=True)

    def update_view(index):
        main_content.controls.clear()
        if index == 0:
            main_content.controls.extend(registro_view(page))
        elif index == 1:
            main_content.controls.extend(ingreso_view(page))
        elif index == 2:
            main_content.controls.extend(tareas_view(page))
        elif index == 3:
            main_content.controls.extend(categorias_view(page))
        elif index == 4:  # Manejar la vista de categorías
            main_content.controls.extend(logout_view(page))
        main_content.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.APP_REGISTRATION, label="Registro"),
            ft.NavigationRailDestination(icon=ft.icons.LOGIN, label="Ingreso"),
            ft.NavigationRailDestination(icon=ft.icons.LIST, label="Tareas"),
            ft.NavigationRailDestination(icon=ft.icons.CATEGORY, label="Categorías"),
            ft.NavigationRailDestination(icon=ft.icons.LOGOUT, label="Logout"),
              # Nuevo botón para Categorías
        ],
        on_change=lambda e: update_view(e.control.selected_index),
        group_alignment=-1.0,
    )

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                main_content,
            ],
            expand=True,
        )
    )

    update_view(rail.selected_index)


if __name__ == '__main__':
    ft.app(target=main)
