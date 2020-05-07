import os
import sys
import discogs_client
from discogs_client.exceptions import HTTPError
from time import sleep
from tqdm import tqdm
import numpy as np

consumer_key = 'LPCdkfqipSxdKywYLhmk'
consumer_secret = 'qQhzfPebKLCDrzImGWzXGzAGHQjTBKba'
user_agent = 'discogs_api_example/2.0'

def discogs_init_(self,email=None,token=None, secret=None):
	if email:
		self.email = email

	self.discogsclient = discogs_client.Client(user_agent=user_agent,consumer_key=consumer_key,
											consumer_secret=consumer_secret, token=token,
											secret=secret)
def get_url_oauth_(self):
	self.token , self.secret, url = self.discogsclient.get_authorize_url()
	self.save()
	return url

def get_oauth_(self, oauth_verifier):
	try:
		access_token, access_secret = self.discogsclient.get_access_token(oauth_verifier)
	except HTTPError:
		print('Unable to authenticate.')
		sys.exit(1)
def scrapp_user_(self):
	self.user = self.discogsclient.identity()
	self.name = self.user.name
	self.profile = self.user.profile
	self.location = self.user.location
	self.home_page = self.user.home_page
	self.url = self.user.url
	self.num_lists = self.user.num_lists
	self.num_wantlist = self.user.num_wantlist
	self.rating_avg = self.user.rating_avg
	self.rating_avg = self.user.rating_avg 	
	self.save()	
	
def get_collection_(self):
	self.collection = self.user.collection_folders[1].releases
	self.len_collection = self.collection.count

def scrapp_collection_(self,Release_obj, Artist_obj, Label_obj, 
							Track_obj, Style_obj, Genre_obj, Video_obj, ArtistUrl_obj):

	# The objects from Models are passes as parameter, so we don't have to import them here
	# It allows to import scrapp_collection_ in models
	for index in range(self.len_collection):
		sleep(2)
		release_discogs = self.collection.__getitem__(index=index).release
		print(release_discogs.id)
		# We want to check if release_id is already in db to avoid useless scrapping
		release = Release_obj.objects.get_or_create(id=release_discogs.id ,title=release_discogs.title, 
										year=int(release_discogs.year),
								#formats=release_discogs.formats, 
								country=release_discogs.country,
								url=release_discogs.url)[0]
		print(release.id)
		print(release.title)

		self.releases.add(release)

		for artist_discogs in release_discogs.artists:
			try:
				artist = Artist_obj.objects.get_or_create(id=artist_discogs.id,name=artist_discogs.name,
												real_name=artist_discogs.real_name,
												profile=artist_discogs.profile)[0]
				for url in artist_discogs.urls:
					ArtistUrl_obj.objects.get_or_create(url=url, artist=artist)
				release.artists.add(artist)

			except:
				print(f"artist_discogs  {artist_discogs}")

		for label_discogs in release_discogs.labels:
			#label = Label_obj.objects.get_or_create(id=label_discogs.id,name=label_discogs.name,
										#profile=label_discogs.profile,
										#url = label_discogs.url)[0]

			# I think we may want to implement our version of get_or_create when dealing with ids
			# to avoid the four following lines

			label = Label_obj.objects.get_or_create(id=label_discogs.id)[0]
			label.name = label_discogs.name
			label.profile = label_discogs.profile
			label.url = label_discogs.url

			release.labels.add(label)

		for track_discogs in release_discogs.tracklist:
			track = Track_obj.objects.get_or_create(title=track_discogs.title, 
										position=track_discogs.position,release=release, 
										 duration=track_discogs.duration)[0]

		for style_discogs in release_discogs.styles:
			style = Style_obj.objects.get_or_create(name=style_discogs)[0]
			release.styles.add(style)

		for genre_discogs in release_discogs.genres:
			genre = Genre_obj.objects.get_or_create(name=genre_discogs)[0]
			release.genres.add(genre)

		for video_discogs in release_discogs.videos:
			video = Video_obj.objects.get_or_create(title=video_discogs.title, url=video_discogs.url,
										description=video_discogs.description)[0]
			release.videos.add(video)

		self.save()
