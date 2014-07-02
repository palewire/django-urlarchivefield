import os
import six
import logging
import storytracker
from django.db import models
from datetime import datetime
from django.core.files.base import File
from django.core.files.base import ContentFile
from django.db.models.fields.files import FieldFile, FileDescriptor
from django.utils.encoding import force_str, force_text
logger = logging.getLogger(__name__)


class URLArchiveFieldFile(FieldFile):
    """
    Overrides the standard FieldFile to download and archive URLs when they
    are provided.
    """
    def save(self, name, content, save=True):
        # Fetch the data from the URL
        url = name
        content = ContentFile(storytracker.archive(url, compress=False))

        # Set the filename using our namespacing scheme
        archive_filename = "%s.html" % (
            storytracker.create_archive_filename(
                name,
                datetime.now()
            ),
        )
        name = self.field.generate_filename(self.instance, archive_filename)

        # Save the file with our namespace and archived content
        self.name = self.storage.save(name, content)
        setattr(self.instance, self.field.name, self.name)

        # Update the filesize cache
        self._size = content.size
        self._committed = True

        # Save the object because it has changed, unless save is False
        if save:
            self.instance.save()
    save.alters_data = True

    def _get_archive_url(self):
        """
        Parses archive namespace to return the URL that was saved.
        """
        basename = os.path.basename(self.name).replace(".html", "")
        return storytracker.reverse_archive_filename(basename)[0]
    archive_url = property(_get_archive_url)

    def _get_archive_timestamp(self):
        """
        Parses archive namespace to return timestamp when URL was saved.
        """
        name = os.path.basename(self.name).replace(".html", "")
        return storytracker.reverse_archive_filename(name)[1]
    archive_timestamp = property(_get_archive_timestamp)


class URLArchiveFileDescriptor(FileDescriptor):
    """
    Override of standard descriptor so it will mark URLs for archive
    """
    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))

        file = instance.__dict__[self.field.name]

        if isinstance(file, six.string_types) or file is None:
            attr = self.field.attr_class(instance, self.field, file)
            # Our only change to the standard routine is right here
            # where we mark any URLs that come in as uncommitted so
            # that they are archived when a save routine fires.
            if 'http://' in file or 'https://' in file:
                attr._committed = False
            instance.__dict__[self.field.name] = attr

        elif isinstance(file, File) and not isinstance(file, FieldFile):
            file_copy = self.field.attr_class(instance, self.field, file.name)
            file_copy.file = file
            file_copy._committed = False
            instance.__dict__[self.field.name] = file_copy

        elif isinstance(file, FieldFile) and not hasattr(file, 'field'):
            file.instance = instance
            file.field = self.field
            file.storage = self.field.storage

        return instance.__dict__[self.field.name]


class URLArchiveField(models.FileField):
    """
    A custom Django model field that archives HTML data.
    """
    attr_class = URLArchiveFieldFile
    descriptor_class = URLArchiveFileDescriptor

    def get_directory_name(self):
        return os.path.normpath(force_text(force_str(self.upload_to)))

    def generate_filename(self, instance, filename):
        return os.path.join(self.get_directory_name(), filename)
