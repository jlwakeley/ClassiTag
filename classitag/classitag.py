import logging
import pathlib
import tkinter as tk
from tkinter import filedialog

import click
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

DEFAULT_FONT_SIZE = 25
CLASSIFICATION_COLORS = {
    "SECRET": (200, 16, 46),
    "CUI": (80, 43, 133),
    "UNCLASSIFIED": (0, 122, 51),
}
DEFAULT_CLASSIFICATION_COLOR = (0, 122, 51)
BAR_HEIGHT = 40
FONT = pathlib.Path(__file__).parent / ".." / "font" / "ARIALBD.TTF"


def load_image(image_path: pathlib.Path) -> Image.Image | None:
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        logging.error(f"Error: File not found at {image_path}")
    except Exception as e:
        logging.error(f"Error opening image: {e}")
    return None


def draw_overlay(draw: ImageDraw.ImageDraw, width: int, height: int, classification: str) -> None:
    font = ImageFont.truetype(str(FONT), DEFAULT_FONT_SIZE)

    classification_upper = classification.upper()

    overlay_color = CLASSIFICATION_COLORS.get(classification_upper, DEFAULT_CLASSIFICATION_COLOR)

    top_overlay_height = BAR_HEIGHT
    bottom_overlay_height = BAR_HEIGHT

    draw.rectangle([0, 0, width, top_overlay_height], fill=overlay_color)  # type: ignore # noqa: PGH003
    draw.rectangle([0, height - bottom_overlay_height, width, height], fill=overlay_color)  # type: ignore # noqa: PGH003

    text = (
        classification_upper
        if classification_upper in {"SECRET", "CUI", "UNCLASSIFIED"}
        else classification
    )

    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] + text_bbox[1]

    text_position_top = ((width - text_width) // 2, (top_overlay_height - text_height) // 2)
    text_position_bottom = (
        (width - text_width) // 2,
        height - bottom_overlay_height + (bottom_overlay_height - text_height) // 2,
    )

    draw.text(text_position_top, text, font=font, fill=(255, 255, 255))
    draw.text(text_position_bottom, text, font=font, fill=(255, 255, 255))


def add_border(img: Image.Image, border_thickness: int) -> Image.Image:
    width, height = img.size

    bordered_img = Image.new(
        "RGB",
        (width + 2 * border_thickness, height + 2 * border_thickness),
        (0, 0, 0),
    )
    bordered_img.paste(img, (border_thickness, border_thickness))

    return bordered_img


def save_image_with_overlay(
    img: Image.Image, image_path: pathlib.Path, classification: str, border_thickness: int = 5
) -> None:
    width, height = img.size

    total_height = height + 2 * BAR_HEIGHT

    new_img = Image.new("RGB", (width, total_height), (0, 0, 0))

    draw = ImageDraw.Draw(new_img)
    draw_overlay(draw, width, total_height, classification)

    new_img.paste(img, (0, BAR_HEIGHT))

    bordered_img = add_border(new_img, border_thickness)

    new_file_path = image_path.with_stem(f"({classification.upper()[0]}) {image_path.stem}")
    bordered_img.save(new_file_path.with_suffix(".png"))


def move_to_original_images(original_path: pathlib.Path, file_path: pathlib.Path) -> None:
    original_images_dir = original_path / "original_images"
    original_images_dir.mkdir(parents=True, exist_ok=True)
    new_file_path = original_images_dir / file_path.name
    file_path.replace(new_file_path)
    logging.info(f"Original file moved to: {new_file_path}")


def add_overlay_to_directory(directory_path: pathlib.Path, classification: str) -> None:
    original_path = directory_path.resolve()
    for file_path in directory_path.glob("*"):
        if file_path.is_file() and file_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".bmp"}:
            img = load_image(file_path)
            if img:
                save_image_with_overlay(img, file_path, classification)
                move_to_original_images(original_path, file_path)
        else:
            logging.warning(f"Skipping unsupported file: {file_path}")


def create_gui() -> None:
    def browse_directory() -> None:
        directory_path = filedialog.askdirectory()
        dir_entry.delete(0, tk.END)
        dir_entry.insert(0, directory_path)

    def start_labeling() -> None:
        directory_path = dir_entry.get()
        classification_type = classification_var.get()
        create_command_line_interface(directory_path, classification_type)  # type: ignore # noqa: PGH003

    root = tk.Tk()
    root.title("ClassiTag")
    root.configure(bg="#f2f2f2")

    header_font = ("Helvetica", 16, "bold")
    button_font = ("Helvetica", 10, "bold")

    dir_label = tk.Label(
        root, text="Select Image Directory:", font=header_font, padx=10, pady=5, bg="#f2f2f2"
    )
    dir_label.grid(row=0, column=0, columnspan=2, sticky="ew")

    dir_entry = tk.Entry(root, width=30)
    dir_entry.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

    browse_button = tk.Button(root, text="Browse", command=browse_directory, padx=10)
    browse_button.grid(row=1, column=1, pady=5, padx=10, sticky="ew")

    class_label = tk.Label(
        root, text="Select Classification Type:", font=header_font, padx=10, pady=5, bg="#f2f2f2"
    )
    class_label.grid(row=2, column=0, columnspan=2, sticky="ew")

    classification_options = ["UNCLASSIFIED", "CUI", "SECRET"]
    classification_var = tk.StringVar(root)
    classification_var.set(classification_options[0])

    for i, option in enumerate(classification_options):
        rb = tk.Radiobutton(
            root, text=option, variable=classification_var, value=option, bg="#f2f2f2", padx=10
        )
        rb.grid(row=3 + i, column=0, columnspan=2, sticky="w", padx=10, pady=2)

    label_button = tk.Button(
        root,
        text="Start Labeling",
        command=start_labeling,
        bg="#004953",
        fg="white",
        width=20,
        height=2,
        font=button_font,
    )
    label_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    root.grid_rowconfigure(0, minsize=20)
    root.grid_rowconfigure(7, minsize=20)
    root.grid_columnconfigure(0, minsize=20)
    root.grid_columnconfigure(1, minsize=20)

    root.mainloop()


def create_command_line_interface(directory_path: pathlib.Path, classification: str) -> None:
    directory_path = pathlib.Path(directory_path)
    if not directory_path.exists() or not directory_path.is_dir():
        logging.error("Invalid directory path. Exiting.")
        return

    add_overlay_to_directory(directory_path, classification)


@click.command()
@click.argument(
    "directory_path", type=click.Path(exists=True, file_okay=False, dir_okay=True), required=False
)
@click.argument(
    "classification",
    type=click.Choice(["CUI", "SECRET", "UNCLASSIFIED"], case_sensitive=False),
    required=False,
)
def main(directory_path: pathlib.Path, classification: str) -> None:
    """
    This project provides a tool for adding classification labels to images within a specified directory. These labels are applied to both the top and bottom of each image, indicating the classification of the content.

    directory_path = The path to the directory containing the images. Optional when using GUI mode.
    classification = The classification type to be applied as an overlay ("CUI", "SECRET" or "UNCLASSIFIED"). Optional when using GUI mode.
    """
    if directory_path is None:
        create_gui()
    elif classification:
        create_command_line_interface(directory_path, classification)
    else:
        logging.error("Classification type is missing. Exiting.")


if __name__ == "__main__":
    main()
