import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time, random


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    })

    base_url = "https://www.goodreads.com/list/show/1.Best_Books_Ever"

    title, urlList, authors, avgRatings, ratingNums = [], [], [], [], []

    for i in range(1, 51):
        print(f"Scraping page {i} ...")
        try:
            page.goto(f"{base_url}?page={i}", wait_until="domcontentloaded", timeout=90000)
        except Exception as e:
            print(f"Timeout or error on page {i}: {e}")
            continue        
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        book_elements = soup.select("#all_votes tr[itemscope][itemtype='http://schema.org/Book']")

        if not book_elements:
            print(f"No books found on page {i}. Possibly hit end or block.")
            break

        for book in book_elements:
            try:
                a_title = book.select_one("a.bookTitle")
                if not a_title:  # skip empty divs
                    continue
                bookTitle = a_title.get_text(strip=True) if a_title else ""
                bookUrl = "https://www.goodreads.com" + a_title['href'] if a_title and a_title else ""

                a_author = book.select_one("a.authorName")
                author = a_author.get_text(strip=True) if a_author else ""

                ratingText = book.select_one("span.minirating")
                splitRating = ratingText.get_text(strip=True).split("—") if ratingText else []  
                avgRating = splitRating[0].split()[0] if len(splitRating) > 0 else ""
                ratingNum = splitRating[1].split()[0] if len(splitRating) > 1 else "" 
                
                title.append(bookTitle)
                urlList.append(bookUrl)
                authors.append(author)
                avgRatings.append(avgRating)
                ratingNums.append(ratingNum)

            except Exception:
                print(f"Skipping a book on page {i} due to missing data.")

        sleep_time = random.uniform(2, 4)
        print(f"Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)

        if i % 10 == 0:
            time.sleep(random.uniform(9, 15))
        
    browser.close()

goodreads = pd.DataFrame({
    "Title": title,
    "URL": urlList,
    "Author": authors,
    "Average Rating": avgRatings,
    "Number of Ratings": ratingNums,
})

goodreads.to_csv("goodreads_holiday_books.csv", index=False)
goodreads.to_json("goodreads_holiday_books.json", orient="records", indent=2)