from django.db import models
from django.contrib.postgres.fields import ArrayField#, JSONField
from django_mysql.models import JSONField

from time import sleep
from .scrapping.scrapper import discogs_init_, get_url_oauth_, get_oauth_
from .scrapping.scrapper import scrapp_user_, get_collection_#, scrapp_collection_

class User(models.Model):
    username = models.TextField()
    name = models.TextField()
    profile = models.TextField()
    location = models.TextField()
    home_page = models.TextField()
    url = models.URLField()
    num_wantlist = models.IntegerField(null=True)
    num_lists = models.IntegerField( null=True)
    rating_avg = models.FloatField(null=True)
    releases_contributed = models.IntegerField(null=True)
    releases = models.ManyToManyField('Release',null=True)
    token = models.TextField()
    secret = models.TextField()
    session_key = models.TextField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'User {self.username}'

    def update_collection(self):
        # Call generic function updating a user's collection in DB by calling Discogs API
        pass

    class Meta:
        db_table = 'users'

User.discogs_init = discogs_init_
User.get_url_oauth = get_url_oauth_
User.get_oauth = get_oauth_
User.scrapp_user = scrapp_user_
User.get_collection = get_collection_

def scrapp_collection_(self):
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

        self.releases.add(release)

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

        self.save()

User.scrapp_collection = scrapp_collection_


class Release(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    year = models.IntegerField()
    artists = models.ManyToManyField('Artist')
    genres = models.ManyToManyField('Genre')
    #formats = JSONField()
    styles = models.ManyToManyField('Style')
    labels = models.ForeignKey('Label', on_delete=models.CASCADE,null=True)  # Why several labels ?
    country = models.TextField()  # Should this be a ForeignKey to a possible Country table ?
    videos = models.ManyToManyField('Video')
    url = models.URLField()

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Release {self.title} ({self.year})'

    class Meta:
        db_table = 'releases'


class Track(models.Model):
    title = models.TextField()
    position = models.TextField()
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    # artist below useless, cause Track already linked to Artist through Release
    #artist = models.ManyToManyField('Artist')
    duration = models.FloatField()
    url = models.URLField()

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'{self.position} - {self.title}'

    class Meta:
        db_table = 'tracks'


class Artist(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    real_name = models.TextField()
    profile = models.TextField()

    # How to deal with aliases ?
    #aliases = models.OneToMany(AliasesInArtist, blank=True)

    # To deal with artist / band / member recursivity, see self referencing many to many
    #https://www.caktusgroup.com/blog/2009/08/14/creating-recursive-symmetrical-many-to-many-relationships-in-django/
    #members =
    #groups =

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Artist {self.name}'

    class Meta:
        db_table = 'artists'


class ArtistUrl(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    url =  models.URLField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Urls {self.name}'

    class Meta:
        db_table = 'urls'


class Label(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    profile = models.TextField()
    url = models.URLField()

    # See self referencing many to many (as above for artists)
    #sublabels =
    #parent_label =

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Label {self.name}'

    class Meta:
        db_table = 'labels'


class Genre(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Genre {self.name}'

    class Meta:
        db_table = 'genres'


class Style(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Style {self.name}'

    class Meta:
        db_table = 'styles'

class Video(models.Model):
    title = models.TextField()
    url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Style {self.title}'

    class Meta:
        db_table = 'videos'