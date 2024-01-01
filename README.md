# ClassiTag README

## Overview

This project provides a tool for adding classification labels to images within a specified directory. These labels are applied to both the top and bottom of each image, indicating the classification of the content.

## Bootstrap

To set up the project, run the following bootstrap script:

```bash
python script/bootstrap
```

This script ensures that the required dependencies are installed. Make sure you have Python installed on your system.

## Usage

### Command-line Interface

The main functionality is exposed through a command-line interface (CLI). The CLI takes two arguments:

1. `directory_path`: The path to the directory containing the images.
2. `classification`: The classification type to be applied as an overlay (`CUI` or `SECRET`).

Example:

```bash
python classify.py /path/to/images_directory secret
```
This command results in the labeling as seen below.

![image](test_images/(SECRET)_Hyperion_SC2_DevRend1.png)

### Functionality

The script iterates through each file in the specified directory, identifies supported image formats (e.g., PNG, JPG, JPEG), and adds classification overlays. The original images are then moved to a new "original_images" directory within the specified directory.

### Configuration

The project includes default configurations such as font size, colors for different classifications, and font file path. These configurations can be adjusted within the script for customization.

## Dependencies

The project relies on the following Python libraries:

- `logging`: Standard library for logging messages.
- `click`: A command-line interface creation kit.
- `PIL`: Python Imaging Library for image processing.

## Notes

- The Python version utilized is 3.11.6
- The classification arguments are not case sensative.
- Supported image formats: PNG, JPG, JPEG.

For more information or assistance, please refer to the documentation or contact the project maintainers.
