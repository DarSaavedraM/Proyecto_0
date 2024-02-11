import flet as ft
from services.auth_service import login

def ingreso_view(page: ft.Page, on_auth_success=None):
    title = ft.Text(value="INGRESO", weight="bold", text_align=ft.TextAlign.CENTER, width=300)
    text_username = ft.TextField(label="Username", width=300)
    text_password = ft.TextField(label="Password", password=True, width=300)
    message = ft.Text()

    def submit_login(e):
        # Llama a la función de servicio para iniciar sesión
        login(page, text_username.value, text_password.value, message, on_auth_success)

    submit_button = ft.ElevatedButton("Ingresar", icon=ft.icons.LOGIN, on_click=submit_login)

    return [title, text_username, text_password, message, submit_button]
