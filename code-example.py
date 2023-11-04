# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

#importing necessary packages
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

#getting the response from the source
url = 'https://www.imdb.com/search/keyword/?keywords=anime&sort=moviemeter,asc&mode=detail&page=1&ref_=kw_nxt'
response = requests.get(url)
soup = BeautifulSoup(response.content,'html.parser')

#create empty lists
Title = []
release_year = []
genre = []
duration = []
rating = []
desc = []
votes = []

# Get the data content
anime_data = soup.findAll('div',attrs = {'class':'lister-item mode-detail'})

#The scraping of data 
final = pd.DataFrame()
for j in range(1,21):
  url = 'https://www.imdb.com/search/keyword/?keywords=anime&sort=moviemeter,asc&mode=detail&page={}&ref_=kw_nxt'.format(j)
  response = requests.get(url)
  soup = BeautifulSoup(response.content,'html.parser')

  anime_data = soup.findAll('div',attrs = {'class':'lister-item mode-detail'})

  for o in anime_data:

    #name = o.h3.a.text
    #Title.append(name)
    try:
      name = o.h3.a.text
      Title.append(name)
    except AttributeError:
      Title.append('NA')

    #OA means on air and the anime is still going on

    #yor = o.h3.find('span',class_='lister-item-year text-muted unbold').text.replace('(','').replace(')','').replace(' ','OA')
    #release_year.append(yor)
    try:
      yor = o.h3.find('span',class_='lister-item-year text-muted unbold').text.replace('(','').replace(')','').replace(' ','OA')
      release_year.append(yor)
    except AttributeError:
      release_year.append('NA')

    #type_anime = o.p.find('span',class_='genre').text.replace('\n','').replace(' ','')
    #genre.append(type_anime)
    try:
      type_anime = o.p.find('span',class_='genre').text.replace('\n','').replace(' ','')
      genre.append(type_anime)
    except AttributeError:
      genre.append('NA')

    #runtime = o.p.find('span',class_='runtime')
    #if o.p.find('span',class_='runtime'):
    #    duration.append(runtime.text.replace(' min',''))
    #else:
        #duration.append('**')
    try:
      runtime = o.p.find('span',class_='runtime')
      if o.p.find('span',class_='runtime'):
        duration.append(runtime.text.replace(' min',''))
      else:
        duration.append('NA')
    except AttributeError:
      duration.append('NA')


    #rate = o.find('div',attrs = {'class':'inline-block ratings-imdb-rating'})
    #rating.append(rate.text.replace('\n',''))
    try:
      rate = o.find('div',attrs = {'class':'inline-block ratings-imdb-rating'})
      rating.append(rate.text.replace('\n',''))
    except AttributeError:
      rating.append('NA')

    #summary = o.find('p',class_='').text.replace('\n','')
    #desc.append(summary)
    try:
      summary = o.find('p',class_='').text.replace('\n','')
      desc.append(summary)
    except AttributeError:
      desc.append('NA')

    #nv = o.find('span',attrs = {'name':'nv'})
    #votes.append(nv.text)
    try:
        nv = o.find('span',attrs = {'name':'nv'})
        votes.append(nv.text)
    except AttributeError:
        votes.append('NA')


anime_DF = pd.DataFrame({
    'Anime Title' : Title,
    'Release Year': release_year,
    'Genre': genre,
    'Duration': duration,
    'Rating': rating,
    'Description': desc,
    'No. of Votes': votes
})

final = pd.concat([final,anime_DF])

