#importing request module
import requests
#importing beautiful soup module
from bs4 import BeautifulSoup
#import json module
import json
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

url = "https://www.wsj.com/articles/meta-employees-security-guards-fired-for-hijacking-user-accounts"

#requesting the url
r = requests.get(url).text
#parsing the html
soup = BeautifulSoup(r, 'html.parser')

print(soup.title.text)

os.chdir(folder)
filename  = re.sub(r'\W+', '', f"{soup.title.text}.txt")
