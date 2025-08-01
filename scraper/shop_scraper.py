# shop_scraper.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper.translator import translate_en

def extract_supplier_and_top(driver, offer_url):
    driver.get(offer_url)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.shop-company-name"))
        )
    except:
        print(f"❌ Не удалось загрузить: {offer_url}")
        return None

    try:
        name_cn = driver.find_element(By.CSS_SELECTOR, "h1.shop-company-name").text.strip()
        name_en = translate_en(name_cn)
        shop_link = driver.find_element(By.CSS_SELECTOR, "a.shop-company-name").get_attribute("href").split("?")[0]
    except:
        name_cn, name_en, shop_link = "❓", "Unknown", ""

    print(f"🏬 Поставщик: {name_en} | Ссылка: {shop_link}")

    top1 = top2 = ""

    try:
        top1 = driver.find_element(By.CSS_SELECTOR, "#hd_0_container_0 div:nth-child(1) div:nth-child(2) div:nth-child(1) div:nth-child(1) div:nth-child(2) div:nth-child(3) div:nth-child(1)").text.strip()
    except:
        pass
    try:
        top2 = driver.find_element(By.CSS_SELECTOR, "#hd_0_container_0 div:nth-child(1) div:nth-child(2) div:nth-child(1) div:nth-child(1) div:nth-child(2) div:nth-child(3) div:nth-child(2)").text.strip()
    except:
        pass

    return {
        "supplier_name_cn": name_cn,
        "supplier_name_en": name_en,
        "shop_url": shop_link,
        "top1": top1,
        "top2": top2,
        "offer_url": offer_url
    }
