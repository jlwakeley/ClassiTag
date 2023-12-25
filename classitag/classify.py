import PyPDF2
from PIL import Image, ImageDraw, ImageFont
import os


def add_overlay(image_path, classification):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    width, height = img.size
    font_size = min(width, height) // 10
    font = ImageFont.truetype("arial.ttf", font_size)

    # Set overlay color based on classification
    if classification == "Secret":
        overlay_color = (255, 0, 0)  # Red
    elif classification == "Controlled Unclassified Information":
        overlay_color = (0, 255, 0)  # Green
    else:
        print("Invalid classification. Exiting.")
        return

    # Add overlay with the classification name in the middle
    draw.rectangle([0, 0, width, height], fill=overlay_color)
    text_width, text_height = draw.textsize(classification, font)
    text_position = ((width - text_width) // 2, (height - text_height) // 2)
    draw.text(text_position, classification, font=font, fill=(255, 255, 255))

    # Save the modified image
    base_name, ext = os.path.splitext(image_path)
    new_file_path = f"{base_name}_{classification}{ext}"
    img.save(new_file_path)
    print(f"Overlay added to {new_file_path}")


def main():
    file_path = input("Enter the path of the PDF or image file: ").strip()
    classification = input(
        "Enter the classification (Classified/Unclassified/Secret): "
    ).strip()

    if not os.path.isfile(file_path):
        print("Invalid file path. Exiting.")
        return

    if file_path.lower().endswith(".pdf"):
        # Add overlay to each page of the PDF
        with open(file_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                img = page.extract_text()  # Extract image as text (not pixel-based)
                img_path = f"temp_page_{page_num + 1}.png"
                img.save(img_path)
                add_overlay(img_path, classification)
                os.remove(img_path)
    elif any(file_path.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg"]):
        # Add overlay to the image
        add_overlay(file_path, classification)
    else:
        print("Unsupported file format. Exiting.")


if __name__ == "__main__":
    main()
