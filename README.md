# django-urlarchivefield

A custom Django model field that automatically archives a URL

[![Build Status](https://travis-ci.org/pastpages/django-urlarchivefield.svg)](https://travis-ci.org/pastpages/django-urlarchivefield)

## Getting started

Install this library from the Python Package Index.

```bash
$ pip install django-urlarchivefield
```

Add it to one of your models.

```python
from django.db import models
from .fields import URLArchiveField

class MyModel(models.Model):
    archive = URLArchiveField(upload_to="my_archive")
```

Saving an URL's HTML content to your ``MEDIA_ROOT`` becomes this easy.

```python
>>> obj = MyModel.objects.create(archive="http://www.latimes.com")
```

The field attribute now has all the typical qualities of [a Django FileField](https://docs.djangoproject.com/en/dev/ref/models/fields/#filefield)
with a few additions.

```python
# Return the URL that was originally submitted for archival
>>> obj.archive.archive_url
# Return the timestamp when the archive was created
>>> obj.archive.archive_timestamp
# Return the HTML from the archive
>>> obj.archive.archive_html
```

By default, the data are compressed before being saved by gzip. If you'd rather store the raw
HTML set the ``compress`` keyword argument on the field.

```python
class MyModel(models.Model):
    archive = URLArchiveField(upload_to="my_archive", compress=False)
```

## Credits

This is a joint project of [PastPages.org](http://pastpages.org), The Reynolds Journalism Institute and the University of Missouri.
