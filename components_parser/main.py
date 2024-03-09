# Библиотеки
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import psycopg2  # Для экспорта в базу данных
from urls import urls

# Исключения
Exceptions = ["Xeon", "LGA1155", "EPYC", "планка", "Плата синхронизации", "SLI HB BRIDGE", "Intel Arc", "GT 710", "GT 220", "GT 210"]


def parser(url: str, find_what: str):
    options = Options()
    options.page_load_strategy = "normal"
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    items = soup.find_all("a", class_="t")  # Ищем все позиции комплектующих данного типа
    for item in items:
        # С импортом в базу данных
        # try:
        #     with psycopg2.connect(dbname='****', user='****', password='****') as conn:
        #         with conn.cursor() as curs:
        #             for i in CPU_exceptions:
        #                 if i in item.get_text():
        #                     break
        #             else:
        #                 cpu_info_parser("https://www.nix.ru" + item["href"])
        #                 curs.execute(***)
        #                 id += 1
        # except:
        #     print("Не получилось подключиться к базе данных")
        #     break
        # Без импорта
        for i in Exceptions:
            if i in item.get_text():
                break
        else:
            spec_url = "https://www.nix.ru" + item["href"]  # Страница с конкретным элементом
            driver.get(spec_url)
            soup_info = BeautifulSoup(driver.page_source, "lxml")
            # Контейнер с изображениями
            container = soup_info.find_all("span", class_="carousel-content")
            # Если контейнера нет - изображение только одно
            if len(container) == 0:
                images = [soup_info.find_all("img", id="main_photo")[0]["src"]]
            else:
                images = [img["href"] for img in container[0].find_all("a")]
            match find_what:
                case "CPU":
                    cpu_info_parser(soup_info)
                case "GPU":
                    gpu_info_parser(soup_info)
                    print(images)


def cpu_info_parser(soup_info):
    info = {}
    info["Manufacturer"] = soup_info.find("td", id="tdsa2943").get_text().strip()
    info["Model"] = soup_info.find("td", id="tdsa2944").get_text()[:-24]
    # info["Price"] = int(soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").get_text()[6:-3])
    info["Socket"] = soup_info.find("td", id="tdsa1307").get_text()[:-22]
    info["BOX/OEM"] = soup_info.find("td", id="tdsa8732").get_text()[:3]
    core = soup_info.find("td", id="tdsa1549").get_text().strip()
    info["Core"] = core[:-23] if core[-3:] == "CPU" else core
    info["TechProcess"] = soup_info.find("td", id="tdsa3735").get_text().strip()
    frequency = soup_info.find("td", id="tdsa3808").get_text().strip()
    info["Frequency"] = frequency + " Boost" if frequency[-5:] == "Turbo" else frequency
    check_video = soup_info.find_all("td", id="tdsa5486")
    if len(check_video) > 0:
        video = soup_info.find("td", id="tdsa5486").get_text().strip()
        info["VideoCore"] = "No" if video == "Нет встроенной видеокарты" else video
    else:
        info["VideoCore"] = "No"
    info["Supported_RAM"] = soup_info.find("td", id="tdsa642").get_text()[:-19]
    info["Cores"] = soup_info.find("td", id="tdsa2557").get_text().strip()
    check_threads = soup_info.find_all("td", id="tdsa23450")
    info["Threads"] = soup_info.find("td", id="tdsa23450").get_text().strip() if len(check_threads) > 0 else soup_info.find("td", id="tdsa2557").get_text().strip()
    info["TDP"] = soup_info.find("td", id="tdsa1754").get_text().strip()
    print(info)


def gpu_info_parser(soup_info):
    info = {}
    check_manufacturer = soup_info.find_all("td", id="tdsa2943")
    info["Manufacturer"] = soup_info.find("td", id="tdsa2943").get_text().strip() if len(check_manufacturer) > 0 else "No"
    check_series = soup_info.find_all("td", id="tdsa5562")
    info["Series"] = soup_info.find("td", id="tdsa5562").get_text().strip() if len(check_series) > 0 else "No"
    info["Model"] = soup_info.find("td", id="tdsa2944").get_text().strip()[:-29]
    gpu = soup_info.find("td", id="tdsa4190").get_text().strip()
    info["GPU"] = gpu[:-27] if "популярный такой же GeForce" in gpu else gpu
    info["Memory"] = soup_info.find("td", id="tdsa689").get_text().strip()
    info["MemoryType"] = soup_info.find("td", id="tdsa4187").get_text().strip()
    info["Interface"] = soup_info.find("td", id="tdsa567").get_text().strip()
    print(info)


if __name__ == "__main__":
    parser(url=urls["CPU"], find_what="CPU")
