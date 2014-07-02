#! -*- coding: utf-8 -*-
import os
import shutil
import tempfile as tempfile
from django.db import models
from django.test import TestCase
from .fields import URLArchiveField
from django.test.utils import override_settings

MEDIA_ROOT = tempfile.mkdtemp()


class TestModel(models.Model):
    archive = URLArchiveField(upload_to="test_archive")


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class URLArchiveTests(TestCase):

    @classmethod
    def setUpClass(cls):
        if not os.path.isdir(MEDIA_ROOT):
            os.makedirs(MEDIA_ROOT)

#    @classmethod
#    def tearDownClass(cls):
#        shutil.rmtree(MEDIA_ROOT)

    def setUp(self):
        self.url = "http://www.latimes.com"

    def test_archive(self):
        obj = TestModel.objects.create(archive=self.url)
        obj.archive = "http://www.cnn.com"
        obj.save()
        obj.archive.save("http://www.cnn.com")
        print obj.archive
