import argparse
import requests
from urllib.parse import urlparse

def main(url, searchwhat):
    print("Webscraper!")

    # Check if the URL scheme is missing and add 'https://' if necessary
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = 'https://' + url

    response = requests.get(url)
    content1 = response.content

    count = content1.count(searchwhat.encode())

    print(f"Word: {searchwhat} and Count: {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Web scraper with search term counting')
    parser.add_argument('url', type=str, help='URL of the website to scrape')
    parser.add_argument('searchwhat', type=str, help='Word or phrase to search for')

    args = parser.parse_args()

    main(args.url, args.searchwhat)