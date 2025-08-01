# scraper/search_scraper.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_offers(driver, keyword, max_pages=1):
    offer_urls = []
    wait = WebDriverWait(driver, 20)

    driver.get("https://www.1688.com/")
    time.sleep(2)

    # Ввод ключевого слова
    search_input = wait.until(EC.presence_of_element_located((By.ID, "alisearch-input")))
    search_input.clear()
    search_input.send_keys(keyword)

    # Кнопка поиска
    search_button = driver.find_element(By.CSS_SELECTOR, ".input-button")
    search_button.click()

    # Ожидание результатов
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-offer-wrapper")))

    for page in range(max_pages):
        print(f"🔍 Страница {page + 1}")
        time.sleep(2)

        cards = driver.find_elements(By.CSS_SELECTOR, "div.search-offer-wrapper a")
        for card in cards:
            url = card.get_attribute("href")
            if url and "offer" in url:
                offer_urls.append(url.split("?")[0])

        # Переход на следующую страницу
        try:
            next_btn = driver.find_element(By.XPATH, "//button[contains(text(),'下一页')]")
            if next_btn.is_enabled():
                next_btn.click()
                wait.until(EC.staleness_of(cards[0]))
            else:
                break
        except:
            break

    return offer_urls
