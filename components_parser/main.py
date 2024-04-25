# Библиотеки
import time
import urllib.request
from seleniumwire import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import psycopg2  # Для экспорта в базу данных
from urls import urls
import proxy

# Исключения
CPU_Exceptions = ["Xeon", "LGA1155", "EPYC"]
GPU_Exceptions = ["планка", "Плата синхронизации", "SLI HB BRIDGE", "Intel Arc", "GT 710", "GT 220", "GT 210", "Профессиональный видеоускоритель", "Supermicro", "Sapphire"]
RAM_Exceptions = ["Registered DDR5", "DDR5 ECC", "SO-DIMM DDR5", "LRDIMM DDR4", "Registered DDR4", "DDR4 ECC", "SO-DIMM DDR4 ECC", "SO-DIMM DDR4", "LV Registered DDR3"]
MB_Exceptions = ["Серверная", "SuperMicro", "onboard"]
HDD_Exceptions = ["Серверный", "SAS", "серверный", "IBM", "Hot-Swap"]
CASE_Inclusions = ["без БП"]
CASE_Exceptions = ["Корзина", "Крепление", "панель", "Держатель", "Брекет", "Кронштейн", "Mini-ITX"]


def parser(url: str, find_what: str, component_id: int):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(seleniumwire_options=proxy.proxys[2], options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    items = soup.find_all("a", class_="t")  # Ищем все позиции комплектующих данного типа
    for item in items:
        spec_url = "https://www.nix.ru" + item["href"]  # Страница с конкретным элементом
        driver.set_page_load_timeout(5)
        try:
            driver.get(spec_url)
        except TimeoutException:
            continue
        # Время для загрузки цены
        time.sleep(0.5)
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
                    break
        if images[0] == "https://static.nix.ru/art/picture_coming_soon.gif":
            continue
        image = images[0]
        match find_what:
            case "CPU":
                for exception in CPU_Exceptions:
                    if exception in item.get_text():
                        break
                else:
                    print(cpu_info_parser(soup_info, image, component_id))
                    component_id += 1
            case "GPU":
                for exception in GPU_Exceptions:
                    if exception in item.get_text():
                        break
                else:
                    gpu = gpu_info_parser(soup_info, image, component_id)
                    if not gpu:
                        break
                    print(gpu)
                    component_id += 1
            case "RAM":
                for exception in RAM_Exceptions:
                    if exception in item.get_text():
                        break
                else:
                    print(ram_info_parser(soup_info, image, component_id))
                    component_id += 1
            case "MB":
                for exception in MB_Exceptions:
                    if exception in item.get_text():
                        break
                else:
                    print(mb_info_parser(soup_info, image, component_id))
                    component_id += 1
            case "SSD":
                print(ssd_info_parser(soup_info, image, component_id))
                component_id += 1
            case "POWER":
                print(power_info_parser(soup_info, image, component_id))
                component_id += 1
            case "HDD":
                print(hdd_info_parser(soup_info, image, component_id))
                component_id += 1
            case "CASE":
                for inclusion in CASE_Inclusions:
                    if inclusion not in item.get_text():
                        break
                for exception in CASE_Exceptions:
                    if exception in item.get_text():
                        break
                else:
                    print(case_info_parser(soup_info, image, component_id))
                    component_id += 1
            case "FAN":
                print(fan_info_parser(soup_info, image, component_id))
                component_id += 1
    return component_id

def cpu_info_parser(soup_info, image, id):
    info = {}
    info["Manufacturer"] = soup_info.find("td", id="tdsa2943").get_text().strip()
    info["Model"] = soup_info.find("td", id="tdsa2944").get_text()[:-24]
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

    full = {}
    full["id"] = id
    full["type"] = "cpu"
    full["name"] = "{} {}".format(info["Manufacturer"], info["Model"])
    full["description"] = "{}, {}, {}, {}/{}".format(info["BOX/OEM"], info["Socket"], info["Frequency"], info["Cores"], info["Threads"])
    # full["price"] = int(soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4])
    full["characters"] = info
    full["image_path"] = image
    return full


def gpu_info_parser(soup_info, image, id):
    info = {}
    check_manufacturer = soup_info.find_all("td", id="tdsa2943")
    info["Manufacturer"] = soup_info.find("td", id="tdsa2943").get_text().strip() if len(check_manufacturer) > 0 else "No"
    check_series = soup_info.find_all("td", id="tdsa5562")
    info["Series"] = soup_info.find("td", id="tdsa5562").get_text().strip() if len(check_series) > 0 else "No"
    model = soup_info.find("td", id="tdsa2944").get_text().strip()
    if "проф" in model:
        info["Model"] = model[:-29]
    else:
        info["Model"] = model[:-24]
    gpu = soup_info.find("td", id="tdsa4190").get_text().strip()
    info["GPU"] = gpu[:-27] if "популярный такой же GeForce" in gpu else gpu
    info["Memory"] = soup_info.find("td", id="tdsa689").get_text().strip()
    info["MemoryType"] = soup_info.find("td", id="tdsa4187").get_text().strip()
    info["Interface"] = soup_info.find("td", id="tdsa567").get_text().strip()

    full = {}
    full["id"] = id
    full["type"] = "gpu"
    if info["Series"] == "No":
        full["name"] = "{} {}".format(info["Manufacturer"], info["Model"])
    else:
        full["name"] = "{} {} {}".format(info["Manufacturer"], info["Series"], info["Model"])
    if full["name"] == "Afox GeForce GT610":
        return 0
    full["description"] = "{}, {}".format(info["Memory"], info["MemoryType"])
    # full["price"] = int(soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4])
    full["characters"] = info
    full["image_path"] = image
    return full


def ram_info_parser(soup_info, image, id):
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

    full = {}
    full["id"] = id
    full["type"] = "ram"
    if info["Series"] == "No":
        full["name"] = "{} {}".format(info["Manufacturer"], info["Model"])
    else:
        full["name"] = "{} {} {}".format(info["Manufacturer"], info["Series"], info["Model"])
    full["description"] = "{}, {}, {}".format(info["Type"], info["Memory"], info["Count"])
    # full["price"] = int(soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4])
    full["characters"] = info
    full["image_path"] = image
    return full


def mb_info_parser(soup_info, image, id):
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

    full = {}
    full["id"] = id
    full["type"] = "mb"
    if info["Series"] == "No":
        full["name"] = "{} {}".format(info["Manufacturer"], info["Model"])
    else:
        full["name"] = "{} {} {}".format(info["Manufacturer"], info["Series"], info["Model"])
    full["description"] = "{}, {}".format(info["Socket"], info["Format"])
    # full["price"] = int(soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4])
    full["characters"] = info
    full["image_path"] = image
    return full


def ssd_info_parser(soup_info, image, id):
    info = {}
    info["Manufacturer"] = soup_info.find("td", id="tdsa2943").get_text().strip()
    check_series = soup_info.find_all("td", id="tdsa5562")
    info["Series"] = soup_info.find("td", id="tdsa5562").get_text().strip() if len(check_series) > 0 else "No"
    info["Model"] = soup_info.find("td", id="tdsa2944").get_text().strip()[:-17]
    info["Price"] = soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4]
    info["Memory"] = soup_info.find("td", id="tdsa3978").get_text().strip()[:-28]

    full = {}
    full["id"] = id
    full["type"] = "ssd"
    if info["Series"] == "No":
        full["name"] = "{} {}".format(info["Manufacturer"], info["Model"])
    else:
        full["name"] = "{} {} {}".format(info["Manufacturer"], info["Series"], info["Model"])
    full["description"] = "{}".format(info["Memory"])
    # full["price"] = int(soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4])
    full["characters"] = info
    full["image_path"] = image
    return full


