import os
import random
import pygame
from PIL import Image
import time
import json
import sys

# Cargar configuraciones desde el archivo JSON
def load_config(config_path):
    with open(config_path, "r") as file:
        return json.load(file)
    
# Path to config file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
config = load_config(CONFIG_PATH)

# Use loaded configuration
SOURCE_FOLDER = config["image_path"]
INCLUDE_SUBFOLDERS = config["include_subfolders"]
IMAGE_DURATION = config["image_duration"]
SCREEN_RATIO = config["screen_ratio"]
BACKGROUND_COLOR = tuple(config["background_color"])
SHOW_FILE_PATH = config["show_file_path"]
FRAME_RATE = config.get("frame_rate", 30)
EXTENSIONS = tuple(config["extensions"])

# Search for images in the folder (and subfolders if enabled)
def find_images(folder):
    images = []
    for root, _, files in os.walk(folder):
        if not INCLUDE_SUBFOLDERS and root != folder:
            continue
        for file in files:
            if file.lower().endswith(EXTENSIONS):
                images.append(os.path.join(root, file))
    return images

# 🖥️ Inicializar pygame para mostrar imágenes
def display_images(images):
    if not images:
        print("⚠️ No images found in folder: ", SOURCE_FOLDER)
        return

    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.mouse.set_visible(True)

    random.shuffle(images) 
    
    clock = pygame.time.Clock()
    index = 0  

    start_time = time.time()
    paused = False

    while True:
        try:
            image_path = images[index]
            img = Image.open(image_path)
            img = img.convert("RGB")

            screen_width, screen_height = screen.get_size()
            img_width, img_height = img.size
            aspect_ratio = img_width / img_height

            if SCREEN_RATIO == "keep":
                if screen_width / screen_height > aspect_ratio:
                    new_height = screen_height
                    new_width = int(new_height * aspect_ratio)
                else:
                    new_width = screen_width
                    new_height = int(new_width / aspect_ratio)
            elif SCREEN_RATIO == "stretch":
                new_width, new_height = screen_width, screen_height

            img = img.resize((new_width, new_height), Image.LANCZOS)

            x_offset = (screen_width - new_width) // 2
            y_offset = (screen_height - new_height) // 2

            mode = img.mode
            size = img.size
            data = img.tobytes()
            pygame_image = pygame.image.fromstring(data, size, mode)

            screen.fill(BACKGROUND_COLOR)
            screen.blit(pygame_image, (x_offset, y_offset))

            if SHOW_FILE_PATH:
                font = pygame.font.Font(None, 36)
                text_color = (200, 200, 200)
                relative_path = os.path.relpath(image_path, SOURCE_FOLDER)
                text_surface = font.render(relative_path, True, text_color)
                text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height - 30))
                screen.blit(text_surface, text_rect)

            pygame.display.flip()

            # Manejar eventos
            update_image = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and not paused:
                        index = (index + 1) % len(images)
                        update_image = True
                        break
                    elif event.key == pygame.K_LEFT and not paused:
                        index = (index - 1) % len(images)
                        update_image = True
                        break
                    elif event.key == pygame.K_SPACE:
                        paused = not paused

            if not paused and not update_image and time.time() - start_time >= IMAGE_DURATION:
                index = (index + 1) % len(images)
                start_time = time.time()

            clock.tick(FRAME_RATE)

        except Exception as e:
            print(f"❌ Error loading {image_path}: {e}")
    pygame.quit()

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "/s":
            images = find_images(SOURCE_FOLDER)
            display_images(images)
        elif sys.argv[1] == "/c":  # Configuración (puedes implementar una ventana de configuración)
            print("Abrir configuración del protector de pantalla")
        elif sys.argv[1] == "/p":  # Previsualización (puedes implementar una vista previa)
            print("Previsualización del protector de pantalla")
    else:
        images = find_images(SOURCE_FOLDER)
        display_images(images)

if __name__ == "__main__":
    main()