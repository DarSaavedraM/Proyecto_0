import requests

def login(page, username, password, message, on_auth_success=None):
    if not username or not password:
        message.value = "Por favor, ingresa tu nombre de usuario y contraseña."
        message.update()
        return

    data = {
        "username": username,
        "password": password,
    }

    # Realiza la solicitud a tu API
    response = requests.post("http://localhost:8080/usuarios/iniciar-sesion", data=data)
    if response.status_code == 200:
        # Suponiendo que tu API devuelve un token de acceso en caso de éxito
        token_data = response.json()
        access_token = token_data.get("access_token", "")
        message.value = "Ingreso exitoso."
        print("Ingreso exitoso. Token:", access_token)

        # Guardar el token en el almacenamiento del cliente
        page.client_storage.set("auth_token", access_token)

        # Invoca el callback de éxito de autenticación si está definido
        if on_auth_success:
            on_auth_success()

        page.update()
    else:
        message.value = "Credenciales incorrectas o error en el servidor."
        print("Credenciales incorrectas o error en el servidor.")
        message.update()

def is_authenticated(page):
    auth_token = page.client_storage.get("auth_token")
    if not auth_token:
        return False, None, "Por favor, inicie sesión primero."
    return True, auth_token, ""

def perform_logout(page):
    page.client_storage.remove("auth_token")
    page.close_dialog()