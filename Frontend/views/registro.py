import flet as ft
from flet import ElevatedButton, FilePicker, FilePickerResultEvent, TextField, Checkbox, Text, icons
import requests

def registro_view(page: ft.Page):
    
    title = Text(value="REGISTRATE", weight="bold", text_align=ft.TextAlign.CENTER, width=300)
    text_username = TextField(label="Username", width=300)
    text_password = TextField(label="Password", password=True, width=300)
    checkbox_terms = Checkbox(label="Acepto términos y condiciones")
    message = Text()  # Usaremos este Text para mostrar mensajes de estado

    # Función para manejar el resultado de la selección de archivos
    def pick_files_result(e: FilePickerResultEvent):
        if e.files:
            page.uploaded_file_info = e.files[0]
            message.value = "Archivo seleccionado: " + e.files[0].name
        else:
            page.uploaded_file_info = None
            message.value = "No file selected or cancelled."
        message.update()

    file_picker = FilePicker(on_result=pick_files_result)
    pick_files_button = ElevatedButton("Pick files", icon=icons.UPLOAD_FILE, on_click=lambda _: file_picker.pick_files(allow_multiple=False))

    def submit_signup(e):
        if not checkbox_terms.value:
            message.value = "Debes aceptar los términos y condiciones."
            message.update()
            return

        data = {
            "nombre_usuario": text_username.value,
            "contrasena_hash": text_password.value,
        }

        files = None
        if hasattr(page, "uploaded_file_info") and page.uploaded_file_info is not None:
            with open(page.uploaded_file_info.path, "rb") as file_data:
                files = {"imagen_perfil": (page.uploaded_file_info.name, file_data, "multipart/form-data")}
                response = requests.post("http://localhost:8080/usuarios", data=data, files=files)

        else:
            response = requests.post("http://localhost:8080/usuarios", data=data)

        if response.status_code == 201:
            message.value = "Usuario registrado exitosamente."
        else:
            message.value = f"Error al registrar el usuario: {response.text}"
        message.update()

    # Botón para enviar el formulario
    submit_button = ElevatedButton("Sign Up", on_click=submit_signup)

    return [title, text_username, text_password, checkbox_terms, pick_files_button, file_picker, message, submit_button]
