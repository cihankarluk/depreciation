import requests
import re


def search_comma_to_dot(string):
    if ',' in string:
        string = string.replace(',', '.')
    return string


def regex_search(response, pattern):
    content = response.content
    if isinstance(content, bytes):
        content = content.decode("utf-8", "ignore")
    try:
        string = re.search(pattern, content).group()
    except AttributeError:
        print("Try another date.")
        exit()
    string = search_comma_to_dot(string)
    exchange_rate = re.search("\d{1,3}.\d{2,4}", string).group()
    return float(exchange_rate)


def get_current_usd_exchange_rate():
    response = requests.get("http://bigpara.hurriyet.com.tr/doviz/dolar/")
    pattern = """span\sclass="value\sup">\d,\d{4}<"""
    return regex_search(response, pattern)


def get_current_gold_exchange_rate():
    response = requests.get("http://bigpara.hurriyet.com.tr/altin/")
    pattern = """span\sclass="value">\d{3},\d{2}<"""
    return regex_search(response, pattern)


def get_given_usd_exchange_rate(date):
    response = requests.get(
        f"http://bigpara.hurriyet.com.tr/doviz/merkez-bankasi-doviz-kurlari/{date}")
    pattern = """<li\sclass="cell015">\d,\d{4}<"""
    return regex_search(response, pattern)


def get_given_gold_exchange_rate(date):
    date = date.split("-")
    date_format = f"{date[2]}/{date[1]}/{date[0]}"
    response = requests.get(f"https://altin.in/arsiv/{date_format}")
    pattern = """Gram\sAltn\s-\sAl">\d{2,3}.\d{4}<"""
    return regex_search(response, pattern)


if __name__ == '__main__':
    print("Are you paid in dollars? (yes/no)")
    answer = input()
    if answer in ['yes', 'y']:
        print("You have nothing to worry about :)")
        exit()

    print("Starting date of work:(dd-mm-yyyy)")
    start_date = input()
    print("Net salary:")
    try:
        net_salary = int(input())
    except ValueError:
        print("Wrong input.")
        exit()

    date_usd_rate = get_given_usd_exchange_rate(start_date)

    current_usd_rate = get_current_usd_exchange_rate()

    date_gold_rate = get_given_gold_exchange_rate(start_date)
    current_gold_rate = get_current_gold_exchange_rate()

    start_date_usd_worth = net_salary / date_usd_rate
    current_usd_worth = net_salary / current_usd_rate
    loss_usd = start_date_usd_worth - current_usd_worth

    start_date_gold_worth = net_salary / date_gold_rate
    current_gold_worth = net_salary / current_gold_rate
    loss_gold = start_date_gold_worth - current_gold_worth

    print(f"First salary USD worth {start_date_usd_worth}")
    print(f"Last salary USD worth {current_usd_worth}")
    print(f"Lost in USD {loss_usd}")
    print(f"First salary gold (gr) worth {start_date_gold_worth}")
    print(f"Last salary gold (gr) worth {current_gold_worth}")
    print(f"Lost in gold(gr) {loss_gold}")
