import os
import random
import pygame
from PIL import Image
import time
import json
import sys
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, ttk

# Cargar configuraciones desde el archivo JSON
def load_config(config_path):
    with open(config_path, "r") as file:
        return json.load(file)


def get_config_candidates():
    candidates = []
    seen = set()

    for base_path in [__file__, sys.executable, sys.argv[0]]:
        if not base_path:
            continue
        try:
            base_dir = os.path.dirname(os.path.abspath(base_path))
        except Exception:
            continue
        if base_dir in seen:
            continue
        seen.add(base_dir)
        candidates.append(os.path.join(base_dir, "config.json"))

    appdata_dir = os.getenv("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
    fallback_dir = os.path.join(appdata_dir, "Vysor3")
    candidates.append(os.path.join(fallback_dir, "config.json"))
    candidates.append(os.path.join(os.path.expanduser("~"), "Vysor3", "config.json"))
    return candidates


def resolve_config_path():
    for candidate in get_config_candidates():
        if os.path.isfile(candidate):
            return candidate

    fallback_path = get_config_candidates()[-2]
    os.makedirs(os.path.dirname(fallback_path), exist_ok=True)
    return fallback_path


def save_config(config_path, config_data):
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w") as file:
        json.dump(config_data, file, indent=4)
        file.write("\n")


def apply_config(config_data):
    global SOURCE_FOLDER, INCLUDE_SUBFOLDERS, IMAGE_DURATION, SCREEN_RATIO, BACKGROUND_COLOR, SHOW_FILE_PATH, FRAME_RATE, EXTENSIONS
    SOURCE_FOLDER = config_data["image_path"]
    INCLUDE_SUBFOLDERS = config_data["include_subfolders"]
    IMAGE_DURATION = config_data["image_duration"]
    SCREEN_RATIO = config_data["screen_ratio"]
    BACKGROUND_COLOR = tuple(config_data["background_color"])
    SHOW_FILE_PATH = config_data["show_file_path"]
    FRAME_RATE = config_data.get("frame_rate", 30)
    EXTENSIONS = tuple(config_data["extensions"])

# Path to config file
CONFIG_PATH = resolve_config_path()
if not os.path.isfile(CONFIG_PATH):
    default_config = {
        "image_path": os.path.expanduser("~/Pictures"),
        "screen_ratio": "keep",
        "background_color": [0, 0, 0],
        "show_file_path": True,
        "extensions": [".jpg", ".jpeg", ".png", ".bmp", ".gif"],
    }
    save_config(CONFIG_PATH, default_config)

config = load_config(CONFIG_PATH)

# Use loaded configuration
apply_config(config)


def normalize_extensions(value):
    extensions = []
    for item in value.split(","):
        ext = item.strip().lower()
        if not ext:
            continue
        if not ext.startswith("."):
            ext = f".{ext}"
        extensions.append(ext)
    return extensions


def show_config_dialog():
    root = tk.Tk()
    root.title("Vysor3 - Configuración")
    root.geometry("640x440")
    root.resizable(False, False)

    main_frame = ttk.Frame(root, padding=16)
    main_frame.pack(fill="both", expand=True)

    image_path_var = tk.StringVar(value=SOURCE_FOLDER)
    include_subfolders_var = tk.BooleanVar(value=INCLUDE_SUBFOLDERS)
    image_duration_var = tk.IntVar(value=int(IMAGE_DURATION))
    screen_ratio_var = tk.StringVar(value=SCREEN_RATIO)
    background_color_var = tk.StringVar(value="#%02x%02x%02x" % BACKGROUND_COLOR)
    show_file_path_var = tk.BooleanVar(value=SHOW_FILE_PATH)
    extensions_var = tk.StringVar(value=", ".join(EXTENSIONS))

    ttk.Label(main_frame, text="Ruta de imágenes:").grid(row=0, column=0, sticky="w", pady=(0, 6))
    path_entry = ttk.Entry(main_frame, textvariable=image_path_var, width=60)
    path_entry.grid(row=1, column=0, columnspan=2, sticky="ew")

    def browse_folder():
        selected_folder = filedialog.askdirectory(
            initialdir=image_path_var.get() or os.path.expanduser("~"),
            title="Selecciona la carpeta de imágenes"
        )
        if selected_folder:
            image_path_var.set(selected_folder)

    browse_button = ttk.Button(main_frame, text="Explorar", command=browse_folder)
    browse_button.grid(row=1, column=2, padx=(8, 0), sticky="ew")

    ttk.Checkbutton(main_frame, text="Incluir subcarpetas", variable=include_subfolders_var).grid(row=2, column=0, columnspan=3, sticky="w", pady=(8, 8))

    ttk.Label(main_frame, text="Duración de cada imagen (segundos):").grid(row=3, column=0, sticky="w", pady=(0, 6))
    ttk.Spinbox(main_frame, from_=1, to=120, textvariable=image_duration_var, width=12).grid(row=4, column=0, sticky="w")

    ttk.Label(main_frame, text="Ajuste de pantalla:").grid(row=3, column=1, sticky="w", padx=(16, 0), pady=(0, 6))
    ratio_combo = ttk.Combobox(main_frame, textvariable=screen_ratio_var, values=["keep", "stretch"], state="readonly", width=16)
    ratio_combo.grid(row=4, column=1, sticky="w", padx=(16, 0))

    ttk.Label(main_frame, text="Color de fondo:").grid(row=5, column=0, sticky="w", pady=(10, 6))
    color_button = ttk.Button(main_frame, text="Elegir color", command=lambda: None)
    color_button.grid(row=6, column=0, sticky="w")

    def pick_color():
        selected = colorchooser.askcolor(initialcolor=background_color_var.get(), title="Elige el color de fondo")
        if selected[1]:
            background_color_var.set(selected[1])

    color_button.configure(command=pick_color)

    color_preview = ttk.Label(main_frame, text="███", foreground=background_color_var.get(), background=background_color_var.get())
    color_preview.grid(row=6, column=1, sticky="w", padx=(10, 0))

    ttk.Checkbutton(main_frame, text="Mostrar ruta del archivo", variable=show_file_path_var).grid(row=7, column=0, columnspan=3, sticky="w", pady=(10, 6))

    ttk.Label(main_frame, text="Extensiones permitidas (separadas por comas):").grid(row=8, column=0, columnspan=3, sticky="w", pady=(0, 6))
    ttk.Entry(main_frame, textvariable=extensions_var, width=80).grid(row=9, column=0, columnspan=3, sticky="ew")

    def save_settings():
        try:
            duration = max(1, int(image_duration_var.get()))
            color_value = background_color_var.get()
            if not color_value.startswith("#"):
                color_value = f"#{color_value}"
            rgb = tuple(int(color_value[i:i+2], 16) for i in (1, 3, 5))
            new_config = {
                "image_path": image_path_var.get().strip() or SOURCE_FOLDER,
                "include_subfolders": bool(include_subfolders_var.get()),
                "image_duration": duration,
                "screen_ratio": screen_ratio_var.get() or "keep",
                "background_color": [rgb[0], rgb[1], rgb[2]],
                "show_file_path": bool(show_file_path_var.get()),
                "extensions": normalize_extensions(extensions_var.get()),
            }
            if not new_config["extensions"]:
                new_config["extensions"] = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
            save_config(CONFIG_PATH, new_config)
            apply_config(new_config)
            messagebox.showinfo("Configuración guardada", "Los cambios se han guardado correctamente.")
            root.destroy()
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo guardar la configuración: {exc}")

    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=10, column=0, columnspan=3, sticky="e", pady=(16, 0))
    ttk.Button(button_frame, text="Guardar", command=save_settings).pack(side="left")
    ttk.Button(button_frame, text="Cancelar", command=root.destroy).pack(side="left", padx=(8, 0))

    root.mainloop()

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
            # Correct orientation using EXIF if available
            try:
                exif = img._getexif()
                if exif is not None:
                    orientation_key = 274  # cf ExifTags
                    if orientation_key in exif:
                        orientation = exif[orientation_key]
                        if orientation == 3:
                            img = img.rotate(180, expand=True)
                        elif orientation == 6:
                            img = img.rotate(270, expand=True)
                        elif orientation == 8:
                            img = img.rotate(90, expand=True)
            except Exception:
                pass

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
            img.close()
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
                    if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_SPACE, pygame.K_e]:
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
                        elif event.key == pygame.K_e:
                            # Pause slideshow and open Windows Explorer with the current image selected
                            import subprocess
                            try:
                                paused = True
                                pygame.display.iconify()  # Minimize the window
                                subprocess.Popen(['explorer', '/select,', image_path])
                                # The slideshow remains paused until user presses SPACE again
                            except Exception as open_err:
                                print(f"Error opening Explorer: {open_err}")

            if not paused and not update_image and time.time() - start_time >= IMAGE_DURATION:
                index = (index + 1) % len(images)
                start_time = time.time()

            clock.tick(FRAME_RATE)

        except Exception as e:
            print(f"❌ Error loading {image_path}: {e}")
    pygame.quit()


