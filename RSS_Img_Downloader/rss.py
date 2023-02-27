import os
import sys
import requests
import feedparser
from bs4 import BeautifulSoup

# get the RSS feed URL and the path to save the images from command-line arguments
if len(sys.argv) < 3:
    print('Usage: python download_images.py <rss_url> <save_path>')
    sys.exit(1)
rss_url = sys.argv[1]
save_dir = sys.argv[2]

# create the directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

# download the RSS feed and parse it
feed = feedparser.parse(rss_url)

# loop through each entry in the feed
for entry in feed.entries:
    # get the HTML content of the entry's summary or content
    html_content = entry.summary or entry.content[0].value

    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # find all img tags in the HTML content
    img_tags = soup.find_all('img')

    # loop through each img tag and download its src attribute value
    for img_tag in img_tags:
        img_url = img_tag['src']
        img_filename = os.path.join(save_dir, os.path.basename(img_url))
        response = requests.get(img_url)
        with open(img_filename, 'wb') as f:
            f.write(response.content)
        print(f'Downloaded {img_filename}')
