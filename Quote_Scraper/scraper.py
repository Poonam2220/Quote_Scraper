import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape quotes from a single page
def scrape_quotes(page_url):
    try:
        response = requests.get(page_url)
        response.raise_for_status()  # Raise an error for bad responses
        quotes = []
        soup = BeautifulSoup(response.text, 'html.parser')
        for quote in soup.find_all('div', class_='quote'):
            text = quote.find('span', class_='text').get_text()
            author = quote.find('small', class_='author').get_text()
            quotes.append({'Quote': text, 'Author': author})
        return quotes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {page_url}: {e}")
        return []

# Main scraping function
def main():
    base_url = 'http://quotes.toscrape.com/page/'
    all_quotes = []
    page = 1

    while True:
        page_url = f"{base_url}{page}/"
        quotes = scrape_quotes(page_url)
        if not quotes:
            break  # Exit loop if no quotes are found
        all_quotes.extend(quotes)
        page += 1

    # Save to CSV
    df = pd.DataFrame(all_quotes)
    df.to_csv('quotes.csv', index=False)
    print("All quotes have been saved to quotes.csv")

if __name__ == "__main__":
    main()