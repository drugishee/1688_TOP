# scraper/search_scraper.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_offers(driver, keyword, max_pages=2):
    driver.get("https://www.1688.com/")

    try:
        search_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#alisearch-input"))
        )
        search_input.clear()
        search_input.send_keys(keyword)

        search_button = driver.find_element(By.CSS_SELECTOR, ".input-button")
        search_button.click()

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-offer-item"))
        )
    except Exception as e:
        print(f"❌ Ошибка поиска: {e}")
        return []

    offer_urls = set()

    for page in range(1, max_pages + 1):
        print(f"🔍 Парсинг страницы {page}...")
        time.sleep(3)

        cards = driver.find_elements(By.CSS_SELECTOR, "div.search-offer-item")
        print(f"  🔗 Найдено карточек: {len(cards)}")

        for card in cards:
            try:
                link_el = card.find_element(By.XPATH, ".//ancestor::a[1]")
                href = link_el.get_attribute("href")
                if href and "offer/" in href:
                    href = href.split("?")[0]
                    offer_urls.add(href)
            except Exception as e:
                print(f"⚠️ Ошибка карточки: {e}")
                continue

        try:
            next_btn = driver.find_element(By.XPATH, "//button[contains(text(),'下一页')]")
            if next_btn.is_enabled():
                next_btn.click()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-offer-item"))
                )
        except Exception as e:
            print("⚠️ Кнопка 'Следующая' не найдена или не работает.")
            break

    return list(offer_urls)
