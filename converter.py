import img2pdf
from PIL import Image
import os

def image_to_pdf(output_filename, image_list):
    with open(output_filename, "wb") as f:
        pdf_bytes = img2pdf.convert(image_list)
        f.write(pdf_bytes)
    print(f"Successfully created: {output_filename}")

if __name__ == "__main__":
    test_images = ["test.jpg"]
    image_to_pdf("my_result.pdf", test_images)
    