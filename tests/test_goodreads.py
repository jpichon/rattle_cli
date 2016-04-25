import datetime
import unittest
from unittest import mock

from rattle_cli.goodreads import Goodreads


class TestUser(unittest.TestCase):

    user_id = "1234"
    user_name = "Test User"

    user_xml = """<?xml version="1.0" encoding="UTF-8"?>
<GoodreadsResponse>
  <Request />
  <user id="%(user_id)s">
    <name>%(user_name)s</name>
  </user>
</GoodreadsResponse>
"""

    def setUp(self):
        session = mock.Mock()
        self.goodreads = Goodreads(session)

    def test_initialise_user(self):
        self.assertEqual(self.goodreads.user_id, None)

        xml = self.user_xml % {'user_id': self.user_id,
                               'user_name': self.user_name}
        response = mock.Mock()
        response.content = xml

        self.goodreads.session.get.return_value = response
        self.goodreads.initialise_user()
        self.assertEqual(self.goodreads.user_id, self.user_id)

    def test_initialise_no_user_id(self):
        self.assertEqual(self.goodreads.user_id, None)

        response = mock.Mock()
        response.content = """<?xml version="1.0" encoding="UTF-8"?>
<GoodreadsResponse>
  <Request />
  <user><name>User Name</name></user>
</GoodreadsResponse>
"""
        self.goodreads.session.get.return_value = response
        with self.assertRaises(SystemExit):
            self.goodreads.initialise_user()

    def test_authenticate_user_cant_parse(self):
        self.assertEqual(self.goodreads.user_id, None)

        response = mock.Mock()
        response.content = ""

        self.goodreads.session.get.return_value = response
        with self.assertRaises(SystemExit):
            self.goodreads.get_authenticated_user()


class TestReviewParsing(unittest.TestCase):

    def setUp(self):
        session = mock.Mock()
        self.goodreads = Goodreads(session)
        self.review = {'id': 1}

    def test_parse_date_read(self):
        self.review['read_at'] = "Fri Mar 04 00:00:00 -0800 2016"

        result = self.goodreads.parse_date_read(self.review)
        self.assertIsInstance(result, datetime.datetime)
        self.assertEqual(result.year, 2016)
        self.assertEqual(result.month, 3)
        self.assertEqual(result.day, 4)

    def test_parse_date_read_cant_parse(self):
        bad_date = "This is not a date"
        self.review['read_at'] = bad_date

        result = self.goodreads.parse_date_read(self.review)
        self.assertIsInstance(result, str)
        self.assertEqual(result, bad_date)

    def test_parse_date_read_empty(self):
        self.review['read_at'] = ""

        result = self.goodreads.parse_date_read(self.review)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "")

    def test_parse_date_no_tag(self):
        result = self.goodreads.parse_date_read(self.review)
        self.assertEqual(result, "")

    def test_parse_author_single(self):
        author = "John Doe"
        self.review['book'] = {'authors': {'author': {'name': author}}}

        result = self.goodreads.parse_author(self.review)
        self.assertEqual(result, author)

    def test_parse_author_two_authors(self):
        self.review['book'] = {'authors': {'author': [{'name': 'John Doe'},
                                                      {'name': 'Jane Doe'}]}}

        result = self.goodreads.parse_author(self.review)
        self.assertEqual(result, "John Doe, Jane Doe")

    def test_parse_author_empty(self):
        self.review['book'] = {'authors': {'author': ""}}

        result = self.goodreads.parse_author(self.review)
        self.assertEqual(result, "")

    def test_parse_author_no_tag(self):
        result = self.goodreads.parse_author(self.review)
        self.assertEqual(result, "")

    def test_parse_shelves_single(self):
        shelf = "My cool shelf that's mine"
        self.review['shelves'] = {'shelf': {'@name': shelf}}

        result = self.goodreads.parse_shelves(self.review)
        self.assertEqual(result, [shelf])

    def test_parse_shelves_two_shelves(self):
        shelf_one = "My shelf"
        shelf_two = "Your shelf"
        self.review['shelves'] = {'shelf': [{'@name': shelf_one},
                                            {'@name': shelf_two}]}

        result = self.goodreads.parse_shelves(self.review)
        self.assertIsInstance(result, list)
        self.assertCountEqual(result, [shelf_one, shelf_two])

    def test_parse_shelves_empty(self):
        self.review['shelves'] = {'shelf': {}}

        result = self.goodreads.parse_shelves(self.review)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_parse_shelves_no_tag(self):
        result = self.goodreads.parse_shelves(self.review)
        self.assertEqual(result, [])
