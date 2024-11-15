import json
import requests

COMMISSION_RATE = 0.97


def format_with_thousands_separator(value):
    return f"{int(value):,}".replace(",", ".")


def calculate_net_profit(buy_price, sell_price, commission_rate):
    return sell_price * commission_rate - buy_price


def load_json_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'cp1251'
        if response.text.strip():
            return response.json()
        else:
            print("Получен пустой ответ.")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке данных: {e}")
        return []
    except json.JSONDecodeError:
        print("Ошибка декодирования JSON.")
        return []


def search_item_in_json(url, keywords=None):
    results = []
    data = load_json_from_url(url)

    for item in data:
        # Разделение item_name на части перед и после "<-"
        item_name_parts = item['item_name'].split(" <- ")

        primary_name = f"{item_name_parts[0]} {item['modifier']}".lower()


        # Проверка, что все ключевые слова содержатся именно в primary_name
        if keywords is None or all(keyword.lower() in primary_name for keyword in keywords):
            results.append(item)

    if results:
        print(f"Найдено {len(results)} совпадающих товаров:")
        for i, result in enumerate(results, 1):
            buy_price = float(result['buy_price'])
            sell_price = float(result['sell_price'])
            sell_commission = float(result['sell_price']) * COMMISSION_RATE
            net_profit = calculate_net_profit(buy_price, sell_price, COMMISSION_RATE)

            print(f"\u001b[38;5;15m\nТовар {i}:\u001b[38;5;15m")
            print(f"  \u001b[38;5;15mНазвание: {result['item_name']}\u001b[38;5;15m")
            print(f"  \u001b[38;5;15mМодификатор: {result['modifier']}\u001b[38;5;15m")
            print("-" * 55)
            print(f"  \u001b[38;5;46mЦена покупки: {format_with_thousands_separator(buy_price)} VC$\u001b[38;5;15m")
            print(f"  \u001b[38;5;196mЦена продажи: {format_with_thousands_separator(sell_price)} VC$\u001b[38;5;15m")
            print("-" * 55)
            print(
                f"  \u001b[38;5;183mЦена продажи с учетом комиссии: {format_with_thousands_separator(sell_commission)} VC$\u001b[38;5;15m")
            print(f"  \u001b[38;5;215mЧистая прибыль: {format_with_thousands_separator(net_profit)} VC$\u001b[38;5;15m")
            print(f"  Комментарий: {result['comment']}")
        return results
    else:
        print("Совпадающие товары не найдены.")
        return []


def main():
    url = 'https://github.com/UtwoA/CSVDB_solution/raw/refs/heads/master/fullItems.json'
    print("""Доступные команды:
    f/а - искать товар
    q/й - выход из программы
    """)
    while True:
        command = input("Введите команду: ").lower()
        if command == 'f' or command == 'а':
            keywords = input("Введите ключевые слова для поиска (через пробел): ").split()
            search_item_in_json(url, keywords)
        elif command == 'q' or command == 'й':
            print("Выход из программы.")
            break
        else:
            print("Неизвестная команда.")


main()