def power_info_parser(soup_info, image, id):
    info = {}
    info["Manufacturer"] = soup_info.find("td", id="tdsa2943").get_text().strip()
    check_series = soup_info.find_all("td", id="tdsa5562")
    info["Series"] = soup_info.find("td", id="tdsa5562").get_text().strip() if len(check_series) > 0 else "No"
    info["Model"] = soup_info.find("td", id="tdsa2944").get_text().strip()[:-26]
    info["Price"] = soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4]
    info["Capacity"] = soup_info.find("td", id="tdsa2123").get_text().strip()

    full = {}
    full["id"] = id
    full["type"] = "power"
    if info["Series"] == "No":
        full["name"] = "{} {}".format(info["Manufacturer"], info["Model"])
    else:
        full["name"] = "{} {} {}".format(info["Manufacturer"], info["Series"], info["Model"])
    full["description"] = "{}".format(info["Capacity"])
    # full["price"] = int(soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4])
    full["characters"] = info
    full["image_path"] = image
    return full

def hdd_info_parser(soup_info, image, id):
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

    full = {}
    full["id"] = id
    full["type"] = "hdd"
    if info["Series"] == "No":
        full["name"] = "{} {}".format(info["Manufacturer"], info["Model"])
    else:
        full["name"] = "{} {} {}".format(info["Manufacturer"], info["Series"], info["Model"])
    full["description"] = "{}".format(info["Volume"])
    # full["price"] = int(soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4])
    full["characters"] = info
    full["image_path"] = image
    return full

