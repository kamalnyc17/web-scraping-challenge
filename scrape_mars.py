# importing dependancies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urlparse


def init_browser():
    # Splinter setup
    executable_path = {'executable_path': '/data/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_dict = {}

    # NASA Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    # extracting latest News Title and Paragraph Text
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find_all('div', class_='content_title')[1].text
    news_body = soup.find_all('div', class_='article_teaser_body')[1].text
    mars_dict["news_title"] = news_title
    mars_dict["news_body"] = news_body

    # Extracting JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # extracting featured image
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_section = soup.find(
        'section', class_="primary_media_feature").article['style']
    image_url = 'https://www.jpl.nasa.gov' + featured_image_section[23:75]
    mars_dict["full_image_url"] = image_url

    # Mars Facts
    u = urlparse("https://space-facts.com/mars")
    url = u.geturl()
    print(url)
    mars_table = pd.read_html(url)
    df = mars_table[0]
    df.columns = ['Matrix Type', 'Information']
    # converting to dict
    data_dict = df.to_dict()
    mars_dict["mars_facts"] = data_dict

    # Mars Hemispheres
    mars_dict["hemisphere_image_urls"] = [
        {"title": "Cerberus Hemisphere",
            "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere",
            "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere",
            "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
        {"title": "Valles Marineris Hemisphere",
            "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
    ]
    # return mars dictionary to the route
    return mars_dict
