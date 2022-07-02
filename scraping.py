

#Import splinter and beautiful soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt





def scrape_all():

    #set up executable path and url to do scraping
    #prepping automatic browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True) #use headless=False when testing to see scraping in action

    #tells Python that we'll be using our mars_news function to pull this data.
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph, ######CHANGE TO news_p???????????????????????????????
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    #ending automated browsing session
    #otherwise it will continue to look for instructions and use up computer battery and memory
    browser.quit()
    return data






# ## article scraping

def mars_news(browser):

    # Visit the mars nasa news site
    url="https://redplanetscience.com"
    browser.visit(url)

    # we're searching for elements with a specific combination of tag (div) and attribute (list_text)
    # Optional delay for loading the page (The optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.)
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    #set up html parser and make browser html a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #add try/except for error handling:
    try:
        #get a bunch of the code from website stored here so we can find stuff in it
        slide_elem = news_soup.select_one('div.list_text')

        #news title
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text() #just .text also works

        #article summary
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').text

    except AttributeError:
        return None, None

    return news_title, news_paragraph





# ## Image Scraping

def featured_image(browser):

    #visit url
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    #find and click on full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #parse the resulting html with soup
    html=browser.html
    img_soup = soup(html, "html.parser")

    #add error handling in case web page's format changes and code doesn't work anymore
    #if this part fails, other things can still be scraped because of the try/except block
    try:
        #.get pulls the link to image
        img_url_rel = img_soup.find("img", class_="fancybox-image").get("src")

    except AttributeError:
        return None

    #add the rest of the url to the image url
    img_url = f"{url}{img_url_rel}"

    return img_url






# ## Collection of mars facts

def mars_facts():

    #add try/except for error handling:
    try:
        #instead of scraping each row of the table, scrape entire table with Pandas' .read_html() function

        #The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. 
        #By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. 
        df=pd.read_html("https://galaxyfacts-mars.com/")[0]

    #base exception is raised when any of the built-in exceptions are encountered and it won't handle any user-defined exceptions. Because data is returned differently and can have errors other than attribute errors
    except BaseException:
        return None
        
    df.columns=["description", "Mars", "Earth"]
    df.set_index('description', inplace=True)

    #Our data is live—if the table is updated, then we want that change to appear in Robin's app also.
    #Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html() function
    return df.to_html(classes="table table-striped") #code added in the argument at end






#tells Flask that our script is complete and ready for action. 
# The print statement will print out the results of our scraping to our terminal after executing the code
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