def case_info_parser(soup_info, image, id):
    info = {}
    info["Manufacturer"] = soup_info.find("td", id="tdsa2943").get_text().strip()
    check_series = soup_info.find_all("td", id="tdsa5562")
    info["Series"] = soup_info.find("td", id="tdsa5562").get_text().strip() if len(check_series) > 0 else "No"
    info["Model"] = soup_info.find("td", id="tdsa2944").get_text().strip()[:-20]
    info["Price"] = soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4]
    format = soup_info.find("td", id="tdsa643").get_text().strip()
    if format[:3] == "ATX":
        info["Format"] = "ATX"
    elif format[:5] == "E-ATX":
        info["Format"] = "E-ATX"
    elif format[:8] == "MicroATX":
        info["Format"] = "MicroATX"

    full = {}
    full["id"] = id
    full["type"] = "case"
    if info["Series"] == "No":
        full["name"] = "{} {}".format(info["Manufacturer"], info["Model"])
    else:
        full["name"] = "{} {} {}".format(info["Manufacturer"], info["Series"], info["Model"])
    full["description"] = "{}".format(info["Format"])
    # full["price"] = int(soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4])
    full["characters"] = info
    full["image_path"] = image
    return full

def fan_info_parser(soup_info, image, id):
    info = {}
    info["Manufacturer"] = soup_info.find("td", id="tdsa2943").get_text().strip()
    check_series = soup_info.find_all("td", id="tdsa5562")
    info["Series"] = soup_info.find("td", id="tdsa5562").get_text().strip() if len(check_series) > 0 else "No"
    info["Model"] = soup_info.find("td", id="tdsa2944").get_text().strip()
    info["Price"] = soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4]
    info["Socket"] = soup_info.find("td", id="tdsa2118").get_text().strip()
    info["Capacity"] = soup_info.find("td", id="tdsa1754").get_text().strip()

    full = {}
    full["id"] = id
    full["type"] = "fan"
    if info["Series"] == "No":
        full["name"] = "{} {}".format(info["Manufacturer"], info["Model"])
    else:
        full["name"] = "{} {} {}".format(info["Manufacturer"], info["Series"], info["Model"])
    full["description"] = "{}, {}".format(info["Socket"], info["Capacity"])
    # full["price"] = int(soup_info.find("div", class_="price pc-component-non-used pc-component-inactive").find_all("span")[1].get_text().replace("\xa0", "")[:-4])
    full["characters"] = info
    full["image_path"] = image
    return full


if __name__ == "__main__":
    component_id = 1
    # CPU, GPU, RAM, MB, SSD, POWER, HDD, CASE, FAN
    component_id = parser(url=urls["CPU"], find_what="CPU", component_id=component_id)
    component_id = parser(url=urls["GPU"], find_what="GPU", component_id=component_id)
    component_id = parser(url=urls["RAM"], find_what="RAM", component_id=component_id)
    component_id = parser(url=urls["MB"], find_what="MB", component_id=component_id)
    component_id = parser(url=urls["SSD"], find_what="SSD", component_id=component_id)
    component_id = parser(url=urls["POWER"], find_what="POWER", component_id=component_id)
    component_id = parser(url=urls["HDD"], find_what="HDD", component_id=component_id)
    component_id = parser(url=urls["CASE"], find_what="CASE", component_id=component_id)
    parser(url=urls["FAN"], find_what="FAN", component_id=component_id)