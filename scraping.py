# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager



def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()

    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

###BELOW THE MARS FACTS CODE A SECTION FOR IMG RETRIEVAL
#Challenge scrape find the hemistphere images for del 1 using scraping techniques 
def hemispher(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    hemisphere_image_urls = []

    imgs_links= browser.find_by_css("a.product-item h3")

    for x in range(len(imgs_links)):
        hemisphere={}

        # Find elements going to click link 
        browser.find_by_css("a.product-item h3")[x].click()

        # Find sample Image link
        sample_img= browser.find_link_by_text("Sample").first
        hemisphere['img_url']=sample_img['href']

        # Get hemisphere Title
        hemisphere['title']=browser.find_by_css("h2.title").text

        #Add Objects to hemisphere_img_urls list
        hemisphere_image_urls.append(hemisphere)

        # Go Back
        browser.back()
    return hemisphere_image_urls

if __name__== "__main__":
    # If running as script, print scrapped data
    print(scrape_all())


    from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

class ScraperHelper:
    def __init__(self):
        pass

    def init_browser(self):
        # @NOTE: Replace the path with your actual path to the chromedriver
        executable_path = {'executable_path': ChromeDriverManager().install()}
        return Browser("chrome", **executable_path, headless=False)


    def scrape_info(self):
        browser = self.init_browser()

        # Scrape NASA News
        url = 'https://redplanetscience.com/'
        browser.visit(url)

        # Optional delay for loading the page
        browser.is_element_present_by_css('div.list_text', wait_time=1)

        # Scrape page into Soup
        html = browser.html
        news_soup = bs(html, 'html.parser')

        slide_elem = news_soup.select_one('div.list_text')
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

        # Get Featured IMAGE
        url = 'https://spaceimages-mars.com'
        browser.visit(url)
        time.sleep(1)

        full_image_elem = browser.find_by_tag('button')[1]
        full_image_elem.click()
        html = browser.html
        img_soup = bs(html, 'html.parser')
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        featured_img_url = f'https://spaceimages-mars.com/{img_url_rel}'

        # Mars Facts
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        df.columns=['Description', 'Mars', 'Earth']
        df.set_index('Description', inplace=True)
        table_html = df.to_html()

        # Hemispheres
        url = 'https://marshemispheres.com/'
        browser.visit(url)
        time.sleep(1)

        html = browser.html
        soup = bs(html, 'html.parser')  
        items = soup.find("div", {"class":"results"}).find_all("div", {"class", "item"})
        
        # init return 
        hemisphere_image_urls = []

        # for each hemi on the main page
        for item in items:
            # grab the link out of it
            link = item.find("a", {"class": "itemLink"})["href"]
            full_url = url + link
            
            # visit the link
            browser.visit(full_url)
            time.sleep(1)
            
            # soupify
            html = browser.html
            soup = bs(html, 'html.parser')
            
            # grab the data we want
            img = soup.find("img", {"class", "wide-image"})["src"]
            img_url = url + img
            
            title = soup.find("h2", {"class": "title"}).text
            title = title.split("Enhanced")[0].strip()
            
            data = {"img_url" : img_url, "title":title}
            
            hemisphere_image_urls.append(data)

        # Store data in a dictionary
        mars_data = {
            "news_title": news_title,
            "news_paragraph": news_p,
            "featured_image": featured_img_url,
            "facts": table_html,
            "hemispheres": hemisphere_image_urls
        }

        # Quite the browser after scraping
        browser.quit()

        # Return results
        return mars_data