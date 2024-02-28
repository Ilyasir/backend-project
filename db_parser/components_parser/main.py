import requests
from bs4 import BeautifulSoup
import psycopg2
from urls import urls

CPU_exceptions = ["Xeon", "LGA1155", "EPYC"]
def parser(url:str):
    id = 1
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    items = soup.find_all("a", class_="t") #Ищем все позиции комплектующих данного типа
    for item in items:
        try:
            with psycopg2.connect(dbname='****', user='****', password='****') as conn:
                with conn.cursor() as curs:
                    for i in CPU_exceptions:
                        if i in item.get_text():
                            break
                    else:
                        info_parser("https://www.nix.ru" + item["href"])
                        # curs.execute("INSERT INTO components2 (id, name, type, image) VALUES (%s, %s, %s, %s);",(id, "Оперативная память", "DDR5", images[0]))
                        id += 1
        except DB_connection_exception:
            print("Не получилось подключиться к базе данных")

def cpu_info_parser(url:str):
    res_info = requests.get(url)
    soup_info = BeautifulSoup(res_info.text, "lxml")
    container = soup_info.find_all("span", class_="carousel-content") #Контейнер с изображениями (контейнера нет, если изображение одно)
    if len(container) == 0:
        images = [soup_info.find_all("img", id="main_photo")[0]["src"]]
    else:
        images = [img["href"] for img in container[0].find_all("a")]
    info = {}
    info["Manufacturer"] = soup_info.find("td", id="tdsa2943").get_text().strip()
    info["Model"] = soup_info.find("td", id="tdsa2944").get_text()[:-24]
    info["Price"] = int(soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").get_text()[6:-3])
    info["Socket"] = soup_info.find("td", id="tdsa1307").get_text()[:-22]
    info["BOX/OEM"] = soup_info.find("td", id="tdsa8732").get_text()[:3]
    info["Core"] = soup_info.find("td", id="tdsa1549").get_text().strip()
    info["TechProcess"] = soup_info.find("td", id="tdsa3735").get_text().strip()
    print(info)

if __name__ == "__main__":
    parser(url=urls["CPU"])