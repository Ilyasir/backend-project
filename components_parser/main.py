# Библиотеки
import time
from seleniumwire import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import psycopg2  # Для экспорта в базу данных
from urls import urls

# Исключения
CPU_Exceptions = ["Xeon", "LGA1155", "EPYC"]
GPU_Exceptions = ["планка", "Плата синхронизации", "SLI HB BRIDGE", "Intel Arc", "GT 710", "GT 220", "GT 210", "Профессиональный видеоускоритель"]
RAM_Exceptions = ["Registered DDR5", "DDR5 ECC", "SO-DIMM DDR5", "LRDIMM DDR4", "Registered DDR4", "DDR4 ECC", "SO-DIMM DDR4 ECC", "SO-DIMM DDR4", "LV Registered DDR3"]
MB_Exceptions = ["Серверная", "SuperMicro", "onboard"]
HDD_Exceptions = ["Серверный", "SAS", "серверный", "IBM", "Hot-Swap"]
CASE_Inclusions = ["без БП"]
CASE_Exceptions = ["Корзина", "Крепление", "панель", "Держатель", "Брекет", "Кронштейн", "Mini-ITX"]


def parser(url: str, find_what: str):
    proxy_options = {
        'proxy': {
            'http': 'socks5://TqFQ6T:PKdwLR@5.101.32.185:8000',
            'https': 'socks5://TqFQ6T:PKdwLR@5.101.32.185:8000',
            'no_proxy': 'localhost,127.0.0.1'
        }
    }
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(seleniumwire_options=proxy_options, options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    items = soup.find_all("a", class_="t")  # Ищем все позиции комплектующих данного типа
    for item in items:
        spec_url = "https://www.nix.ru" + item["href"]  # Страница с конкретным элементом
        driver.set_page_load_timeout(5)
        try:
            driver.get(spec_url)
        except TimeoutException:
            pass
        # Время для загрузки цены
        time.sleep(0.1)
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
        if images[0] == "https://static.nix.ru/art/picture_coming_soon.gif":
            continue
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
            case "HDD":
                hdd_info_parser(soup_info)
            case "CASE":
                for inclusion in CASE_Inclusions:
                    if inclusion not in item.get_text():
                        break
                for exception in CASE_Exceptions:
                    if exception in item.get_text():
                        break
                else:
                    case_info_parser(soup_info)
            case "FAN":
                fan_info_parser(soup_info)


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
    format = soup_info.find("td", id="tdsa643").get_text().strip()
    if format[:3] == "ATX":
        info["Format"] = "ATX"
    elif format[:5] == "E-ATX":
        info["Format"] = "E-ATX"
    elif format[:8] == "MicroATX":
        info["Format"] = "MicroATX"
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
    check_series = soup_info.find_all("td", id="tdsa5562")
    info["Series"] = soup_info.find("td", id="tdsa5562").get_text().strip() if len(check_series) > 0 else "No"
    info["Model"] = soup_info.find("td", id="tdsa2944").get_text().strip()[:-26]
    info["Price"] = soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4]
    info["Capacity"] = soup_info.find("td", id="tdsa2123").get_text().strip()
    print(info)

def hdd_info_parser(soup_info):
    info = {}
    info["Manufacturer"] = soup_info.find("td", id="tdsa2943").get_text().strip()
    check_series = soup_info.find_all("td", id="tdsa5562")
    info["Series"] = soup_info.find("td", id="tdsa5562").get_text().strip() if len(check_series) > 0 else "No"
    check_model = soup_info.find_all("td", id="tdsa2944")
    if len(check_model) > 0:
        info["Model"] = soup_info.find("td", id="tdsa2944").get_text().strip()[:-17]
    else:
        return 0
    info["Price"] = soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4]
    info["Volume"] = soup_info.find("td", id="tdsa3978").get_text().strip()
    print(info)

def case_info_parser(soup_info):
    info = {}
    info["Manufacturer"] = soup_info.find("td", id="tdsa2943").get_text().strip()
    check_series = soup_info.find_all("td", id="tdsa5562")
    info["Series"] = soup_info.find("td", id="tdsa5562").get_text().strip() if len(check_series) > 0 else "No"
    info["Model"] = soup_info.find("td", id="tdsa2944").get_text().strip()[:-20]
    # info["Price"] = soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4]
    format = soup_info.find("td", id="tdsa643").get_text().strip()
    if format[:3] == "ATX":
        info["Format"] = "ATX"
    elif format[:5] == "E-ATX":
        info["Format"] = "E-ATX"
    elif format[:8] == "MicroATX":
        info["Format"] = "MicroATX"
    print(info)

def fan_info_parser(soup_info):
    info = {}
    info["Manufacturer"] = soup_info.find("td", id="tdsa2943").get_text().strip()
    check_series = soup_info.find_all("td", id="tdsa5562")
    info["Series"] = soup_info.find("td", id="tdsa5562").get_text().strip() if len(check_series) > 0 else "No"
    info["Model"] = soup_info.find("td", id="tdsa2944").get_text().strip()
    # info["Price"] = soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4]
    info["Socket"] = soup_info.find("td", id="tdsa2118").get_text().strip()
    info["Capacity"] = soup_info.find("td", id="tdsa1754").get_text().strip()
    print(info)


if __name__ == "__main__":
    # CPU, GPU, RAM, MB, SSD, POWER, HDD, CASE, FAN
    current = "FAN"
    parser(url=urls[current], find_what=current)
