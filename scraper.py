import requests
from bs4 import BeautifulSoup
import json
import csv
import os
import time
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}
SAVE_FOLDER = "scraped_data"
def get_soup(url, parser="html.parser"):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, parser)
    except requests.exceptions.RequestException as e:
        print(f"Could not load {url} -> {e}")
        return None
def scrape_jobs():
    url = "https://realpython.github.io/fake-jobs/"
    soup = get_soup(url)
    if soup is None:
        return []
    jobs = []
    cards = soup.select(".card-content")
    for card in cards:
        title = card.select_one("h2.title")
        company = card.select_one("h3.subtitle")
        location = card.select_one("p.location")
        link_tag = card.select_one("a.card-footer-item")
        job = {
            "title": title.get_text(strip=True) if title else "",
            "company": company.get_text(strip=True) if company else "",
            "location": location.get_text(strip=True) if location else "",
            "apply_link": link_tag["href"] if link_tag else ""
        }
        jobs.append(job)
    return jobs
def scrape_products(pages=2):
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    products = []
    for page_num in range(1, pages + 1):
        url = base_url.format(page_num)
        soup = get_soup(url)
        if soup is None:
            break
        items = soup.select("article.product_pod")
        if not items:
            break
        for item in items:
            name_tag = item.select_one("h3 a")
            price_tag = item.select_one(".price_color")
            rating_tag = item.select_one("p.star-rating")
            link = name_tag["href"] if name_tag else ""
            full_link = "https://books.toscrape.com/catalogue/" + link.replace("../../../", "")
            product = {
                "name": name_tag["title"] if name_tag else "",
                "price": price_tag.get_text(strip=True) if price_tag else "",
                "rating": rating_tag["class"][1] if rating_tag else "",
                "product_link": full_link
            }
            products.append(product)
        time.sleep(1)
    return products
def scrape_news():
    url = "https://feeds.bbci.co.uk/news/rss.xml"
    soup = get_soup(url, parser="xml")
    if soup is None:
        return []
    news_items = []
    entries = soup.find_all("item")
    for entry in entries:
        title = entry.find("title")
        description = entry.find("description")
        pub_date = entry.find("pubDate")
        news = {
            "title": title.get_text(strip=True) if title else "",
            "description": description.get_text(strip=True) if description else "",
            "source": "BBC News",
            "published_date": pub_date.get_text(strip=True) if pub_date else ""
        }
        news_items.append(news)
    return news_items
def filter_data(data, keyword):
    keyword = keyword.lower()
    results = []
    for entry in data:
        combined_text = " ".join(str(v) for v in entry.values()).lower()
        if keyword in combined_text:
            results.append(entry)
    return results
def ensure_folder():
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
def save_as_json(data, filename):
    ensure_folder()
    path = os.path.join(SAVE_FOLDER, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Saved {len(data)} records to {path}")
def save_as_csv(data, filename):
    if not data:
        print("Nothing to save.")
        return
    ensure_folder()
    path = os.path.join(SAVE_FOLDER, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved {len(data)} records to {path}")
def print_preview(data, limit=5):
    if not data:
        print("No records found.")
        return
    for i, entry in enumerate(data[:limit], start=1):
        print(f"\n{i}.")
        for key, value in entry.items():
            print(f"   {key}: {value}")
    if len(data) > limit:
        print(f"\n...and {len(data) - limit} more records.")
def main_menu():
    current_data = []
    current_category = ""
    while True:
        print("\n===== WEB SCRAPER MENU =====")
        print("1. Select Category (Jobs / Products / News)")
        print("2. Scrape Data")
        print("3. Search / Filter Data")
        print("4. Save Data")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            print("\na) Jobs\nb) Products\nc) News")
            pick = input("Choose category: ").strip().lower()
            if pick == "a":
                current_category = "jobs"
            elif pick == "b":
                current_category = "products"
            elif pick == "c":
                current_category = "news"
            else:
                print("Invalid option.")
                continue
            print(f"Category set to: {current_category}")
        elif choice == "2":
            if not current_category:
                print("Please select a category first.")
                continue
            print("Scraping, please wait...")
            if current_category == "jobs":
                current_data = scrape_jobs()
            elif current_category == "products":
                current_data = scrape_products(pages=2)
            elif current_category == "news":
                current_data = scrape_news()
            print(f"Scraped {len(current_data)} records.")
            print_preview(current_data)
        elif choice == "3":
            if not current_data:
                print("No data available. Scrape something first.")
                continue
            keyword = input("Enter keyword to search: ").strip()
            filtered = filter_data(current_data, keyword)
            print(f"Found {len(filtered)} matching records.")
            print_preview(filtered)
        elif choice == "4":
            if not current_data:
                print("No data available to save.")
                continue
            file_format = input("Save as (json/csv): ").strip().lower()
            filename = f"{current_category}_data.{file_format}"
            if file_format == "json":
                save_as_json(current_data, filename)
            elif file_format == "csv":
                save_as_csv(current_data, filename)
            else:
                print("Unsupported format.")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")
if __name__ == "__main__":
    main_menu()