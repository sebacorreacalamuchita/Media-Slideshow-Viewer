import os
import random
import pygame
from PIL import Image
import time
import json
import sys

# Cargar configuraciones desde el archivo JSON
def cargar_configuracion(ruta_config):
    with open(ruta_config, "r") as archivo:
        return json.load(archivo)
    
# Ruta del archivo de configuración
RUTA_CONFIG = os.path.join(os.path.dirname(__file__), "config.json")
config = cargar_configuracion(RUTA_CONFIG)

# Usar configuraciones cargadas
CARPETA_FUENTE = config["ruta_imagenes"]
INCLUIR_SUBCARPETAS = config["incluir_subcarpetas"]
DURACION_IMAGEN = config["duracion_imagen"]
PROPORCION_PANTALLA = config["proporcion_pantalla"]
COLOR_FONDO = tuple(config["color_fondo"])
MOSTRAR_RUTA_ARCHIVO = config["mostrar_ruta_archivo"]
FRAME_RATE = config.get("frame_rate", 30)  # Default to 30 FPS if not specified
EXTENSIONES = tuple(config["extensiones"])  # Cargar extensiones desde el JSON

# 🔍 Buscar imágenes en la carpeta y subcarpetas
def buscar_imagenes(carpeta):
    imagenes = []
    for root, _, files in os.walk(carpeta):
        if not INCLUIR_SUBCARPETAS and root != carpeta:
            continue
        for file in files:
            if file.lower().endswith(EXTENSIONES):
                imagenes.append(os.path.join(root, file))
    return imagenes

# 🖥️ Inicializar pygame para mostrar imágenes
def mostrar_imagenes(imagenes):
    if not imagenes:
        print("⚠️ No se encontraron imágenes en la carpeta ", CARPETA_FUENTE)
        return

    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.mouse.set_visible(True)

    clock = pygame.time.Clock()
    indice = 0  # Índice de la imagen actual

    # Controlar el tiempo de presentación de cada imagen
    start_time = time.time()  # Registrar el tiempo de inicio

    # Manejar eventos
    pausado = False  # Variable para controlar el estado de pausa

    while True:
        try:
            imagen = imagenes[indice]
            img = Image.open(imagen)
            img = img.convert("RGB")

            # Obtener dimensiones de la pantalla
            screen_width, screen_height = screen.get_size()

            # Calcular dimensiones según la configuración de proporción
            img_width, img_height = img.size
            aspect_ratio = img_width / img_height

            if PROPORCION_PANTALLA == "mantener":
                if screen_width / screen_height > aspect_ratio:
                    new_height = screen_height
                    new_width = int(new_height * aspect_ratio)
                else:
                    new_width = screen_width
                    new_height = int(new_width / aspect_ratio)
            elif PROPORCION_PANTALLA == "estirar":
                new_width, new_height = screen_width, screen_height

            img = img.resize((new_width, new_height), Image.LANCZOS)

            # Centrar la imagen en la pantalla
            x_offset = (screen_width - new_width) // 2
            y_offset = (screen_height - new_height) // 2

            mode = img.mode
            size = img.size
            data = img.tobytes()
            pygame_image = pygame.image.fromstring(data, size, mode)

            screen.fill(COLOR_FONDO)
            screen.blit(pygame_image, (x_offset, y_offset))

            if MOSTRAR_RUTA_ARCHIVO:
                font = pygame.font.Font(None, 36)
                text_color = (200, 200, 200)
                ruta_relativa = os.path.relpath(imagen, CARPETA_FUENTE)
                text_surface = font.render(ruta_relativa, True, text_color)
                text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height - 30))
                screen.blit(text_surface, text_rect)

            pygame.display.flip()

            # Manejar eventos
            actualizar_imagen = False  # Bandera para forzar actualización
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and not pausado:
                        indice = (indice + 1) % len(imagenes)
                        actualizar_imagen = True
                        break
                    elif event.key == pygame.K_LEFT and not pausado:
                        indice = (indice - 1) % len(imagenes)
                        actualizar_imagen = True
                        break
                    elif event.key == pygame.K_SPACE:
                        pausado = not pausado  # Alternar entre pausa y reanudar

            # Cambiar a la siguiente imagen automáticamente después de DURACION_IMAGEN segundos
            if not pausado and not actualizar_imagen and time.time() - start_time >= DURACION_IMAGEN:
                indice = (indice + 1) % len(imagenes)
                start_time = time.time()  # Reiniciar el temporizador

            clock.tick(FRAME_RATE)

        except Exception as e:
            print(f"❌ Error al cargar {imagen}: {e}")
    pygame.quit()

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "/s":  # Ejecutar el protector de pantalla
            imagenes = buscar_imagenes(CARPETA_FUENTE)
            mostrar_imagenes(imagenes)
        elif sys.argv[1] == "/c":  # Configuración (puedes implementar una ventana de configuración)
            print("Abrir configuración del protector de pantalla")
        elif sys.argv[1] == "/p":  # Previsualización (puedes implementar una vista previa)
            print("Previsualización del protector de pantalla")
    else:
        # Por defecto, ejecutar el protector de pantalla
        imagenes = buscar_imagenes(CARPETA_FUENTE)
        mostrar_imagenes(imagenes)

if __name__ == "__main__":
    main()