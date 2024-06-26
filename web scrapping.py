import requests
from bs4 import BeautifulSoup
import csv
import time

# Define the base URL
base_url = "http://quotes.toscrape.com/"

# Function to scrape a single page
def scrape_page(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Function to parse the quotes from the page
def parse_quotes(soup):
    quotes = soup.find_all('div', class_='quote')
    scraped_data = []
    for quote in quotes:
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
        scraped_data.append({
            'text': text,
            'author': author,
            'tags': tags
        })
    return scraped_data

# Function to save data to a CSV file
def save_to_csv(data, filename='quotes.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['text', 'author', 'tags']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow({
                'text': row['text'],
                'author': row['author'],
                'tags': ', '.join(row['tags'])
            })

# Main function to handle pagination and overall scraping
def main():
    all_data = []
    page_number = 1
    while True:
        print(f"Scraping page {page_number}...")
        url = f"{base_url}page/{page_number}/"
        soup = scrape_page(url)
        if soup is None:
            break
        page_data = parse_quotes(soup)
        if not page_data:
            break
        all_data.extend(page_data)
        next_button = soup.find('li', class_='next')
        if not next_button:
            break
        page_number += 1
        time.sleep(1)  # Be polite and wait a second between requests

    save_to_csv(all_data)
    print("Scraping complete. Data saved to quotes.csv.")

# Run the main function
if __name__ == "__main__":
    main()
