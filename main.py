import csv
import json
import logging
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from scraper.search_scraper import search_offers
from scraper.shop_scraper import extract_supplier_and_top

FIREFOX_BINARY = r"C:\\Program Files\\Mozilla Firefox\\firefox.exe"
GECKODRIVER = r"C:\\geckodriver\\geckodriver.exe"
PROFILE_PATH = r"C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\kyazsafw.default-release"

SEEN_FILE = Path("db/seen_suppliers.json")
RESULTS_JSON = Path("results.json")
RESULTS_CSV = Path("results.csv")

def load_seen():
    try:
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()

def save_seen(seen):
    SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(seen), f, ensure_ascii=False, indent=2)

def save_results(results):
    with open(RESULTS_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    if results:
        with open(RESULTS_CSV, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
            writer.writeheader()
            writer.writerows(results)

def run(keyword, max_pages=1):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    options = Options()
    options.binary_location = FIREFOX_BINARY
    options.add_argument(f"--profile={PROFILE_PATH}")
    driver = webdriver.Firefox(service=Service(GECKODRIVER), options=options)

    seen = load_seen()
    results = []

    try:
        urls = search_offers(driver, keyword, max_pages)
        logging.info("Получено %d ссылок", len(urls))
        for url in urls:
            try:
                info = extract_supplier_and_top(driver, url)
                if not info:
                    continue
                shop_url = info.get("shop_url")
                if shop_url in seen:
                    logging.info("Пропуск уже обработанного поставщика: %s", shop_url)
                    continue
                results.append(info)
                seen.add(shop_url)
            except Exception as e:
                logging.exception("Ошибка при обработке %s: %s", url, e)
        save_results(results)
    finally:
        save_seen(seen)
        driver.quit()
    return results

if __name__ == "__main__":
    run("секонд хенд", max_pages=1)
