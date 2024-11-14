import json

with open("items_with_ids.json", "r", encoding="cp1251") as file:
    items = json.load(file)

for item in items:
    if item.get("comment") == "":
        del item["comment"]
    if "sell_commission" in item:
        del item["sell_commission"]

with open("items_cleaned.json", "w", encoding="cp1251") as file:
    json.dump(items, file, ensure_ascii=False, indent=4)

print("Файл успешно обработан и сохранён как 'items_cleaned.json'")