def print_help():
    print("Uso: vysor3.exe [opción] [ruta]")
    print("Opciones:")
    print("  /s [ruta]   Ejecutar el protector de pantalla usando la ruta de imágenes especificada.")
    print("              Si no se indica ruta, se usa la carpeta configurada en config.json.")
    print("  /c          Abrir el cuadro de diálogo de configuración")
    print("  /p          Modo vista previa (no se muestra en pantalla completa)")
    print("  /h, /?      Mostrar esta ayuda")
    print("")
    print("Ejemplo:")
    print("  vysor3.exe /s \"C:\\Users\\TuUsuario\\Pictures\\Screensaver\"")
    print("")
    print("Esto permite cambiar la carpeta de imágenes en tiempo de ejecución sin editar config.json ni recompilar.")


def preview_mode():
    # Windows often invokes the screensaver with /p from the Screen Saver Settings dialog.
    # We intentionally do not launch the full-screen slideshow in preview mode.
    time.sleep(2)


def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg.startswith("/") or arg.startswith("-"):
            arg = arg[1:]

        if arg in ["h", "?", "help"] or arg.startswith("h"):
            print_help()
            return

        if arg.startswith("s"):
            source_folder = SOURCE_FOLDER
            if len(sys.argv) > 2 and sys.argv[2].strip():
                source_folder = sys.argv[2]
            images = find_images(source_folder)
            display_images(images)
            return

        if arg.startswith("c"):
            show_config_dialog()
            return

        if arg.startswith("p"):
            preview_mode()
            return

        print("Opción no reconocida.")
        print_help()
        return

    images = find_images(SOURCE_FOLDER)
    display_images(images)

if __name__ == "__main__":
    main()