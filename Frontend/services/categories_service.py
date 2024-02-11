import requests

def api_request(page, method, endpoint, data=None, item_id=None):
    auth_token = page.client_storage.get("auth_token")
    headers = {"Authorization": f"Bearer {auth_token}"}
    url = f"http://localhost:8080/categorias/{item_id if item_id else ''}"
    
    if method.upper() == 'GET':
        response = requests.get(url, headers=headers)
    elif method.upper() == 'POST':
        response = requests.post(url, json=data, headers=headers)
    elif method.upper() == 'DELETE':
        response = requests.delete(url, headers=headers)
    
    return response

def display_message(message, success, action):
    if success:
        message.value = f"Categoría {action} exitosamente."
    else:
        message.value = f"Error al {action} la categoría."
    message.update()

def obtener_categorias(page, message):
    response = api_request(page, 'GET', '/categorias/')
    if response.status_code == 200:
        categorias = response.json()
        categorias_list = "\n".join([f"ID: {cat['id']} - Nombre: {cat['nombre']} - Descripción: {cat.get('descripcion', 'Sin descripción')}" for cat in categorias])
        message.value = f"Categorías:\n{categorias_list}"
    else:
        message.value = "Error al obtener las categorías."
    message.update()

def crear_categoria(page, categoria_nombre, categoria_descripcion, message):
    data = {
        "nombre": categoria_nombre.value,
        "descripcion": categoria_descripcion.value
    }
    response = api_request(page, 'POST', '/categorias/', data=data)
    display_message(message, response.status_code in [200, 201], 'creada')

def eliminar_categoria(page, categoria_id_para_eliminar, message):
    cat_id = categoria_id_para_eliminar.value
    response = api_request(page, 'DELETE', '/categorias/', item_id=cat_id)
    display_message(message, response.status_code == 200, 'eliminada')
