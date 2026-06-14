import requests
import os
from dotenv import load_dotenv
import argparse


def convert_amount(api_key, base_code, target_code, amount):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_code}/{target_code}/{amount}"
    response = requests.get(url)
    conversion_result = response.json()

    return conversion_result


def main():
    load_dotenv()
    api_key = os.getenv("EXCHANGERATE_API_KEY")
    parser = argparse.ArgumentParser(
        description="Принимает аргрументы, где: -b/--base - основная валюта, -t/--target - целевая валюта, -a/--amount - количество валюты"
    )
    parser.add_argument(
        "-b", "--base", default="RUB", help="Введите код основной валюты"
    )
    parser.add_argument(
        "-t", "--target", default="USD", help="Введите код целевой валюты"
    )
    parser.add_argument(
        "-a", "--amount", type=float, default=10000, help="Введите количество валюты"
    )
    args = parser.parse_args()
    base_code = args.base.strip().upper()
    target_code = args.target.strip().upper()
    amount = args.amount
    conversion_result = convert_amount(api_key, base_code, target_code, amount)

    try:
        if conversion_result["result"] == "success":
            print(
                f"Конвертированная сумма: {conversion_result['conversion_result']} {target_code}"
            )
        else:
            print(f"Ошибка API: {conversion_result['error-type']}")
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка HTTPError: {e}")


if __name__ == "__main__":
    main()
