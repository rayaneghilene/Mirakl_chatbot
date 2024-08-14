from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import argparse
import requests
import json
import time
import sys


def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_links(soup, base_url):
    links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Handle relative URLs
        if not href.startswith('http'):
            href = base_url + href
        links.append({'text': a_tag.get_text(strip=True), 'href': href})
    return links


def extract_data(soup):
    data = {
        'title': soup.title.string if soup.title else 'No title',
        'headings': [{f"h{i}": [h.get_text(strip=True) for h in soup.find_all(f"h{i}")]} for i in range(1, 7)],
        'paragraphs': [p.get_text(strip=True) for p in soup.find_all('p')],
    }
    return data


def scrape_website(base_url):
    main_soup = fetch_url(base_url)
    if main_soup is None:
        return {}

    all_links = extract_links(main_soup, base_url)
    website_data = {}

    for link in all_links:
        link_url = link['href']
        link_text = link['text']

        print(f"Scraping {link_text}: {link_url}")
        link_soup = fetch_url(link_url)
        if link_soup:
            page_data = extract_data(link_soup)
            website_data[link_text] = {
                'url': link_url,
                'content': page_data
            }
            time.sleep(1)

    return website_data


def save_to_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(f"Data saved to {file_path}")


def main():
    parser = argparse.ArgumentParser(description='Scrape a website and save the data to a JSON file.')
    parser.add_argument('--base_url', type=str, default='https://www.mirakl.com/',
                        help='The base URL of the website to scrape (default: https://www.mirakl.com/).')
    parser.add_argument('--output_file', type=str, default='scraped_data.json',
                        help='The file path to save the scraped data in JSON format (default: scraped_data.json).')

    args = parser.parse_args()

    data = scrape_website(args.base_url)
    save_to_json(data, args.output_file)


if __name__ == "__main__":
    main()