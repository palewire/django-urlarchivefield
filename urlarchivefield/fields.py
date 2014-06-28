import six
import storytracker
from django.db import models


class URLArchiveField(
    six.with_metaclass(models.SubfieldBase, models.FileField)
):
    """
    TK
    """
    def pre_save(self, model_instance, add):
        "Returns field's value just before saving."
        file = super(FileField, self).pre_save(model_instance, add)
        if file and not file._committed:
            # Get the URL we're trying to save
            # Fetch a file from that URL
            # Save that URL to the database
            # (But how does the the url itself and timestamp ever get stored
            #   so it can be pulled off the object later when you access the
            #   the object? Do we need to extend the file descriptor perhaps?
            #   Also, how does it ingest a URL as the input?)
            file.save(file.name, file, save=False)
        return file

    def generate_filename(self, instance, filename):
        return storytracker.create_archive_filename(url, timestamp)
