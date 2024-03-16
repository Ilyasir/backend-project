# Библиотеки
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import psycopg2  # Для экспорта в базу данных
from urls import urls

# Исключения
CPU_Exceptions = ["Xeon", "LGA1155", "EPYC"]
GPU_Exceptions = ["планка", "Плата синхронизации", "SLI HB BRIDGE", "Intel Arc", "GT 710", "GT 220", "GT 210", "Профессиональный видеоускоритель"]
RAM_Exceptions = ["Registered DDR5", "DDR5 ECC", "SO-DIMM DDR5", "LRDIMM DDR4", "Registered DDR4", "DDR4 ECC", "SO-DIMM DDR4 ECC", "SO-DIMM DDR4", "LV Registered DDR3"]
MB_Exceptions = ["Серверная", "SuperMicro", "onboard"]


def parser(url: str, find_what: str):
    options = Options()
    # options.add_argument("--headless=new")
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
        spec_url = "https://www.nix.ru" + item["href"]  # Страница с конкретным элементом
        driver.get(spec_url)
        driver.implicitly_wait(2)
        time.sleep(0.3)
        soup_info = BeautifulSoup(driver.page_source, "html.parser")
        # Контейнер с изображениями
        container = soup_info.find_all("span", class_="carousel-content")
        # Если контейнера нет - изображение только одно
        if len(container) == 0:
            images = [soup_info.find_all("img", id="main_photo")[0]["src"]]
        else:
            images = []
            for img in container[0].find_all("a"):
                if img["href"] != "":
                    images.append(img["href"])
        match find_what:
            case "CPU":
                for exception in CPU_Exceptions:
                    if exception in item.get_text():
                        break
                else:
                    cpu_info_parser(soup_info)
            case "GPU":
                for exception in GPU_Exceptions:
                    if exception in item.get_text():
                        break
                else:
                    gpu_info_parser(soup_info)
            case "RAM":
                for exception in RAM_Exceptions:
                    if exception in item.get_text():
                        break
                else:
                    ram_info_parser(soup_info)
            case "MB":
                for exception in MB_Exceptions:
                    if exception in item.get_text():
                        break
                else:
                    mb_info_parser(soup_info)
            case "SSD":
                ssd_info_parser(soup_info)
            case "POWER":
                power_info_parser(soup_info)


def cpu_info_parser(soup_info):
    info = {}
    info["Manufacturer"] = soup_info.find("td", id="tdsa2943").get_text().strip()
    info["Model"] = soup_info.find("td", id="tdsa2944").get_text()[:-24]
    info["Price"] = soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0","")[:-4]
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
    info["SupportedRAM"] = soup_info.find("td", id="tdsa642").get_text()[:-19]
    info["Cores"] = soup_info.find("td", id="tdsa2557").get_text().strip()
    # Если нет потоков, то вписываем в потоки ядра
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
    info["Price"] = soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0","")[:-4]
    gpu = soup_info.find("td", id="tdsa4190").get_text().strip()
    info["GPU"] = gpu[:-27] if "популярный такой же GeForce" in gpu else gpu
    info["Memory"] = soup_info.find("td", id="tdsa689").get_text().strip()
    info["MemoryType"] = soup_info.find("td", id="tdsa4187").get_text().strip()
    info["Interface"] = soup_info.find("td", id="tdsa567").get_text().strip()
    print(info)


def ram_info_parser(soup_info):
    info = {}
    info["Manufacturer"] = soup_info.find("td", id="tdsa2943").get_text().strip()
    info["Series"] = soup_info.find("td", id="tdsa5562").get_text().strip()
    info["Model"] = soup_info.find("td", id="tdsa2944").get_text().strip()
    info["Price"] = soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0","")[:-4]
    info["Type"] = soup_info.find("td", id="tdsa2510").get_text().strip()[-4:]
    info["Memory"] = soup_info.find("td", id="tdsa3360").get_text().strip()[:-20]
    info["Count"] = soup_info.find("td", id="tdsa4273").get_text().strip()
    info["Frequency"] = soup_info.find("td", id="tdsa1475").get_text().strip()
    check_timings = soup_info.find_all("td", id="tdsa2558")
    info["Timings"] = soup_info.find("td", id="tdsa2558").get_text().strip() if len(check_timings) > 0 else "No"
    print(info)


def mb_info_parser(soup_info):
    info = {}
    info["Manufacturer"] = soup_info.find("td", id="tdsa2943").get_text().strip()
    info["Series"] = soup_info.find("td", id="tdsa5562").get_text().strip()
    info["Model"] = soup_info.find("td", id="tdsa2944").get_text().strip()[:-23]
    info["Price"] = soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4]
    chipset = soup_info.find("td", id="tdsa3362").get_text().strip()
    info["Chipset"] = chipset[:-22] if "характеристики чипсета" in chipset else chipset
    socket = soup_info.find("td", id="tdsa1307").get_text().strip()
    info["Socket"] = socket[:-16] if "подходящий кулер" in socket else socket
    supported_ram = soup_info.find("td", id="tdsa642").get_text().strip()
    info["SupportedRAM"] = supported_ram[:-89] if "описании процессора" in supported_ram else supported_ram
    print(info)


def ssd_info_parser(soup_info):
    info = {}
    info["Manufacturer"] = soup_info.find("td", id="tdsa2943").get_text().strip()
    check_series = soup_info.find_all("td", id="tdsa5562")
    info["Series"] = soup_info.find("td", id="tdsa5562").get_text().strip() if len(check_series) > 0 else "No"
    info["Model"] = soup_info.find("td", id="tdsa2944").get_text().strip()[:-17]
    info["Price"] = soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4]
    info["Memory"] = soup_info.find("td", id="tdsa3978").get_text().strip()[:-28]
    print(info)


def power_info_parser(soup_info):
    info = {}
    info["Manufacturer"] = soup_info.find("td", id="tdsa2943").get_text().strip()
    info["Series"] = soup_info.find("td", id="tdsa5562").get_text().strip()
    info["Model"] = soup_info.find("td", id="tdsa2944").get_text().strip()[:-26]
    info["Price"] = soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4]
    print(info)



if __name__ == "__main__":
    current = "SSD"
    parser(url=urls[current], find_what=current)
