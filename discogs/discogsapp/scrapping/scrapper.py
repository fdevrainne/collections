import os
import sys
import discogs_client
from discogs_client.exceptions import HTTPError
from time import sleep
from tqdm import tqdm
import numpy as np
from discogsapp.models import User, Release, Track, Artist, Label, Genre, Style, Video

consumer_key = 'LPCdkfqipSxdKywYLhmk'
consumer_secret = 'qQhzfPebKLCDrzImGWzXGzAGHQjTBKba'
user_agent = 'discogs_api_example/2.0'


class DiscogsUser(User):
	def __init__(self,token=None, secret=None):
		self.discogsclient = discogs_client.Client(user_agent=user_agent,consumer_key=consumer_key,
												consumer_secret=consumer_secret, token=token,
												secret=secret)
		User.__init__(self)

	def get_url_oauth(self):
		token, secret, url = self.discogsclient.get_authorize_url()

		self.token = token 
		self.secret = "secret"
		self.save()

		return url

	def get_oauth(self, oauth_verifier):
		try:
			access_token, access_secret = self.discogsclient.get_access_token(oauth_verifier)
		except HTTPError:
			print('Unable to authenticate.')
			sys.exit(1)
	def scrapp_user(self):
		self.user = self.discogsclient.identity()

		super(DiscogsUser, self).objects.create(name=self.user.name, profile=self.user.profile,
								location=self.user.location,home_page=self.user.home_page,
								url=self.user.url,num_wantlist=self.user.num_wantlist,
								num_lists=self.user.num_lists,rating_avg=self.user.rating_avg,
								releases_contributed=self.user.releases_contributed)    		
		
	def get_collection(self):
		self.collection = self.user.collection_folders[1].releases
		self.len_collection = self.collection.count

	def scrapp_collection(self):
		for index in range(self.len_collection):
			sleep(1)
			release_discogs = self.collection.__getitem__(index=index).release
			print(release_discogs.id)
			# We want to check if release_id is already in db to avoid useless scrapping
			release = Release.objects.create(id=release_discogs.id ,title=release_discogs.title, 
											year=release_discogs.year,
									#formats=release_discogs.formats, 
									country=release_discogs.country,
									url=release_discogs.url)

			#super
			super(DiscogsUser, self).releases.add(release)

			for artist_discogs in release_discogs.artists:
				artist = Artist.objects.create(id=artist_discogs.id,name=artist_discogs.name,
												real_name=artist_discogs.real_name,
												profile=artist_discogs.profile,urls=artist_discogs.urls)
				release.artists.add(artist)

			for label_discogs in release_discogs.labels:
				label = Label.objects.create(id=label_discogs.id,name=label_discogs.name,
											profile=label_discogs.profile,
											url = label_discogs.url)
				release.labels.add(label)

			for track_discogs in release_discogs.tracklist:
				track = Track.objects.create(title=track_discogs.title, 
											position=track_discogs.position,release=release, 
											 duration=track_discogs.duration, url=track_discogs.url)

			for style_discogs in release_discogs.styles:
				style = Style.objects.create(name=style_discogs.name)
				release.styles.add(style)

			for genre_discogs in release_discogs.genres:
				genre = Genre.objects.create(name=genre_discogs.name)
				release.genres.add(genre)

			for video_discogs in release_discogs.videos:
				video = Video.objects.create(title=video_discogs.title, url=video_discogs.url,
											description=video_discogs.description)
				release.videos.add(video)



