import logging
import pathlib

from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

DEFAULT_FONT_SIZE = 13
CLASSIFICATION_COLORS = {
    "SECRET": (255, 0, 0),
    "CUI": (0, 255, 0),
}
DEFAULT_CLASSIFICATION_COLOR = (0, 0, 0)
FONT_PATH = "/Users/jon/src/classitag/font/OpenSans-Bold.ttf"
BAR_HEIGHT = 15


def load_image(image_path: pathlib.Path) -> Image.Image:
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        logging.error(f"Error: File not found at {image_path}")
    except Exception as e:
        logging.error(f"Error opening image: {e}")
    return None


def draw_overlay(draw: ImageDraw.Draw, width: int, classification: str) -> None:
    font_size = DEFAULT_FONT_SIZE
    font = ImageFont.truetype(FONT_PATH, font_size)

    classification_upper = classification.upper()

    overlay_color = CLASSIFICATION_COLORS.get(classification_upper, DEFAULT_CLASSIFICATION_COLOR)

    # Draw top overlay
    draw.rectangle([0, 0, width, BAR_HEIGHT], fill=overlay_color)

    # Draw bottom overlay
    draw.rectangle([0, draw.im.size[1] - BAR_HEIGHT, width, draw.im.size[1]], fill=overlay_color)

    text = classification_upper if classification_upper in ["SECRET", "CUI"] else classification

    text_bbox = draw.textbbox((0, 0), text, font=font)

    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] + text_bbox[1]

    text_position_top = ((width - text_width) // 2, (BAR_HEIGHT - text_height) // 2)
    text_position_bottom = (
        (width - text_width) // 2,
        draw.im.size[1] - BAR_HEIGHT + (BAR_HEIGHT - text_height) // 2,
    )

    draw.text(text_position_top, text, font=font, fill=(0, 0, 0))
    draw.text(text_position_bottom, text, font=font, fill=(0, 0, 0))


def save_image_with_overlay(
    img: Image.Image, image_path: pathlib.Path, classification: str
) -> None:
    width, height = img.size

    draw = ImageDraw.Draw(img)
    draw_overlay(draw, width, classification)

    new_file_path = image_path.with_stem(f"({classification.upper()})_{image_path.stem}")
    img.save(new_file_path.with_suffix(".png"))
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


def main() -> None:
    directory_path = pathlib.Path(input("Enter the path to the image directory: ").strip())
    classification = (
        input("Enter the classification (Controlled Unclassified Information (CUI)/Secret): ")
        .strip()
        .title()
    )

    if not directory_path.exists() or not directory_path.is_dir():
        logging.error("Invalid directory path. Exiting.")
        return

    add_overlay_to_directory(directory_path, classification)


if __name__ == "__main__":
    main()
