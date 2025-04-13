# Media Slideshow Viewer

This script displays images in full-screen mode from a specified folder, including its subfolders. It allows users to navigate through images manually or let them cycle automatically. The configuration is managed through a JSON file.

In future versions, support for video playback will be added.

## Features

- Displays images from a specified folder, including subfolders (configurable)
- Supports multiple image formats
- Full-screen mode
- Auto-slideshow with configurable duration per image
- Manual navigation with arrow keys
- Pause and resume functionality
- Displays image file paths (configurable)

## Requirements

- Python 3.x
- Required Python libraries:
  - `pygame`
  - `PIL` (Pillow)
  - `json`
  - `os`
  - `random`
  - `sys`
  - `time`

You can install the required dependencies using:

```sh
pip install pygame pillow
```

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/sebacorreacalamuchita/Media-Slideshow-Viewer.git
   ```
2. Navigate to the project directory:
   ```sh
   cd media-slideshow-viewer
   ```
3. Modify the `config.json` file according to your preferences.
4. Use the provided `.bat` script to create and install the screensaver:
   - Run the `create_screensaver.bat` script located in the `scripts` folder to generate the `.scr` file and install it in the `System32` folder.

   Example:
   ```sh
   scripts\create_screensaver.bat
   ```

   The script will:
   - Verify Python and required dependencies.
   - Generate the screensaver executable.
   - Request administrator permissions to copy the `.scr` file to the `System32` folder.

## Configuration (config.json)

The `config.json` file contains settings for the slideshow:

```json
{
  "image_folder": "C:/path/to/images",
  "include_subfolders": true,
  "image_duration": 5,
  "screen_fit": "maintain",
  "background_color": [0, 0, 0],
  "show_file_path": true,
  "frame_rate": 30,
  "extensions": [".jpg", ".png", ".jpeg"]
}
```

### Explanation of settings:

- `image_folder`: Path to the folder containing images.
- `include_subfolders`: Whether to include images from subfolders.
- `image_duration`: Duration (in seconds) each image is displayed.
- `screen_fit`: How images are displayed on the screen:
  - `maintain`: Keeps the aspect ratio without stretching.
  - `stretch`: Fills the entire screen by stretching.
- `background_color`: Background color when images do not fill the screen.
- `show_file_path`: Display the image path at the bottom of the screen.
- `frame_rate`: Frame rate for smooth transitions.
- `extensions`: Supported image file formats.

## Usage

Run the script with:

```sh
python slideshow.py
```

### Command-line arguments:

- `/s`: Starts the slideshow.
- `/c`: Opens configuration (future feature).
- `/p`: Shows a preview of the slideshow.

Example:

```sh
python slideshow.py /s
```

## Controls

- `Right Arrow`: Next image
- `Left Arrow`: Previous image
- `Spacebar`: Pause/Resume
- `Esc`: Exit the slideshow

## Future Features

- Support for video playback alongside images.
- Additional transition effects between media files.
- Enhanced configuration options.

## License

This project is licensed under the MIT License.

## Contributing

Feel free to fork this repository and submit pull requests with improvements!

---

**Author:** Sebastian Correa **GitHub:** [sebacorreacalamuchita](https://github.com/sebacorreacalamuchita)

