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

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT)

    def setUp(self):
        self.url = "http://www.latimes.com"
        self.url2 = "http://www.cnn.com"

    def test_archive(self):
        obj = TestModel.objects.create(archive=self.url)
        self.assertTrue(os.path.exists(obj.archive.path))
        obj.archive.archive_url
        obj.archive.archive_timestamp
        obj.archive = self.url2
        obj.save()
        self.assertTrue(os.path.exists(obj.archive.path))
        obj.save()
        obj.archive.delete()
        with self.assertRaises(ValueError):
            obj.archive.path



