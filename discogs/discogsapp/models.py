"""
In this file are defined the Django Models that are used to create tables in the PostgreSQL DataBase as well as when
accessing objects via the Django ORM.
The following models are defined (order in the file counts, a model depending on another one via a OneToMany (o2m) or
ManyToMany (m2m) relation must be defined after)
"""
# Create your models here.
from __future__ import absolute_import, division, print_function, unicode_literals
import sys


from django.db import models
from django.db.models import Q, UniqueConstraint
from django.utils.timezone import datetime
from django.contrib.postgres.fields import JSONField


# Maybe id should be an integer ? For sure and everywhere

# Rather than creating ImagesInRelease, ImagesInLabel, ImagesInArtist, should we create imagesIn with a third extra column "in what ?".
# As possible values for this field, we would have "Release", or "Label", or "Artist" ...

class User(models.Model):
	id = models.TextField(primary_key=True, db_index=True)

	username = models.TextField(null=True)
	releases_contributed = models.TextField(null=True)
   	num_collection = IntegerField(blank=True, null=True)
    num_wantlist = IntegerField(blank=True, null=True)
    num_lists = IntegerField(blank=True, null=True)
    rank = = models.FloatField(null=True)
    rating_avg = = models.FloatField(null=True)
    url = models.TextField(null=True)
    name = models.TextField(null=True)
    profile = models.TextField(null=True)
    location = models.TextField(null=True)
    home_page = models.TextField(null=True)
    registered = models.TextField(null=True)
    collection = OneToMany(CollectionFolder, blank=True)

# Are the following columns wanted ?

    #inventory = ObjectCollection('Listing', key='listings', url_key='inventory_url')
    #wantlist = ObjectCollection('WantlistItem', key='wants', url_key='wantlist_url', list_class=Wantlist)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'users'


class Release(PrimaryAPIObject):
    id = models.TextField(primary_key=True, db_index=True)
    title = models.TextField(null=True)
    year = models.IntegerField(blank=True, null=True)
    thumb = models.TextField(null=True)
    data_quality = models.TextField(null=True)
    status = models.TextField(null=True)
    genres = models.OneToMany(GenresInRelease, blank=True)
    images = models.OneToMany(ImagesInRelease, blank=True)
    country = models.TextField(null=True)
    notes = models.TextField(null=True)
    formats = models.TextField(null=True)

# Example of the variable formats : [{'qty': '1', 'descriptions': ['12"', 'EP'], 'name': 'Vinyl'}]
# WHat should be done ?

# JSONField ?

    styles = models.OneToMany(Styles, blank=True)
    url = models.TextField(null=True)

    videos = models.OneToMany(VideosInRelease, blank=True)
    tracks = models.OneToMany(TracksInRelease, blank=True)
    artists = models.OneToMany(ArtistsInRelease, blank=True)

# Are they really needed ?
    #credits = ListField('Artist', key='extraartists')
    #companies = ListField('Label')
    labels = models.OneToMany(LabelsInRelease, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'users'

class Artist(PrimaryAPIObject):
    id =  models.TextField(primary_key=True, db_index=True)
    name =  models.TextField(null=True)
    real_name = models.TextField(null=True)
    images = models.OneToMany(ImagesInArtist, blank=True)
    profile = models.TextField(null=True)
    data_quality = models.TextField(null=True)

    name_variations = models.OneToMany(NamesinArtist, blank=True)
    url = models.TextField(null=True)

    # example for urls field ['http://www.soundcloud.com/vinylspeedadjust','https://www.facebook.com/vinylspeedadjust','https://www.youtube.com/VINYLSPEEDADJUST']
    urls = models.OneToMany(UrlsinArtist, blank=True)
    aliases = models.OneToMany(AliasesInArtist, blank=True)

    # An artist can be actually a band. Bands and/or artists are part of this band and so on ...
    # How to deal with the reference ?
    #members = models.OneToMany(Artist, blank=True)

    groups = models.OneToMany(GroupsInArtist, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'artists'


class Label(PrimaryAPIObject):
    id = models.TextField(primary_key=True, db_index=True)
    name =  models.TextField(null=True)
    #profile =  models.TextField(null=True)
    urls = models.OneToMany(UrlsinLabel blank=True)
    images = models.OneToMany(ImagesInLabel, blank=True)
    #contact_info = SimpleField()
    data_quality = models.TextField(null=True)
    url = models.TextField(null=True)

    # Same with the following column, that also are labels
    sublabels = ListField('Label')
    parent_label = ObjectField('Label', optional=True)
    
    # We don't want this one. It will lead to too much scrapping, I just leave it, so you see it exists
    #releases = ObjectCollection('Release')

    # We want each release to link to a label with label_id (also more than one label_id for a release is possible)

############################################################################################################################################
class Master(PrimaryAPIObject):
    id = SimpleField()
    title = SimpleField()
    data_quality = SimpleField()
    styles = SimpleField()
    genres = SimpleField()
    images = SimpleField()
    url = SimpleField(key='uri')
    videos = ListField('Video')
    tracklist = ListField('Track')
    main_release = ObjectField('Release', as_id=True)
    versions = ObjectCollection('Release')

    def __init__(self, client, dict_):
        super(Master, self).__init__(client, dict_)
        self.data['resource_url'] = '{0}/masters/{1}'.format(client._base_url, dict_['id'])

    def __repr__(self):
        return self.repr_str('<Master {0!r} {1!r}>'.format(self.id, self.title))


class Track(SecondaryAPIObject):
    duration = SimpleField()
    position = SimpleField()
    title = SimpleField()
    artists = ListField('Artist')
    credits = ListField('Artist', key='extraartists')

    def __repr__(self):
        return self.repr_str('<Track {0!r} {1!r}>'.format(self.position, self.title))



class Video(SecondaryAPIObject):
    duration = SimpleField()
    embed = SimpleField()
    title = SimpleField()
    description = SimpleField()
    url = SimpleField(key='uri')




class Wantlist(PaginatedList):
    def add(self, release, notes=None, notes_public=None, rating=None):
        release_id = release.id if isinstance(release, Release) else release
        data = {
            'release_id': str(release_id),
            'notes': notes,
            'notes_public': notes_public,
            'rating': rating,
        }
        self.client._put(self.url + '/' + str(release_id), omit_none(data))
        self._invalidate()

    def remove(self, release):
        release_id = release.id if isinstance(release, Release) else release
        self.client._delete(self.url + '/' + str(release_id))
        self._invalidate()


class OrderMessagesList(PaginatedList):
    def add(self, message=None, status=None, email_buyer=True, email_seller=False):
        data = {
            'message': message,
            'status': status,
            'email_buyer': email_buyer,
            'email_seller': email_seller,
        }
        self.client._post(self.url, omit_none(data))
        self._invalidate()


class MixedPaginatedList(BasePaginatedResponse):
    """A paginated list of objects identified by their type parameter."""
    def __init__(self, client, url, key):
        super(MixedPaginatedList, self).__init__(client, url)
        self._list_key = key

    def _transform(self, item):
        # In some cases, we want to map the 'title' key we get back in search
        # results to 'name'. This way, you can repr() a page of search results
        # without making 50 requests.
        if item['type'] in ('label', 'artist'):
            item['name'] = item['title']

        return CLASS_MAP[item['type']](self.client, item)





class WantlistItem(PrimaryAPIObject):
    id = SimpleField()
    rating = SimpleField(writable=True)
    notes = SimpleField(writable=True)
    notes_public = SimpleField(writable=True)
    release = ObjectField('Release', key='basic_information')
