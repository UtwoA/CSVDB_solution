import pytesseract
from PIL import Image
import re
import json
import os


def extract_prices_and_items(text):

    price_pattern = re.compile(r'(\d[\d\s]+)')
    prices = [int(match.replace(" ", "")) for match in price_pattern.findall(text)]

    if len(prices) != 12:
        raise ValueError("Unexpected number of price values found. Check the OCR output or modify the code.")

    item_lines = [line for line in text.splitlines() if "делориан" in line.lower() or "экспрес" in line.lower()]

    if len(item_lines) < 4:
        raise ValueError("Could not detect the expected item names and modifiers.")

    items = [
        {"item_name": item_lines[0].strip(), "modifier": "сток"},
        {"item_name": item_lines[1].strip(), "modifier": "+12"},
        {"item_name": item_lines[2].strip(), "modifier": "+15"},
        {"item_name": item_lines[3].strip(), "modifier": "+16"}
    ]

    for i, item in enumerate(items):
        item["buy_price"] = prices[i * 3]
        item["sell_price"] = prices[i * 3 + 1]
        item["sell_commission"] = prices[i * 3 + 2]
        item["comments"] = ""

    return items


def process_image_to_json(image_path, output_json_path):
    image = Image.open(image_path)

    text = pytesseract.image_to_string(image, lang='rus+eng')

    items = extract_prices_and_items(text)

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=4)


def process_images_in_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_dir, filename)
            json_filename = os.path.splitext(filename)[0] + '.json'
            output_json_path = os.path.join(output_dir, json_filename)

            try:
                process_image_to_json(image_path, output_json_path)
                print(f'Processed {filename} to {json_filename}')
            except Exception as e:
                print(f"Error processing {filename}: {e}")


input_directory = 'path/to/your/image_directory'
output_directory = 'path/to/your/output_directory'
process_images_in_directory(input_directory, output_directory)
