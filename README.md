Web Scraper CLI

A simple Python command-line tool that scrapes jobs, products, and news from real websites, lets you search/filter the results by keyword, and export everything to JSON or CSV.

Features


Scrape job listings, book/product listings, or news headlines
Keyword search across scraped data
Export results to JSON or CSV
Simple menu-driven interface (no coding needed to use it)
Handles network/site errors gracefully


Data Sources

CategorySourceFieldsJobsrealpython.github.io/fake-jobstitle, company, location, apply linkProductsbooks.toscrape.comname, price, rating, product linkNewsBBC News RSS feedtitle, description, source, published date

Requirements


Python 3.7+
Packages: requests, beautifulsoup4, lxml


Installation

bashpip install requests beautifulsoup4 lxml

Usage

Run the script:

bashpython scraper.py

You'll see a menu:

===== WEB SCRAPER MENU =====
1. Select Category (Jobs / Products / News)
2. Scrape Data
3. Search / Filter Data
4. Save Data
5. Exit

Steps:


Choose option 1 and pick a category (a for Jobs, b for Products, c for News)
Choose option 2 to scrape the data — a preview will be shown
Choose option 3 to search the scraped data by any keyword
Choose option 4 to save the data as json or csv
Choose option 5 to exit


All saved files go into a folder called scraped_data in the same directory as the script.

Example

Enter your choice: 1
Choose category: b

Enter your choice: 2
Scraping, please wait...
Scraped 20 records.

Enter your choice: 3
Enter keyword to search: Light

Enter your choice: 4
Save as (json/csv): csv
Saved 3 records to scraped_data/products_data.csv

Notes


This project is for learning/practice purposes and uses websites that are safe for scraping practice.
If a site is down or changes its layout, the script will show an error instead of crashing.
for demo video click here
https://drive.google.com/file/d/1dlGvZVx8d_kd2gMMGm3obxq-reoXP9iP/view?usp=drive_link


License

Free to use and modify.
