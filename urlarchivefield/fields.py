import os
import six
import copy
import logging
import storytracker
from django.db import models
from datetime import datetime
from django.core.files.base import ContentFile
from django.db.models.fields.files import FieldFile
from django.core.files.storage import default_storage
from django.utils.encoding import force_str, force_text
logger = logging.getLogger(__name__)


class URLArchiveFieldFile(FieldFile):

    def save(self, name, content, save=True):
        print "SAVE!"

        real_name = "%s.html" % (
            storytracker.create_archive_filename(
                url,
                datetime.now()
            ),
        )
        name = self.field.generate_filename(self.instance, real_name)
        print name
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
        basename = os.path.basename(self.name).replace(".html", "")
        return storytracker.reverse_archive_filename(basename)[0]
    archive_url = property(_get_archive_url)

    def _get_archive_timestamp(self):
        name = os.path.basename(self.name).replace(".html", "")
        return storytracker.reverse_archive_filename(name)[1]
    archive_timestamp = property(_get_archive_timestamp)


class URLArchiveField(models.FileField):
    """
    TK
    """
    attr_class = URLArchiveFieldFile

    def get_directory_name(self):
        return os.path.normpath(force_text(force_str(self.upload_to)))

    def generate_filename(self, instance, filename):
        return os.path.join(self.get_directory_name(), filename)
