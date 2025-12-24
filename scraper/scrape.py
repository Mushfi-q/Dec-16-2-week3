import time
import requests
import psycopg2
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

url = "https://books.toscrape.com/"

ratingMap = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def getCategories():
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    category_tags = (
        soup.find("ul", class_="nav nav-list")
            .find("ul")
            .find_all("a")
    )

    categories = []

    for tag in category_tags:
        categories.append({
            "category": tag.get_text(strip=True),
            "url": urljoin(url, tag.get("href"))
        })

    return categories


def get_all_pages(category_url):
  pages=[]
  currentUrl=category_url
  while True:
    #print(f"Scraping page: {currentUrl}")
    pages.append(currentUrl)

    
    page=requests.get(currentUrl)
    soup=BeautifulSoup(page.text, 'html.parser')

    nxtBtn=soup.find('li',class_='next')

    if nxtBtn:
      nxtPage= nxtBtn.find('a')["href"]
      currentUrl=urljoin(currentUrl,nxtPage)
    else:
      break

  return pages


def getAllBooksUrl(category_url):
    booksUrl = []

    pages = get_all_pages(category_url)

    for page_url in pages:
        response = requests.get(page_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.find_all('article', class_="product_pod")

        for article in articles:
            relLink = article.find('h3').find('a')['href']
            fullLink = urljoin(page_url, relLink)
            booksUrl.append(fullLink)

    return booksUrl


def bookDetails(booksUrl):

    try:
        req_start = time.perf_counter()
        response=requests.get(booksUrl)
        response.encoding = "utf-8"
        req_end = time.perf_counter()

        request_time = req_end - req_start

        parse_start = time.perf_counter()
        soup=BeautifulSoup(response.text, 'html.parser')

        #title
        title=soup.find('h1').get_text(strip=True)

        #category
        breadcrumb = soup.find('ul', class_='breadcrumb')
        category = breadcrumb.find_all('a')[2].get_text(strip=True)
        

        #price
        priceText=soup.find('p',class_='price_color').get_text()
        price=float(priceText.replace("£", ""))

        #availability
        availability_text = soup.find("p", class_="availability").get_text(strip=True)
        availability = "In stock" if "In stock" in availability_text else "Out of stock"

        #rating
        rating=soup.find('p',class_='star-rating')['class'][1]
        rating=ratingMap[rating]

        #image url
        imgRel=soup.find('div',class_='item active').find('img')['src']
        img=urljoin(booksUrl,imgRel)

        parse_end = time.perf_counter()
        parsing_time = parse_end - parse_start

        total_time = request_time + parsing_time

        return {
            "title":title,
            "category":category,
            "price":price,
            "availability":availability,
            "rating":rating,
            "product_url":booksUrl,
            "img":img,
            "request_time": request_time,
            "parsing_time": parsing_time,
            "total_time": total_time
        }
    except Exception as e:
        print(f"Failed to scrape {booksUrl}: {e}")
        return None


def run_scraper(save_json=True, json_path="books.json"):
    all_books = []

    overall_start = time.perf_counter()

    categories = getCategories()
    categories_df = pd.DataFrame(categories)
    categories_df.index += 1

    for _, row in categories_df.iterrows():
        category_url = row["url"]

        book_urls = getAllBooksUrl(category_url)

        for book_url in book_urls:
            book_data = bookDetails(book_url)
            if book_data:
                all_books.append(book_data)

    overall_end = time.perf_counter()

    total_books = len(all_books)
    total_runtime = overall_end - overall_start
    average_time_per_book = (
        sum(book["total_time"] for book in all_books) / total_books
        if total_books else 0
    )

    print(f"Total books scraped: {total_books}")
    print(f"Average time per book: {average_time_per_book:.4f} seconds")
    print(f"Total runtime: {total_runtime:.4f} seconds")

    books_df = pd.DataFrame(all_books)
    books_df.index += 1
    books_df.drop_duplicates(subset="product_url", inplace=True)

    print(books_df.head())

    if save_json:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(all_books, f, ensure_ascii=False, indent=2)

    return all_books


if __name__ == "__main__":
    run_scraper()