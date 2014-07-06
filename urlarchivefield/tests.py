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
    archive2 = URLArchiveField(upload_to="test_archive", compress=False)


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
        self.url2 = "http://www.cnn.com/"
        self.long_url = "http://www.washingtonpost.com/investigations/us-\
intelligence-mining-data-from-nine-us-internet-companies-in-broad-secret-\
program/2013/06/06/3a0c0da8-cebf-11e2-8845-d970ccb04497_story.html"

    def assertIsInstance(self, value, type):
        self.assertTrue(isinstance(value, type))

    def test_archive(self):
        obj = TestModel.objects.create(archive=self.url)
        self.assertFalse(obj.archive.name == self.url)
        self.assertTrue(os.path.exists(obj.archive.path))
        self.assertIsInstance(obj.archive.archive_url, six.string_types)
        self.assertIsInstance(obj.archive.archive_timestamp, datetime)
        obj.archive.archive_html
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

    def test_long_url(self):
        obj = TestModel.objects.create(archive=self.long_url)
        self.assertFalse(obj.archive.name == self.long_url)
        self.assertTrue(os.path.exists(obj.archive.path))
        self.assertIsInstance(obj.archive.archive_url, six.string_types)
        self.assertIsInstance(obj.archive.archive_timestamp, datetime)
        obj.archive.archive_html

    def test_compress(self):
        obj = TestModel.objects.create(archive2=self.url)
        obj.archive2.archive_html

    def test_deconstruct(self):
        try:
            field1 = URLArchiveField(compress=False)
            name, path, args, kwargs = field1.deconstruct()
        except NotImplementedError:
            return
        field2 = URLArchiveField(*args, **kwargs)
        self.assertEqual(field1.archive2, field2.archive2)
