#%%
# Dependencies
import pandas as pd
from pprint import pprint
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import requests
import tweepy
from tweepy import OAuthHandler


#%%
get_ipython().system('which chromedriver')


#%%
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


#%%
mars_url = 'https://mars.nasa.gov/news'
browser.visit(mars_url)


#%%
# HTML object
html = browser.html

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

# Use Beautiful Soup's find() method to navigate and retrieve attributes
h3 = soup.find('h3')
news_title = h3.text
print(news_title)

newsfeed = soup.find('div', class_='rollover_description_inner')
news_p = newsfeed.text.strip()
print(news_p)


#%%
jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(jpl_url)


#%%
# HTML object
html = browser.html

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

# Use Beautiful Soup's find() method to navigate and retrieve attributes
item = soup.find('a', class_='button fancybox')
base_url = 'https://www.jpl.nasa.gov'
featured_img_url = base_url + item['data-fancybox-href']
print(featured_img_url)


#%%
consumer_key = 'NCgxx81KmAg3x7grbgXQ28mUF'
consumer_secret = 'hKYSlIloSnaxvTH2eyfQYK4JCc1ngGre0CIsBosUKvCrjXQOnW'
access_token = '1524954282-eogZthzXepkLq2IQLBUIO04uujavVRlg4VANP4b'
access_secret = 'sp24Dl1dfQNulOkJCL54hNm5uwD2Mr45WTSiVwQELYGFc'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

MarsWxReport = api.user_timeline(screen_name = 'MarsWxReport', count = 1)
for status in MarsWxReport:
    mars_weather = status.text.strip()
pprint(mars_weather)


#%%
# Scrape table contents using Pandas
mars_facts_url = 'https://space-facts.com/mars/'
tables = pd.read_html(mars_facts_url)

# Convert table/list to dataframe using Pandas
# Transpose results
mars_facts_df = tables[0]
mars_facts_df.columns = ["Column Name", "Value"]
mars_facts_df = mars_facts_df.set_index("Column Name").T

# Convert dataframe into html table
mars_facts_html = mars_facts_df.to_html(index = False)

# Strip unwanted newlines from html table
mars_facts_html = mars_facts_html.replace('\n', '')

# Print the html table
pprint(mars_facts_html)


#%%
astrogeo_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(astrogeo_url)


#%%
# HTML object
html = browser.html

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

# Create base url
astro_base_url = 'https://astrogeology.usgs.gov'

# Create an empty array for hemisphere image urls
hemisphere_img_urls = []

# Find the html class/section to loop through for each image url
hemisphere_list = soup.find('div', class_='collapsible results')
hemisphere = hemisphere_list.find_all('div', class_='description')

# Loop through and scrape the image url and title to append to the hemisphere_img_urls array
for item in hemisphere:
    h3 = item.find('h3')
    title = h3.text.strip()
    partial_link = item.find('a')['href']
    full_link = astro_base_url + partial_link
    browser.visit(full_link)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_downloads = soup.find('div', class_='downloads')
    full_img = img_downloads.find('a')['href']
    hemisphere_img_urls.append({"title" : title, "urls": full_img})

# Print the array
pprint(hemisphere_img_urls)

######################################################################

from flask import Flask, jsonify

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date():
    start_temp = []
    
    for TMin, TAvg, TMax in calc_temps:
        start_temp_dict = {}
        start_temp_dict["Minimum Temperature"] = TMin
        start_temp_dict["Average Temperature"] = TAvg
        start_temp_dict["Maximum Temperature"] = TMax
        start_temp.append(start_temp_dict)
        
    return jsonify(start_end_date)

if __name__ == "__main__":
    app.run(debug=True)
