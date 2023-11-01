import requests
from bs4 import BeautifulSoup
import json


def main():
    # headers = {
    #     "Accept": '*/*',
    #     "User Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    # }
    # req = requests.get(url, headers=headers)
    # src = req.text
    # print(src)
    # with open('index.html', 'w') as file:
    #     file.write(src)
    product_name = []
    product_url = []

    with open('index.html', 'r') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    all_table_data = soup.find("tbody").find_all('td')
    for row in all_table_data:
        data = row.find('a')
        if data:
            product_url.append(data.get('href'))
            product_name.append(data.text)
    all_rt = soup.find_all('tr')
    # print(all_rt, sep='\n')
    description = []
    for rt in all_rt:
        descriptions = rt.find_all('td')
        if descriptions:
            description.append(descriptions[-1].text)
    description_list = description[0: 20]
    json_data = {}
    for i in range(20):
        json_data[product_name[i]] = [product_url[i], description_list[i]]

    with open("products.json", "w", ) as file:
        json.dump(json_data, file, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))


if __name__ == '__main__':
    main()
