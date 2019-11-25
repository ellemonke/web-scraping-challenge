from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)


# NASA Mars News
def mars_news():
    # URL to scrape
    news_url = 'https://mars.nasa.gov/news/'
    response = requests.get(news_url)
    news_soup = bs(response.text, 'lxml')

    # Scrape results
    news_title = news_soup.find('div', class_='content_title').find('a').text
    news_p = news_soup.find('div', class_='rollover_description_inner').text.strip()

    return news_title, news_p


# JPL Mars Featured Space Image
def mars_image():
    # URL to scrape
    mars_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response = requests.get(mars_url)
    mars_soup = bs(response.text, 'html.parser')

    # Scrape results
    image_url = mars_soup.find('div', class_='carousel_container')\
        .find('div', class_='carousel_items').article['style']

    # Parse out first part of string
    image_url = image_url.split("('")   
    image_url = image_url[1]
    # Parse out last part of string
    image_url = image_url.strip("');")  
    # Add url parts together 
    base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = base_url + image_url

    return featured_image_url


# Mars Weather
def mars_weather():
    # URL to scrape
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(twitter_url)
    twitter_soup = bs(response.text, 'html.parser')

    # Scrape results
    mars_weather = twitter_soup.find('p', class_ = 'js-tweet-text').text

    # Remove Twitter pic url
    mars_weather = mars_weather.split('pic.twitter.com')
    mars_weather = mars_weather[0]

    return mars_weather


# Mars Facts
def mars_facts():
    # URL to scrape
    facts_url = 'https://space-facts.com/mars/'
    response = requests.get(facts_url)
    facts_soup = bs(response.text, 'html.parser')

    # Scrape results
    facts_table = facts_soup.find('table', id = 'tablepress-p-mars-no-2')

    # Convert element tag to string
    tmp_table = str(facts_table)
    # Convert string to list
    facts_list = pd.read_html(tmp_table)
    # Slice list to df
    facts_df = facts_list[0]
    facts_df.columns=['','value']
    # Convert df to html string
    mars_facts = facts_df.to_html(index=False, border=None)
    mars_facts = mars_facts.replace('\n', '')

    return mars_facts


# Mars Hemispheres
def mars_hemispheres():
    browser = init_browser()

    # URL to scrape
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html = browser.html
    hemi_soup = bs(html, 'html.parser')
    # Scrape results
    results = hemi_soup.find_all('div', class_ = 'item')

    base_url = 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/'
    hemisphere_image_urls = []

    # Loop through results
    for result in results:
        # Find full-size img
        img_thumb = result.find('a', class_ = 'product-item').find('img', class_ = 'thumb')
        img_str = str(img_thumb)                        # convert each element tag to string
        img_split = img_str.split('_', 1)               # drop first part of string
        img_tif = img_split[1].split('_thumb.png"/>')   # drop last part of string
        img_url = base_url + img_tif[0] + '/full.jpg'   # add img location to base_url

        # Find title
        title = result.find('div', class_ = 'description')\
            .find('a', class_ = 'product-item').find('h3').text
        
        # Create dict and add to list of dicts
        hemi_dict = {'title': title, 'img_url': img_url}
        hemisphere_image_urls.append(hemi_dict)

    return hemisphere_image_urls


# Scrape function
def scrape():
    
    # Create empty dict
    mars_info = {}

    # Unpack results from mars_news()
    (news_title, news_p) = mars_news()
    # Fill in dict with results from other functions
    mars_info["news_title"] = news_title
    mars_info["news_p"] = news_p
    mars_info["featured_image_url"] = mars_image()
    mars_info["mars_weather"] = mars_weather()
    mars_info["mars_facts"] = mars_facts()
    mars_info["hemisphere_image_urls"] = mars_hemispheres()

    return mars_info


if __name__ == "__main__":
    print(scrape())
