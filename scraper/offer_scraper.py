import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper.translator import translate_en

FIREFOX_BINARY = r"C:\Program Files\Mozilla Firefox\firefox.exe"
GECKODRIVER = r"C:\geckodriver\geckodriver.exe"
PROFILE_PATH = r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\kyazsafw.default-release"

SUPPLIER_NAME_SELECTOR = ".shop-company-name > h1"
SUPPLIER_LINK_SELECTOR = ".shop-company-name"
TOP1_SELECTOR = "#hd_0_container_0 > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1)"
TOP2_SELECTOR = "#hd_0_container_0 > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2)"

def extract_supplier_info(offer_url):
    print(f"🔗 Обработка карточки товара: {offer_url}")
    options = Options()
    options.binary_location = FIREFOX_BINARY
    options.add_argument(f"--profile={PROFILE_PATH}")

    driver = webdriver.Firefox(service=Service(GECKODRIVER), options=options)
    driver.get(offer_url)

    result = {}

    try:
        # Ждём загрузки названия поставщика
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, SUPPLIER_NAME_SELECTOR))
        )

        name_el = driver.find_element(By.CSS_SELECTOR, SUPPLIER_NAME_SELECTOR)
        name_cn = name_el.text.strip()
        name_en = translate_en(name_cn)

        link_el = driver.find_element(By.CSS_SELECTOR, SUPPLIER_LINK_SELECTOR)
        shop_url = link_el.get_attribute("href")

        # Ждём топовые товары
        time.sleep(3)
        top1 = driver.find_element(By.CSS_SELECTOR, TOP1_SELECTOR).text.strip()
        top2 = driver.find_element(By.CSS_SELECTOR, TOP2_SELECTOR).text.strip()

        result = {
            "name_cn": name_cn,
            "name_en": name_en,
            "shop_url": shop_url,
            "top1": top1,
            "top2": top2,
            "source_offer": offer_url
        }

        print(f"✅ Поставщик: {name_en}, Топ-1: {top1}, Топ-2: {top2}")

    except Exception as e:
        print(f"❌ Ошибка при извлечении поставщика: {e}")

    finally:
        driver.quit()

    return result
