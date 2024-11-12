import csv

COMMISSION_RATE = 0.97

def format_with_thousands_separator(value):
    return f"{int(value):,}".replace(",", ".")

def add_item_to_csv(filename, item_data):
    fieldnames = ['item_name', 'modifier', 'buy_price', 'sell_price', 'sell_commission', 'comment']
    try:
        with open(filename, 'r+', encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if reader.fieldnames is None:
                writer.writeheader()
            writer.writerow(item_data)
    except FileNotFoundError:
        with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(item_data)
    print("Данные успешно добавлены в CSV-файл.")

def search_item_in_csv(filename, keywords=None):
    results = []
    try:
        with open(filename, 'r', encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                item_full_name = f"{row['item_name']} {row['modifier']}".lower()
                if keywords is None or all(keyword.lower() in item_full_name for keyword in keywords):
                    results.append(row)
        if results:
            print(f"Найдено {len(results)} совпадающих товаров:")
            for i, result in enumerate(results, 1):
                print(f"\nТовар {i}:")
                print(f"  Название: {result['item_name']}")
                print(f"  Модификатор: {result['modifier']}")
                print(f"  Цена покупки: {format_with_thousands_separator(float(result['buy_price']))} VC$")
                print(f"  Цена продажи: {format_with_thousands_separator(float(result['sell_price']))} VC$")
                print(f"  Комиссия при продаже: {format_with_thousands_separator(float(result['sell_commission']))} VC$")
                print(f"  Комментарий: {result['comment']}")
            return results
        else:
            print("Совпадающие товары не найдены.")
            return []
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
    except Exception as e:
        print(f"Ошибка при поиске товара: {e}")
    return []


def delete_item_from_csv(filename, keywords):
    try:
        results = search_item_in_csv(filename, keywords)
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
        print("\nВыбранный товар для удаления:")
        print(f"  Название: {selected_item['item_name']}")
        print(f"  Модификатор: {selected_item['modifier']}")
        print(f"  Цена покупки: {format_with_thousands_separator(float(selected_item['buy_price']))} VC$")
        print(f"  Цена продажи: {format_with_thousands_separator(float(selected_item['sell_price']))} VC$")
        print(f"  Комиссия при продаже: {format_with_thousands_separator(float(selected_item['sell_commission']))} VC$")
        print(f"  Комментарий: {selected_item['comment']}")
        confirmation = input("Вы уверены, что хотите удалить этот товар? (y/n): ").lower()
        if confirmation != 'y':
            print("Удаление отменено.")
            return
        rows = []
        with open(filename, 'r', encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = [row for row in reader if not (
                    row['item_name'] == selected_item['item_name'] and row['modifier'] == selected_item['modifier'])]
        with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print("Товар успешно удалён.")
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
    except Exception as e:
        print(f"Ошибка при удалении товара: {e}")

def edit_item_in_csv(filename, keywords):
    try:
        results = search_item_in_csv(filename, keywords)
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
        print(f"  Цена покупки: {format_with_thousands_separator(float(selected_item['buy_price']))} VC$")
        print(f"  Цена продажи: {format_with_thousands_separator(float(selected_item['sell_price']))} VC$")
        print(f"  Комиссия при продаже: {format_with_thousands_separator(float(selected_item['sell_commission']))} VC$")
        print(f"  Комментарий: {selected_item['comment']}")
        confirmation = input("Вы уверены, что хотите редактировать этот товар? (y/n): ").lower()
        if confirmation != 'y':
            print("Редактирование отменено.")
            return
        new_buy_price = float(input("Введите новую цену для ПОКУПКИ (в млн VC$): ")) * 1000000
        new_sell_price = float(input("Введите новую цену для ПРОДАЖИ (в млн VC$): ")) * 1000000
        new_sell_commission = new_sell_price * COMMISSION_RATE
        new_comment = input("Введите новый комментарий: ")
        rows = []
        with open(filename, 'r', encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['item_name'] == selected_item['item_name'] and row['modifier'] == selected_item['modifier']:
                    row['buy_price'] = int(new_buy_price)
                    row['sell_price'] = int(new_sell_price)
                    row['sell_commission'] = int(new_sell_commission)
                    row['comment'] = new_comment
                rows.append(row)
        with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print("Данные о товаре успешно обновлены.")
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
    except Exception as e:
        print(f"Ошибка при редактировании товара: {e}")

# Остальная часть main() остаётся прежней...



def main():
    filename = 'items.csv'

    # Описание функционала программы
    print("""
    Доступные команды:
    a - добавить новый товар
    f - искать товар
    d - удалить товар
    e - редактировать товар
    q - выход из программы
    """)

    while True:
        try:
            command = input("Введите команду: ").lower()
            if command == 'a':
                item_name = input("Введите название предмета:\n")
                up_naming = ['сток', '+12', '+15', '+16']
                comment = input(f'Комментарий для {item_name.upper()}: ')
                for up_name in up_naming:
                    item_name_version = item_name + ' ' + up_name
                    buy_price = float(input(f'Введите цену для ПОКУПКИ для {item_name_version.upper()} в млн VC$: '))
                    buy_price = int(buy_price * 1000000)
                    sell_price = float(input(f'Введите цену для ПРОДАЖИ для {item_name_version.upper()} в млн VC$: '))
                    sell_price = int(sell_price * 1000000)
                    sell_commission = sell_price * COMMISSION_RATE
                    item_data = {
                        'item_name': item_name,
                        'modifier': up_name,
                        'buy_price': buy_price,
                        'sell_price': sell_price,
                        'sell_commission': sell_commission,
                        'comment': comment
                    }
                    add_item_to_csv(filename, item_data)
            elif command == 'f':
                keywords = input("Введите ключевые слова для поиска (через пробел): ").split()
                search_item_in_csv(filename, keywords)
            elif command == 'd':
                keywords = input("Введите ключевые слова для поиска товара (через пробел): ").split()
                delete_item_from_csv(filename, keywords)
            elif command == 'e':
                keywords = input("Введите ключевые слова для поиска товара (через пробел): ").split()
                edit_item_in_csv(filename, keywords)
            elif command == '?':
                print("""
                    Доступные команды:
                    a - добавить новый товар
                    f - искать товар
                    d - удалить товар
                    e - редактировать товар
                    q - выход из программы
                    """)
            elif command == 'q':
                print("Выход из программы.")
                break
            else:
                print("Неизвестная команда. Пожалуйста, введите одну из предложенных команд.")
        except Exception as e:
            print(f"Ошибка: {e}")


main()

