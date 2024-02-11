
import flet as ft
from services.categories_service import obtener_categorias, crear_categoria, eliminar_categoria

def categorias_view(page: ft.Page):
    # Verifica si el usuario está autenticado
    if not page.client_storage.get("auth_token"):
        return [ft.Text("Por favor, inicia sesión para gestionar las categorías.")]
    
    page.title = "Gestión de Categorias"
    
    title = ft.Text(value="GESTIÓN DE CATEGORIAS", weight="bold", text_align=ft.TextAlign.CENTER, width=300)
    
    categoria_nombre = ft.TextField(label="Nombre de la categoría", width=300)
    categoria_descripcion = ft.TextField(label="Descripción de la categoría", width=300)
    categoria_id_para_eliminar = ft.TextField(helper_text="ID de Categoria", border=ft.InputBorder.UNDERLINE, width=150)
    message = ft.Text()

    # Botones para las acciones
    crear_btn = ft.ElevatedButton(text="Crear Categoría", icon=ft.icons.ADD, on_click=lambda e: crear_categoria(page, categoria_nombre, categoria_descripcion, message))
    obtener_btn = ft.ElevatedButton(text="Obtener Categorías", icon=ft.icons.SELECT_ALL_ROUNDED , on_click=lambda e: obtener_categorias(page, message))
    eliminar_btn = ft.ElevatedButton(text="Eliminar Categoría (id)", icon=ft.icons.DELETE_FOREVER,on_click=lambda e: eliminar_categoria(page, categoria_id_para_eliminar, message))

    controls = [title,categoria_nombre, categoria_descripcion, categoria_id_para_eliminar, obtener_btn, crear_btn, eliminar_btn, message]
    return controls
