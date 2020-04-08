#!/usr/bin/env python
import sys
import discogs_client
from discogs_client.exceptions import HTTPError
from time import sleep
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

consumer_key = 'nHfIQQZKYMFtKAuNZQfg'
consumer_secret = 'HVAQrcOTsQzWHBnHuEyxmOplrftuZcHW'
user_agent = 'discogs_api_example/2.0'

# auth with the app (key, secret)
discogsclient = discogs_client.Client(user_agent)
discogsclient.set_consumer_key(consumer_key, consumer_secret)
token, secret, url = discogsclient.get_authorize_url()
print(f"Request the following url : {url} \nThen write down the code below")
oauth_verifier = input("code: ")

# auth with the user access token
try:
    access_token, access_secret = discogsclient.get_access_token(oauth_verifier)
except HTTPError:
    print('Unable to authenticate.')
    sys.exit(1)
user = discogsclient.identity()

# Get the user collection
collection = user.collection_folders[0].releases
len_collection = collection.count
colonnes = ['index','genres', 'country', 'formats', 'year','styles', 'artists', 'labels', 'tracklist']

# Create the collection "dataframe"
df = []
pbar = tqdm(range(len_collection))
pbar.set_description("Collection loading")
for index in pbar:
    sleep(1)
    release = collection.__getitem__(index=index).release
    row = [index, 
           release.genres,  release.country, release.formats, release.year,
          release.styles,
          [artist.name for artist in release.artists],
          [label.name for label in release.labels],
          [track.title for track in release.tracklist]]
    df.append(row)

# Graphes
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(13, 13))

# Create graph for countries
countries = pd.DataFrame(np.take(np.array(df),indices=colonnes.index("country"),axis=1),columns=["country"])
countries.groupby("country").size().plot(kind='pie',ax=axes[0,0])

# Five top label graph
labels = [row[colonnes.index("labels")] for row in df]
labels = pd.DataFrame([item for sublist in labels for item in sublist], columns=["label"])
top_labels = labels.groupby('label').size().sort_values(ascending = False)
top_labels = top_labels[:5]
top_labels.plot(kind='bar',ax=axes[1,0])

# Years
years = pd.DataFrame(np.take(np.array(df),indices=colonnes.index("year"),axis=1),columns=["year"])
plot_year = years.groupby("year").size().plot(kind='bar',ax=axes[0,1])

# Styles
styles = [row[colonnes.index("styles")] for row in df]
styles = pd.DataFrame([item for sublist in styles for item in sublist], columns=["style"])
top_styles = styles.groupby('style').size().sort_values(ascending = False)
top_styles = top_styles[:10]
top_styles.plot(kind='bar',ax=axes[1,1])

axes[1,1].set_xlabel('')
axes[1,0].set_xlabel('')
plt.savefig("results.png")
plt.show()
