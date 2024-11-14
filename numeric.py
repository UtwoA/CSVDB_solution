import json

with open("items.json", "r", encoding="cp1251") as file:
    items = json.load(file)

for idx, item in enumerate(items, start=1):
    item["item_id"] = idx

with open("items_with_ids.json", "w", encoding="cp1251") as file:
    json.dump(items, file, ensure_ascii=False, indent=4)

print("Файл успешно пронумерован и сохранён как 'items_with_ids.json'")
