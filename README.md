# ClassiTag - Image Classification Labeling

## Overview

This project provides a tool for adding classification labels to images within a specified directory. These labels are applied to both the top and bottom of each image, indicating the classification of the content.

## Prerequisites

Make sure you have the following prerequisites installed on your system:

- Python 3.11
- Virtualenv (optional but recommended)
- Dependencies listed in `pyproject.toml` (use `poetry install` to install)

## Environment Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/classitag.git
   cd classitag
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Run the bootstrap script to set up dependencies:
    ```bash
    ./bootstrap.sh
    ```
   This script installs system-level dependencies based on your operating system.

4. Install additional project dependencies:

   ```bash
   poetry install
   ```

# Usage

## Command-line Interface

The main functionality is exposed through a command-line interface (CLI). The CLI takes two arguments:

1. `directory_path`: The path to the directory containing the images.
2. `classification`: The classification type to be applied as an overlay (`CUI` or `SECRET`).

To add classification overlays to images in a directory, use the following command:

```bash
python classitag.py /path/to/directory secret 
```
Replace `/path/to/directory` with the path to the directory containing your images. You can also specify the classification type (`CUI` or `SECRET`).

This command results in the labeling as seen below.

![image](example_images/(SECRET)_Hyperion_SC2_DevRend1.png)

# Development

## Running Tests

To run tests, use the following command:

```bash
poetry run pytest
```
## Dependencies

The project relies on the following Python libraries:

- `logging`: Standard library for logging messages.
- `click`: A command-line interface creation kit.
- `Pillow`: Python Imaging Library (PIL) for image processing.

## Notes

- The Python version utilized is 3.11.6
- The classification arguments are not case sensative.
- Supported image formats: PNG, JPG, JPEG, BMP.

## Contributing

Contributions are welcome! If you encounter issues or have suggestions, please open an issue or create a pull request.

