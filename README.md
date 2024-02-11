
#Instrucciones de Despliegue para Proyecto0
Este proyecto está dividido en dos partes principales: Backend y Frontend. El Backend se ejecuta en un contenedor Docker, mientras que el Frontend es una aplicación Flet que se ejecuta directamente desde Python.

##Requisitos Previos
Docker y Docker Compose (para el backend)
Python 3.8 o superior (para el frontend)
Pip (para instalar dependencias de Python)
Despliegue del Backend
El backend está configurado para ejecutarse en Docker. Para desplegarlo, sigue estos pasos:

##Navega al directorio Backend en tu consola o terminal.

Ejecuta docker-compose up para construir e iniciar los contenedores del backend.
Esto iniciará todos los servicios necesarios definidos en tu docker-compose.yml.

##Ejecución del Frontend
El frontend es una aplicación Flet que requiere Python para su ejecución. Para ejecutarla, realiza los siguientes pasos:

Navega al directorio Frontend en tu consola o terminal.

##Configura un entorno virtual de Python:

bash
Copy code
python -m venv .venv
source .venv/bin/activate  # En Windows usa .venv\Scripts\activate
##Instala las dependencias necesarias:

bash
Copy code
Proyecto0/Backend pip install -r requirements.txt
Proyecto0/Frontend pip install -r requirements.txt

##Ejecuta la aplicación:
dirigete a la carpeta de Frontend
bash
Copy code
python main.py
La aplicación Flet ahora debería estar corriendo en tu navegador por defecto en localhost con el puerto especificado en el código (por defecto el 8502).

##Problemas Conocidos y Solución de Problemas
Si encuentras problemas al ejecutar la aplicación, asegúrate de:

Tener la versión correcta de Python instalada.
Tener activo el docker compose
Tener todas las dependencias de Python necesarias instaladas en tu entorno virtual.
Los puertos que la aplicación necesita no estén siendo utilizados por otro servicio.
Para cualquier otro problema, revisa los registros de errores o abre un issue en el repositorio del proyecto.
