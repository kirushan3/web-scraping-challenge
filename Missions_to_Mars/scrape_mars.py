from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from pprint import pprint


def scrape_all():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_p = mars_news(browser)

    #Run all scraping functions created
    main_data = {
        "news_tile": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image(browser),
        "Mars_weather": Mars_weather(browser),
        "Mars_facts": Mars_facts(),
        "Mars_hemispheres": Mars_hemispheres(browser)
    }



def mars_news(browser):
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    #delay for the url
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time = 1)
    # set up parser
    html = browser.html
    news_soup = bs(html, 'html.parser')

    try:
    #finding the elements
        side_elem = news_soup.select_one('ul.item_list li.slide')
        side_elem.find("div", class_='content_title')       
    #finding the title
        news_title = side_elem.find("div", class_='content_title').get_text()
   
    #finding the paragraph
        news_p= side_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p

def featured_image(browser):
    #finding mars image
    #url retrieval
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)
    #parsering featured image url
    #url parsel
    main_image_html = browser.html
    main_image_soup = bs(main_image_html, 'html.parser')
    #retrieve image
    #https://stackoverflow.com/questions/24981963/extracting-url-from-style-background-url-with-beautifulsoup-and-without-regex

    get_main_image = main_image_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    core_url = 'https://www.jpl.nasa.gov'

    #Concatenate featured image url
    featured_image_url = core_url + get_main_image
    
    return featured_image_url

def Mars_weather(browser):
    mars_weather = "InSight sol 607 (2020-08-11) low -93.1ºC (-135.6ºF) high -18.9ºC (-2.1ºF) winds from the WNW at 8.2 m/s (18.4 mph) gusting to 21.4 m/s (47.8 mph) pressure at 7.90 hPa"

    return mars_weather

def Mars_facts():
    mars_facts_url = "https://space-facts.com/mars/"
    #mars data extracted thru read html
    mars_data = pd.read_html(mars_facts_url)
    mars_data
    #mars data table
    mars_data_table = mars_data[0]
    mars_data_table
    #mars data table with column headers
    mars_data_table.columns = ['Description', 'Values']
    
    return mars_data_table.to_html(classes = "table table-striped")

def Mars_hemispheres(browser):
    #open browser
    mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemi_url)
    #soup text
    response_hemi = requests.get(mars_hemi_url)
    soup_hemi = bs(response_hemi.text, 'html.parser')
    #looping thru soup script
    mars_links = []
    for i in soup_hemi.find_all('a'):
        mars_links.append(i.get('href'))
    #arranging links
    astro_url = 'https://astrogeology.usgs.gov'
    link_1 = astro_url+mars_links[4]
    link_2 = astro_url+mars_links[5]
    link_3 = astro_url+mars_links[6]
    link_4 = astro_url+mars_links[7]
    #parsing images
    browser_hemi.visit(link_1)
    response_1 = requests.get(link_1)
    soup_1 = bs(response_1.text, 'html.parser')
    title_1 = soup_1.h2.text
    link_image_1 = soup_1.li.a['href']
    browser_hemi.back()

    browser_hemi.visit(link_2)
    response_2 = requests.get(link_2)
    soup_2 = bs(response_2.text, 'html.parser')
    title_2 = soup_2.h2.text
    link_image_2 = soup_2.li.a['href']
    browser_hemi.back()

    browser_hemi.visit(link_3)
    response_3 = requests.get(link_3)
    soup_3 = bs(response_3.text, 'html.parser')
    title_3 = soup_3.h2.text
    link_image_3 = soup_3.li.a['href']
    browser_hemi.back()

    browser_hemi.visit(link_4)
    response_4 = requests.get(link_4)
    soup_4 = bs(response_4.text, 'html.parser')
    title_4 = soup_4.h2.text
    link_image_4 = soup_4.li.a['href']
    browser_hemi.quit()
    #image link dictionary
    hemis_image_urls_dict = [{"title":title_1, "img_url": link_image_1},
                        {"title":title_2, "img_url": link_image_2},
                        {"title":title_3, "img_url": link_image_3},
                        {"title":title_4, "img_url": link_image_4}]
    
    return hemis_image_urls_dict

if __name__ == "__main__":
    print(scrape_all())    