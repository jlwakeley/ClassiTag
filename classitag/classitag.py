import logging
import pathlib

import click
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

DEFAULT_FONT_SIZE = 12
CLASSIFICATION_COLORS = {
    "SECRET": (255, 0, 0),
    "CUI": (0, 255, 0),
}
DEFAULT_CLASSIFICATION_COLOR = (0, 0, 0)
BAR_HEIGHT = 15
FONT = "font/ARIALBD.TTF"


def load_image(image_path: pathlib.Path) -> Image.Image:
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        logging.error(f"Error: File not found at {image_path}")
    except Exception as e:
        logging.error(f"Error opening image: {e}")
    return None


def draw_overlay(draw: ImageDraw.Draw, width: int, height: int, classification: str) -> None:
    font = ImageFont.truetype(FONT, DEFAULT_FONT_SIZE)

    classification_upper = classification.upper()

    overlay_color = CLASSIFICATION_COLORS.get(classification_upper, DEFAULT_CLASSIFICATION_COLOR)

    # Calculate top and bottom overlay heights
    top_overlay_height = BAR_HEIGHT
    bottom_overlay_height = BAR_HEIGHT

    # Draw top overlay
    draw.rectangle([0, 0, width, top_overlay_height], fill=overlay_color)

    # Draw bottom overlay
    draw.rectangle([0, height - bottom_overlay_height, width, height], fill=overlay_color)

    text = classification_upper if classification_upper in ["SECRET", "CUI"] else classification

    text_bbox = draw.textbbox((0, 0), text, font=font)

    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] + text_bbox[1]

    text_position_top = ((width - text_width) // 2, (top_overlay_height - text_height) // 2)
    text_position_bottom = (
        (width - text_width) // 2,
        height - bottom_overlay_height + (bottom_overlay_height - text_height) // 2,
    )

    draw.text(text_position_top, text, font=font, fill=(0, 0, 0))
    draw.text(text_position_bottom, text, font=font, fill=(0, 0, 0))


def save_image_with_overlay(
    img: Image.Image, image_path: pathlib.Path, classification: str
) -> None:
    width, height = img.size

    # Create a new image with additional space above and below
    new_img = Image.new("RGB", (width, height + 2 * BAR_HEIGHT), (255, 255, 255))

    # Paste the original image onto the new image
    new_img.paste(img, (0, BAR_HEIGHT))

    draw = ImageDraw.Draw(new_img)
    draw_overlay(draw, width, height + 2 * BAR_HEIGHT, classification)

    new_file_path = image_path.with_stem(f"({classification.upper()})_{image_path.stem}")
    new_img.save(new_file_path.with_suffix(".png"))
    logging.info(f"Overlay added to {new_file_path.with_suffix('.png')}")


def move_to_original_images(original_path: pathlib.Path, file_path: pathlib.Path) -> None:
    original_images_dir = original_path / "original_images"
    original_images_dir.mkdir(parents=True, exist_ok=True)
    new_file_path = original_images_dir / file_path.name
    file_path.replace(new_file_path)
    logging.info(f"Original file moved to: {new_file_path}")


def add_overlay_to_directory(directory_path: pathlib.Path, classification: str) -> None:
    original_path = directory_path.resolve()
    for file_path in directory_path.glob("*"):
        if file_path.is_file() and file_path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
            img = load_image(file_path)
            if img:
                save_image_with_overlay(img, file_path, classification)
                move_to_original_images(original_path, file_path)
        else:
            logging.warning(f"Skipping unsupported file: {file_path}")


def create_command_line_interface(directory_path: pathlib.Path, classification: str) -> None:
    directory_path = pathlib.Path(directory_path)
    if not directory_path.exists() or not directory_path.is_dir():
        logging.error("Invalid directory path. Exiting.")
        return

    add_overlay_to_directory(directory_path, classification)


@click.command()
@click.argument("directory_path", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument("classification", type=click.Choice(["CUI", "SECRET"], case_sensitive=False))
def main(directory_path: pathlib.Path, classification: str) -> None:
    create_command_line_interface(directory_path, classification)


if __name__ == "__main__":
    main()