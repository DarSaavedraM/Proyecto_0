import requests

def register_user(page, username, password_hash, selected_file, message):
    data = {
        "nombre_usuario": username,
        "contrasena_hash": password_hash,
    }

    files = None
    if selected_file:
        with open(selected_file["path"], "rb") as file_data:
            files = {"imagen_perfil": (selected_file["name"], file_data, "multipart/form-data")}
    

    if hasattr(page, "selected_file") and page.selected_file is not None:
        with open(page.selected_file.path, "rb") as file_data:
            files = {"imagen_perfil": (page.selected_file.name, file_data, "multipart/form-data")}
            response = requests.post("http://localhost:8080/usuarios", data=data, files=files)
    else:
        response = requests.post("http://localhost:8080/usuarios", data=data)

    if response.status_code == 201:
        message.value = "Usuario registrado exitosamente."
    else:
        message.value = f"Error al registrar el usuario: {response.text}"
    message.update()
