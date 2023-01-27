from bs4 import BeautifulSoup
import requests
import os
import re


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_folders(folder="text"):
    cwd = os.getcwd()
    source_path = os.path.join(cwd,folder)
    create_dir(source_path)
    training_path = os.path.join(source_path)
    return training_path

folder = create_folders()

"""
anytime=
1day = 1d
1week = 1w
1month = 1m
"""

keyword = input("Enter the search term: ")
def daterange ():
    date = input("date range: 1d , 1w , 1m  : ")
    if date == "1d":
        return date
    if date == "1w":
        return date
    if date == "1m":
        return date
    else:
        print("invalid input")
        daterange()


keyword = keyword
date = daterange()

news_data = []

os.chdir(folder)

for page in (0,21,41,61,81):
    url = 'https://news.search.yahoo.com/search?p={}&b={}&ei=UTF-8&fr2=time&age={}&btf=m'.format(keyword,page,date)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for article in soup.find_all('div', {'class': 'NewsArticle'}):
        news_title = article.find('h4').text
        news_source = article.find('span','s-source').text
        news_description = article.find('p','s-desc').text
        news_link = article.find('a').get('href')
        news_time = article.find('span', class_='fc-2nd').text
        # perform basic clean text
        news_time = news_time.replace('.','').strip()
        news_title = news_title.replace('.','').strip()
        filename  = re.sub(r'\W+', '', f"{news_title}.txt")
        with open(filename, 'w') as f:	
            sum = news_description
            f.writelines(sum)
        news_data.append([news_title, news_source, news_description, news_link, news_time]) 

import pandas as pd
df = pd.DataFrame(news_data, columns=['Title', 'Source', 'Description', 'Link', 'Time'])

print(df.head())