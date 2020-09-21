#!/usr/bin/env python
# coding: utf-8

# # Mars

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[ ]:


# Path to chromedriver
#!which chromedriver


# In[2]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=True)


# ### Visit the NASA Mars News Site

# In[ ]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[ ]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[ ]:


slide_elem.find("div", class_='content_title')


# In[ ]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[ ]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[ ]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[ ]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[ ]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[ ]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[ ]:


# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# ### Mars Facts

# In[ ]:


# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# In[ ]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# ### Mars Weather

# In[ ]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[ ]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[ ]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1 Scrape High-Resolution Mars' Hemisphere Images and Titles

# ### Hemispheres

# In[20]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemi_soup = soup(html, 'html.parser')

hemi_titles = hemi_soup.find_all('h3')
for title in hemi_titles:

    #hemi_soup = soup(html, 'html.parser')
    #print(title.text)
    
    # Find title and click link to image
    hemi_image_elem = browser.links.find_by_partial_text(title.text)
    hemi_image_elem.click()

    
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    
    # Find the relative image url
    hemi_url_rel = hemi_soup.find('img', class_='wide-image').get('src')
    hemi_url_full = f'https://astrogeology.usgs.gov/{hemi_url_rel}'
    
    # Create dictionary
    hemis = {'img_url':hemi_url_full, 'title':title.text}

    # Add dictionary to list
    hemisphere_image_urls.append(hemis)
    
    # Back to search page
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()




