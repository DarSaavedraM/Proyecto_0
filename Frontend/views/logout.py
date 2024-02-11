# views/logout_view.py
import flet as ft
from services.auth_service import perform_logout

def logout_view(page: ft.Page):
    def logout():
        # Aquí invocamos el servicio de cierre de sesión
        perform_logout(page)

    # Los diálogos y otros controles de la interfaz de usuario se mantienen en la vista
    dlg_logout = ft.AlertDialog(
        title=ft.Text("Cerrar sesión"),
        content=ft.Text("¿Estás seguro de que deseas cerrar sesión?"),
        actions=[
            ft.TextButton("Sí", on_click=lambda _: page.close_dialog()),
            ft.TextButton("No", on_click=lambda _: page.close_dialog()),
        ],
        on_dismiss=lambda e: print("Dialog dismissed!")
    )

    return [
        ft.Column(
            [
                ft.Text("Para cerrar sesión, presiona el botón de abajo."),
                ft.ElevatedButton("Cerrar sesión", on_click=lambda _: logout())
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
    ]


