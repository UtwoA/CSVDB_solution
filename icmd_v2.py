import json
import os
from functools import cmp_to_key

COMMISSION_RATE = 0.97

def format_with_thousands_separator(value):
    return f"{int(value):,}".replace(",", ".")

def calculate_net_profit(buy_price, sell_price, commission_rate):
    return sell_price * commission_rate - buy_price

def load_json(filename):
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='cp1251') as file:
            json.dump([], file, ensure_ascii=False, indent=4)
        return []
    with open(filename, 'r', encoding='cp1251') as file:
        return json.load(file)

def save_json(filename, data):
    with open(filename, 'w', encoding='cp1251') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def add_item_to_json(filename, item_data):
    data = load_json(filename)
    data.append(item_data)
    save_json(filename, data)
    print("Данные успешно добавлены в JSON-файл.")

def search_item_in_json(filename, keywords=None):
    results = []
    data = load_json(filename)
    for item in data:
        item_full_name = f"{item['item_name']} {item['modifier']}".lower()
        if keywords is None or all(keyword.lower() in item_full_name for keyword in keywords):
            results.append(item)

    if results:
        print(f"Найдено {len(results)} совпадающих товаров:")
        for i, result in enumerate(results, 1):
            buy_price = float(result['buy_price'])
            sell_price = float(result['sell_price'])
            sell_commission = float(result['sell_price']) * COMMISSION_RATE
            net_profit = calculate_net_profit(buy_price, sell_price, COMMISSION_RATE)
            print(f"\nТовар {i}:")
            print(f"  Название: {result['item_name']}")
            print(f"  Модификатор: {result['modifier']}")
            print("-" * 55)
            print(f"  \u001b[38;5;46mЦена покупки: {format_with_thousands_separator(buy_price)} VC$\u001b[38;5;15m")
            print(f"  \u001b[38;5;196mЦена продажи: {format_with_thousands_separator(sell_price)} VC$\u001b[38;5;15m")
            print("-" * 55)
            print(f"  \u001b[38;5;183mЦена продажи с учетом комиссии: {format_with_thousands_separator(sell_commission)} VC$\u001b[38;5;15m")
            print(f"  \u001b[38;5;215mЧистая прибыль: {format_with_thousands_separator(net_profit)} VC$\u001b[38;5;15m")
            print(f"  Комментарий: {result['comment']}")
        return results
    else:
        print("Совпадающие товары не найдены.")
        return []

def delete_item_from_json(filename, keywords):
    data = load_json(filename)
    results = search_item_in_json(filename, keywords)
    if not results:
        print("Нет товаров для удаления.")
        return

    if len(results) > 1:
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['item_name']} {result['modifier']}")
        choice = int(input("Выберите номер товара для удаления: ")) - 1
        selected_item = results[choice]
    else:
        selected_item = results[0]

    data = [item for item in data if not (
        item['item_name'] == selected_item['item_name'] and item['modifier'] == selected_item['modifier'])]
    save_json(filename, data)
    print("Товар успешно удалён.")

def edit_item_in_json(filename, keywords):
    data = load_json(filename)
    results = search_item_in_json(filename, keywords)
    if not results:
        print("Нет товаров для редактирования.")
        return

    if len(results) > 1:
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['item_name']} {result['modifier']}")
        choice = int(input("Выберите номер товара для редактирования: ")) - 1
        selected_item = results[choice]
    else:
        selected_item = results[0]

    print("\nВыбранный товар для редактирования:")
    print(f"  Название: {selected_item['item_name']}")
    print(f"  Модификатор: {selected_item['modifier']}")
    new_buy_price = float(input("Введите новую цену для ПОКУПКИ (в млн VC$): ")) * 1000000
    new_sell_price = float(input("Введите новую цену для ПРОДАЖИ (в млн VC$): ")) * 1000000
    new_sell_commission = new_sell_price * COMMISSION_RATE
    new_comment = input("Введите новый комментарий: ")

    for item in data:
        if item['item_name'] == selected_item['item_name'] and item['modifier'] == selected_item['modifier']:
            item['buy_price'] = int(new_buy_price)
            item['sell_price'] = int(new_sell_price)
            item['sell_commission'] = int(new_sell_price * 0.97)
            item['comment'] = new_comment

    save_json(filename, data)
    print("Данные о товаре успешно обновлены.")

def main():
    filename = 'items.json'
    print("""Доступные команды:
    a - добавить новый товар
    f - искать товар
    d - удалить товар
    e - редактировать товар
    q - выход из программы
    """)
    while True:
        command = input("Введите команду: ").lower()
        if command == 'a' or command == 'ф':
            item_name = input("Введите название предмета:\n")
            up_naming = ['сток', '+12', '+15', '+16']
            comment = input(f'Комментарий для {item_name.upper()}: ')
            for up_name in up_naming:
                buy_price = float(input(f'Введите цену для ПОКУПКИ для {item_name + " " + up_name} в млн VC$: ')) * 1000000
                sell_price = float(input(f'Введите цену для ПРОДАЖИ для {item_name + " " + up_name} в млн VC$: ')) * 1000000
                sell_commission = sell_price * COMMISSION_RATE
                item_data = {
                    'item_name': item_name,
                    'modifier': up_name,
                    'buy_price': int(buy_price),
                    'sell_price': int(sell_price),
                    'sell_commission': int(sell_commission),
                    'comment': comment
                }
                add_item_to_json(filename, item_data)
        elif command == 'x' or command == 'ч':
            while True:
                item_name = input("Введите название предмета:\n")
                modifier = input(f'Введите модификацию {item_name.upper()}: ')
                buy_price = float(input(f'Введите цену для ПОКУПКИ для {item_name} в млн VC$: ')) * 1000000
                sell_price = float(input(f'Введите цену для ПРОДАЖИ для {item_name} в млн VC$: ')) * 1000000
                sell_commission = sell_price * COMMISSION_RATE
                item_data = {
                    'item_name': item_name,
                    'modifier': modifier,
                    'buy_price': int(buy_price),
                    'sell_price': int(sell_price),
                    'sell_commission': int(sell_commission),
                    'comment': ""
                }
                add_item_to_json(filename, item_data)
        elif command == 'f' or command == 'а':
            keywords = input("Введите ключевые слова для поиска (через пробел): ").split()
            search_item_in_json(filename, keywords)
        elif command == 'r' or command == 'к':
            keywords = input("Введите ключевые слова для поиска товара (через пробел): ").split()
            delete_item_from_json(filename, keywords)
        elif command == 'e' or command == 'у':
            keywords = input("Введите ключевые слова для поиска товара (через пробел): ").split()
            edit_item_in_json(filename, keywords)
        elif command == 'q' or command == 'й':
            print("Выход из программы.")
            break
        else:
            print("Неизвестная команда.")
main()