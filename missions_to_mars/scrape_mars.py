# Dependencies and Setup
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import datetime as dt

# Set Executable Path & Initialize Chrome Browser
executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path)

# NASA Mars News Site Web Scraper
def mars_news(browser):
    # Visit the NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    #using BeautifulSoup to write it into html
    html = browser.html
    soup = bs(html,"html.parser")

    try:
        news_title = soup.find("div",class_="content_title").text
        news_paragraph = soup.find("div", class_="article_teaser_body").text
    except AttributeError:
        return None, None
    
    return news_title, news_paragraph


# NASA JPL Site Web Scraper
def featured_image(browser):
    # Visit the NASA JPL (Jet Propulsion Laboratory) Site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url) 
    
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    # Find "More Info" Button and Click It
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    new_html = browser.html
    new_soup = bs(new_html, 'html.parser')
    temp_img_url = new_soup.select_one("figure.lede a img")
    
    try:
        back_half_img_url = temp_img_url.get('src')
    except AttributeError:
        return None 
   # Use Base URL to Create Absolute URL
    recent_mars_image_url = f"https://www.jpl.nasa.gov{back_half_img_url}"
    return recent_mars_image_url

# Mars Weather Twitter Account Web Scraper
def twitter_weather(browser):
    # Visit the Mars Weather Twitter Account
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)

    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    
    return mars_weather

# Mars Facts Web Scraper
def mars_facts():
       
    try:
        mars_space_table_read = pd.read_html("https://space-facts.com/mars/")
        df_mars_facts = mars_space_table_read[0]
    except BaseException:
        return None
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index("Parameter")
    df_mars_facts.reset_index()
    return df_mars_facts.to_html(classes="table table-hover table-striped")


# Mars Hemispheres Web Scraper
def hemisphere(browser):
    # Visit the USGS Astrogeology Science Center Site
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)

    hemisphere_image_urls = []

    # Get a List of All the Hemisphere
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        browser.find_by_css("a.product-item h3")[item].click()
        
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate Backwards
        browser.back()
    return hemisphere_image_urls


# Call web scraping 
def scrape_all():
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path)

    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    mars_weather = twitter_weather(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
   
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "weather": mars_weather,
        "facts": facts,
        "hemispheres": hemisphere_image_urls 
        }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())