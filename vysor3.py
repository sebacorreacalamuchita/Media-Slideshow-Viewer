import os
import random
import pygame
from PIL import Image
import time

# 📂 Configurar la carpeta de imágenes
CARPETA_FUENTE = r"C:\Users\Escritorio\Desktop\Candy"  # 🔄 Cambia esto a la ruta donde están tus imágenes  C:\Users\Escritorio\Pictures
DURACION_IMAGEN = 5  # ⏳ Duración en segundos de cada imagen

# 📸 Extensiones de imagen permitidas
EXTENSIONES = (".jpg", ".jpeg", ".png", ".bmp", ".gif")

# 🔍 Buscar imágenes en la carpeta y subcarpetas
def buscar_imagenes(carpeta):
    imagenes = []
    for root, _, files in os.walk(carpeta):
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
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()
    indice = 0  # Índice de la imagen actual

    while True:
        try:
            imagen = imagenes[indice]
            img = Image.open(imagen)
            img = img.convert("RGB")

            # Obtener dimensiones de la pantalla
            screen_width, screen_height = screen.get_size()

            # Calcular dimensiones manteniendo la relación de aspecto
            img_width, img_height = img.size
            aspect_ratio = img_width / img_height

            if screen_width / screen_height > aspect_ratio:
                # Ajustar por altura
                new_height = screen_height
                new_width = int(new_height * aspect_ratio)
            else:
                # Ajustar por ancho
                new_width = screen_width
                new_height = int(new_width / aspect_ratio)

            img = img.resize((new_width, new_height), Image.LANCZOS)

            # Centrar la imagen en la pantalla
            x_offset = (screen_width - new_width) // 2
            y_offset = (screen_height - new_height) // 2

            mode = img.mode
            size = img.size
            data = img.tobytes()
            pygame_image = pygame.image.fromstring(data, size, mode)

            screen.fill((0, 0, 0))  # Rellenar el fondo con negro
            screen.blit(pygame_image, (x_offset, y_offset))

            # Renderizar la ruta del archivo
            font = pygame.font.Font(None, 36)  # Fuente predeterminada, tamaño 36
            text_color = (200, 200, 200)  # Color gris claro
            ruta_relativa = os.path.relpath(imagen, CARPETA_FUENTE)  # Ruta relativa desde CARPETA_FUENTE
            text_surface = font.render(ruta_relativa, True, text_color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height - 30))  # Posición centrada en la parte inferior
            screen.blit(text_surface, text_rect)

            pygame.display.flip()

            # Obtener detalles del archivo
            fecha_modificacion = os.path.getmtime(imagen)
            fecha_modificacion_str = f"Última modificación: {time.ctime(fecha_modificacion)}"

            # Manejar eventos
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:  # Flecha derecha
                            indice = (indice + 1) % len(imagenes)  # Ir a la siguiente imagen
                            break
                        elif event.key == pygame.K_LEFT:  # Flecha izquierda
                            indice = (indice - 1) % len(imagenes)  # Ir a la imagen anterior
                            break
                        elif event.key == pygame.K_RETURN:  # Enter para pausar
                            continue
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEMOTION:
                        # Mostrar detalles en la esquina inferior derecha
                        details_font = pygame.font.Font(None, 24)
                        details_surface = details_font.render(fecha_modificacion_str, True, (255, 255, 255))
                        details_rect = details_surface.get_rect(bottomright=(screen_width - 10, screen_height - 10))
                        screen.blit(details_surface, details_rect)
                        pygame.display.flip()

                clock.tick(10)
                break  # Salir del bucle interno para cargar la siguiente imagen

        except Exception as e:
            print(f"❌ Error al cargar {imagen}: {e}")  # Mostrar errores en la consola
            indice = (indice + 1) % len(imagenes)  # Saltar a la siguiente imagen en caso de error

    pygame.quit()

# 🚀 Ejecutar el visor de imágenes
imagenes = buscar_imagenes(CARPETA_FUENTE)
mostrar_imagenes(imagenes)
