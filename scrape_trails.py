import requests
from bs4 import BeautifulSoup


def scrape_alltrails(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    souped_txt = BeautifulSoup(response.content, 'html.parser')
    print(f"souped_txt: {souped_txt}")
    # Find all trail cards
    trail_cards = souped_txt.find('div',
                                  class_='styles-module__results___ZXJFU')
    print(f"soup: {trail_cards}")
    new_trail_cards = souped_txt.find_all('div')
    print(new_trail_cards)

    # Loop through each trail card and extract information
    for card in trail_cards:
        # Extract trail name
        trail_name = card.find('h3').text.strip()

        # Extract trail length
        trail_length = card.find('span', class_='xlate-none').text.strip()

        # Extract trail rating
        trail_rating = card.find(
            'span', class_='MuiRating-root')['aria-label'].split(' ')[1]

        # Print trail information
        print(f"Trail Name: {trail_name}")
        print(f"Trail Length: {trail_length}")
        print(f"Trail Rating: {trail_rating}")
        print()

    else:
        print("Failed to retrieve page")


# URL of the page to scrape
url = "https://www.alltrails.com/us/new-hampshire"
scrape_alltrails(url)
