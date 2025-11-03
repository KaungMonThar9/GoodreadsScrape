from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time, random, json

start_index = 0 
with open("goodreads_holiday_books.json", "r", encoding="utf-8") as f:
    books = json.load(f)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    })

    for id, book in enumerate(books[start_index:], start=start_index + 1):
        url = book.get("URL")
        if not url:
            book["Genres"] = ""
            continue

        page.goto(url, wait_until="domcontentloaded", timeout=90000)
        try:
            page.wait_for_selector('[data-testid="genresList"]', timeout=10000)
            print(f"Scraping genres for: {book['Title']}")
        except Exception as e:
            print("Genres not found:", e)
            genres = None
        try:
            soup = BeautifulSoup(page.content(), "html.parser")

            genre_spans = soup.select('div[data-testid="genresList"] a span.Button__labelItem')[:5]
            genres = [g.get_text(strip=True) for g in genre_spans]
            
            pageAmt = soup.select('div.BookDetails p[data-testid="pagesFormat"]')
            pageAmt = pageAmt[0].get_text(strip=True).split()[0] if pageAmt else ""
            pubYear = soup.select('div.BookDetails p[data-testid="publicationInfo"]')
            pubYear = pubYear[0].get_text(strip=True).split()[-1] if pubYear else ""

            book["Genres"] = ", ".join(genres) if genres else ""
            book["Page Count"] = pageAmt
            book["Publication Year"] = pubYear

        except Exception as e:
            print(f"Failed to fetch genres for {url}: {e}")

        sleep_time = random.uniform(3, 5)
        print(f"Sleeping {sleep_time:.2f}s...")
        time.sleep(sleep_time)

        if id % 10 == 0:
                with open("goodreads_books_with_genres.json", "w", encoding="utf-8") as f:
                    json.dump(books[:id], f, indent=2, ensure_ascii=False)
                print(f"Autosaved progress at {id} books.")

    browser.close()

# Save new enriched JSON
with open("goodreads_books_with_genres.json", "w", encoding="utf-8") as f:
    json.dump(books, f, indent=2, ensure_ascii=False)

print("Finished adding genres!")