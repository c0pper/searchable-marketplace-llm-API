import os
import json
from pathlib import Path


def create_text_files(json_list):
    for item in json_list:
        file_name = f"{item['_id']}.txt"
        file_path = os.path.join("docs", file_name)

        with open(file_path, "w") as file:
            file.write(f"[name]: {item['name']}\n")
            file.write(f"[description]: {item['description']}\n")
            file.write(f"[price]: {item['price']}\n")


if __name__ == '__main__':
    file_path = 'all_products.json'
    data = json.loads(Path(file_path).read_text())

    create_text_files(data)