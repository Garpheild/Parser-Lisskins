import json
import re
import requests
from bs4 import BeautifulSoup
from time import sleep


headers = {
        'authority': 'lis-skins.ru',
        'accept': '*/*',
        'accept-language': 'ru,en;q=0.9',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
        'x-csrf-token': 'S5XSO6NGKv92EG6Qc2LCxYikqk1jCD14z44DifSN',
        'x-requested-with': 'XMLHttpRequest',
    }

name_dict = {}


def get_id_name_prise():

    response = requests.get('https://lis-skins.ru/market/csgo/', headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    pages = soup.find("ul", class_="pagination").find_all("li", class_="page-item")
    pages_list = [i.text for i in pages]
    max_page = int(pages_list[-2])
    for i in range(1, max_page + 1):
        sleep(1.5)
        response = requests.get(f'https://lis-skins.ru/market/csgo/?page={i}&ajax=1', headers=headers)
        soup = BeautifulSoup(response.json()["skins"], "lxml")

        item_ids = soup.find("div", class_="skins-market-skins-list").find_all("div", class_=re.compile("item market_item market_item_"))
        item_names = soup.find("div", class_="skins-market-skins-list").find_all("img", class_="image")
        item_prises = soup.find("div", class_="skins-market-skins-list").find_all("div", class_="price")

        for item_id, name, prise in zip(item_ids, item_names, item_prises):
            name_dict[item_id.get("data-id")] = {"name": name.get("title"), "prise": prise.text[:-2]}

        print(f"Обработано {i}/{max_page} страниц")


if __name__ == "__main__":
    get_id_name_prise()
    with open("prises.json", "w") as file:
        json.dump(name_dict, file, indent=4)
