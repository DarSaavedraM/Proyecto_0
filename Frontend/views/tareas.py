import flet as ft
from datetime import datetime
from services.task_service import add_task, get_tasks, delete_task, update_task, search_task
from services.auth_service import is_authenticated

def tareas_view(page: ft.Page):
    if not page.client_storage.get("auth_token"):
        return [ft.Text("Por favor, inicia sesión para gestionar las tareas.")]
        
    page.title = "Gestión de Tareas"
    
    title = ft.Text(value="GESTIÓN DE TAREAS", weight="bold", text_align=ft.TextAlign.CENTER, width=300)
    task_description = ft.TextField(label="Descripción", width=300)
    task_state = ft.Dropdown(label="Estado", width=300, filled=True, value="Sin Empezar", options=[
        ft.dropdown.Option("Sin Empezar"),
        ft.dropdown.Option("Empezada"),
        ft.dropdown.Option("Finalizada"),
    ])
    category_id = ft.TextField(label="ID de Categoría", width=300)
    task_id_btn = ft.TextField(helper_text="ID de Tarea", border=ft.InputBorder.UNDERLINE, width=150)
    message = ft.Text()

    date_picker = ft.DatePicker(first_date=datetime.now(), last_date=datetime(2025, 12, 31))
    date_button = ft.ElevatedButton("Seleccionar Fecha de Finalización", on_click=lambda _: date_picker.pick_date())

    # Botones para las acciones
    create_button = ft.ElevatedButton("Crear Tarea", icon=ft.icons.ADD, on_click=lambda _: add_task(page, task_description, task_state, category_id, date_picker, message))
    get_tasks_button = ft.ElevatedButton("Consultar Tareas", icon=ft.icons.LIST, on_click=lambda _: get_tasks(page, message))
    delete_button = ft.ElevatedButton("Eliminar Tarea", icon=ft.icons.DELETE, on_click=lambda _: delete_task(page, task_id_btn, message))
    update_button = ft.ElevatedButton("Modificar Tarea", icon=ft.icons.EDIT, on_click=lambda _: update_task(page, task_description, task_state, category_id, date_picker, task_id_btn, message))
    search_button = ft.ElevatedButton("Buscar Tarea", icon=ft.icons.SEARCH, on_click=lambda _: search_task(page, task_id_btn, message))

    return [
        title,
        task_description,
        task_state,
        category_id,
        date_button,
        task_id_btn,
        create_button,
        get_tasks_button,
        delete_button,
        update_button,
        search_button,
        message,
        date_picker  # Asegúrate de añadir el date_picker a la lista de retornos
    ]
