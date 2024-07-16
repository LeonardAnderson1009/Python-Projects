import requests

def main():
    print("Webscraper!")
    url1 = "https://" + input("Choose a website: ") + "/"
    searchwhat = input("What you want to search for: ")

    response = requests.get(url1)
    content1 = response.content

    count = content1.count(searchwhat.encode())

    print(f"Word: {searchwhat} and Count: {count}")

if __name__ == "__main__":
    main()
