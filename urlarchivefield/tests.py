#! -*- coding: utf-8 -*-
import os
import six
import shutil
import tempfile as tempfile
from django.db import models
from datetime import datetime
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

    def assertIsInstance(self, value, type):
        self.assertTrue(isinstance(value, type))

    def test_archive(self):
        obj = TestModel.objects.create(archive=self.url)
        self.assertFalse(obj.archive.name == self.url)
        self.assertTrue(os.path.exists(obj.archive.path))
        self.assertIsInstance(obj.archive.archive_url, six.string_types)
        self.assertIsInstance(obj.archive.archive_timestamp, datetime)
        obj.archive = self.url2
        obj.save()
        self.assertTrue(os.path.exists(obj.archive.path))
        obj.save()
        obj.archive.delete()
        with self.assertRaises(ValueError):
            obj.archive.path
        obj = TestModel()
        obj.save()
        obj.archive.name
        with self.assertRaises(ValueError):
            obj.archive.path
        obj.archive = None
        obj.save()


