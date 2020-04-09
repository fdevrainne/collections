from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField


class User(models.Model):
    username = models.TextField()
    name = models.TextField()
    profile = models.TextField()
    location = models.TextField()
    home_page = models.TextField()
    url = models.URLField()
    num_wantlist = models.IntegerField()
    num_lists = models.IntegerField()
    rating_avg = models.FloatField()
    release_contributed = models.IntegerField()
    release = models.ManyToManyField('Release')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'User {self.username}'

    def update_collection(self):
        # Call generic function updating a user's collection in DB by calling Discogs API
        pass

    class Meta:
        db_table = 'user'


class Release(models.Model):
    title = models.TextField()
    year = models.IntegerField()
    artist = models.ManyToManyField('Artist')
    genres = models.ManyToManyField('Genre')
    format = JSONField()
    styles = models.ManyToManyField('Style')
    label = models.ForeignKey('Label', on_delete=models.CASCADE)  # Why several labels ?
    country = models.TextField()  # Should this be a ForeignKey to a possible Country table ?
    #videos = models.ManyToManyField('Videos')  # Useful ? Could store url of video directly in track table by matching
    url = models.URLField()  # Useful ?

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Release {self.title} ({self.year})'

    class Meta:
        db_table = 'release'


class Track(models.Model):
    title = models.TextField()
    position = models.TextField()
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    artist = models.ManyToManyField('Artist')
    duration = models.FloatField()
    url = models.URLField()

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'{self.position} - {self.title}'

    class Meta:
        db_table = 'track'


class Artist(models.Model):
    name = models.TextField()
    real_name = models.TextField()
    profile = models.TextField()

    # Example : ['http://www.soundcloud.com/vinylspeedadjust','https://www.facebook.com/vinylspeedadjust',
    # 'https://www.youtube.com/VINYLSPEEDADJUST']. Should we do a many to many ?
    urls = ArrayField(models.CharField(max_length=200))

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
        db_table = 'artist'


class Label(models.Model):
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
        db_table = 'label'


class Genre(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Genre {self.name}'

    class Meta:
        db_table = 'genre'


class Style(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Style {self.name}'

    class Meta:
        db_table = 'style'
