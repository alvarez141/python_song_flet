# Music Player

Este es un reproductor de música simple creado con Flet y Pygame. Permite reproducir archivos MP3 desde una carpeta específica y muestra información sobre la canción actual, incluyendo el título y la duración.

## Requisitos

- Python 3.7 o superior
- Flet
- Pygame
- Mutagen

## Instalación

1. Clona este repositorio:
   ```sh
   git clone https://github.com/tu_usuario/musica_python.git
   cd musica_python
   ```

2. Crea un entorno virtual y actívalo:
python -m venv venv
```sh
venv\Scripts\activate  # En Windows
source venv/bin/activate  # En macOS/Linux
```

3. Instala las dependencias:
```sh
pip install -r requirements.txt
```
USO
 1. Asegúrate de tener una carpeta llamada canciones en el mismo directorio que app.py, y coloca tus archivos MP3 en esa carpeta.
 2. Ejecuta la aplicación:
 python app.py