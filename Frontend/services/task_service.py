import requests
from datetime import datetime
from services.auth_service import is_authenticated


def add_task(page, task_description, task_state, category_id, date_picker, message):
    authenticated, auth_token, error_message = is_authenticated(page)
    if not authenticated:
        message.value = error_message
        message.update()
        return
       
    fecha_finalizacion = date_picker.value.strftime('%Y-%m-%d') if date_picker.value else None

    task_data = {
        "texto": task_description.value,
        "fecha_creacion": datetime.now().strftime('%Y-%m-%d'),
        "fecha_finalizacion": fecha_finalizacion,
        "estado": task_state.value,
        "id_categoria": int(category_id.value) if category_id.value.isdigit() else 0,
    }

    # Deberías obtener el token de autenticación como parte de la verificación
    # La función is_authenticated ahora devuelve el token además del estado de autenticación
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = requests.post("http://localhost:8080/tareas/", json=task_data, headers=headers)
    
    if response.status_code == 201:
        message.value = "Tarea creada exitosamente."
    else:
        message.value = f"Error al crear la tarea: {response.text}"
    message.update()

def get_tasks(page, message):
    authenticated, auth_token, error_message = is_authenticated(page)
    if not authenticated:
        message.value = error_message
        message.update()
        return

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get("http://localhost:8080/tareas/usuario", headers=headers)

    if response.status_code == 200:
        tasks = response.json()
        tasks_list = "\n".join([f" - ID: {task['id']} - Tarea: {task['texto']}- Categoria: {task['id_categoria']}- Estado: {task['estado']} - Finaliza: {task.get('fecha_finalizacion', 'Sin fecha')}" for task in tasks])
        message.value = f"Tareas Usuario:\n{tasks_list}"
    else:
        message.value = f"Error al obtener las tareas: {response.text}"
    page.update()

def delete_task(page, task_id_btn, message):
    authenticated, auth_token, error_message = is_authenticated(page)
    if not authenticated:
        message.value = error_message
        message.update()
        return
    
    task_id = task_id_btn.value
    if not task_id.isdigit():
        message.value = "Por favor, ingrese un ID de tarea válido."
        message.update()
        return

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.delete(f"http://localhost:8080/tareas/{task_id}", headers=headers)

    if response.status_code == 200:
        message.value = "Tarea eliminada exitosamente."
    else:
        message.value = f"Error al eliminar la tarea: {response.text}"
    message.update()

def update_task(page, task_description, task_state, category_id, date_picker, task_id_btn, message):
    authenticated, auth_token, error_message = is_authenticated(page)
    if not authenticated:
        message.value = error_message
        message.update()
        return

    task_id = task_id_btn.value
    if not task_id.isdigit():
        message.value = "Por favor, ingrese un ID de tarea válido."
        message.update()
        return

    fecha_finalizacion = date_picker.value.strftime('%Y-%m-%d') if date_picker.value else None

    task_data = {
        "texto": task_description.value,
        "fecha_finalizacion": fecha_finalizacion,
        "estado": task_state.value,
        "id_categoria": int(category_id.value) if category_id.value.isdigit() else 0,
    }

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.put(f"http://localhost:8080/tareas/{task_id}", json=task_data, headers=headers)

    if response.status_code == 200:
        message.value = "Tarea modificada exitosamente."
    else:
        message.value = f"Error al modificar la tarea: {response.text}"
    message.update()

def search_task(page, task_id_btn, message):
    authenticated, auth_token, error_message = is_authenticated(page)
    if not authenticated:
        message.value = error_message
        message.update()
        return
    
    task_id = task_id_btn.value
    if not task_id.isdigit():
        message.value = "Por favor, ingrese un ID de tarea válido."
        message.update()
        return

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"http://localhost:8080/tareas/{task_id}", headers=headers)

    if response.status_code == 200:
        task = response.json()
        task_info = f"ID: {task['id']} - Descripción: {task['texto']}- Categoria: {task['id_categoria']} - Estado: {task['estado']} - Fecha de finalización: {task.get('fecha_finalizacion', 'Sin fecha')}"
        message.value = f"Tarea encontrada:\n{task_info}"
    else:
        message.value = f"Error al buscar la tarea: {response.text}"
    message.update()