#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import datetime
import unittest
from unittest import mock

from rattle_cli.goodreads import Book, Goodreads
from rattle_cli.tests.xml_fixtures import GoodreadsXMLFactory


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
        self.review = {'id': 1, 'date_updated': ''}
        self.title = "Test"

    def test_parse_date_read(self):
        self.review['read_at'] = "Fri Mar 04 00:00:00 -0800 2016"

        result = self.goodreads.parse_date_read(self.review, self.title)
        self.assertIsInstance(result, datetime.datetime)
        self.assertEqual(result.year, 2016)
        self.assertEqual(result.month, 3)
        self.assertEqual(result.day, 4)

    def test_parse_date_read_cant_parse(self):
        bad_date = "This is not a date"
        self.review['read_at'] = bad_date

        result = self.goodreads.parse_date_read(self.review, self.title)
        self.assertIsInstance(result, str)
        self.assertEqual(result, bad_date)

    def test_parse_date_read_empty(self):
        self.review['read_at'] = ""

        result = self.goodreads.parse_date_read(self.review, self.title)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "")

    def test_parse_no_date_read_and_use_date_updated(self):
        self.review['read_at'] = ""
        self.review['date_updated'] = "Thu Feb 15 13:54:37 -0800 2018"

        result = self.goodreads.parse_date_read(self.review, self.title)
        self.assertIsInstance(result, datetime.datetime)
        self.assertEqual(result.year, 2018)
        self.assertEqual(result.month, 2)
        self.assertEqual(result.day, 15)

    def test_parse_date_no_tag(self):
        result = self.goodreads.parse_date_read(self.review, self.title)
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

    def test_parse_author_utf8(self):
        author = "村上春樹"
        self.review['book'] = {'authors': {'author': {'name': author}}}

        result = self.goodreads.parse_author(self.review)
        self.assertEqual(result, author)

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

    def test_parse_shelves_utf8(self):
        shelf_one = "广东话"
        shelf_two = "čeština"
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


class TestReviewRetrieval(unittest.TestCase):

    book_title = "Wonderful Book Title %d"

    def setUp(self):
        session = mock.Mock()
        self.goodreads = Goodreads(session)
        self.xml_factory = GoodreadsXMLFactory()

    def test_retrieve_reviews(self):
        response = mock.Mock()
        response.content = self.xml_factory.create_full_xml_response()
        self.goodreads.session.post.return_value = response

        result = self.goodreads.retrieve_reviews()
        self.assertIsInstance(result, OrderedDict)
        self.assertIn('review', result.keys())

        review = result['review']  # Only one review, so not a list
        self.assertIn('book', review.keys())
        self.assertIn('shelves', review.keys())

    def test_retrieve_reviews_shelves(self):
        response = mock.Mock()
        response.content = self.xml_factory.create_full_xml_response(shelves=2)
        self.goodreads.session.post.return_value = response

        result = self.goodreads.retrieve_reviews("read")
        self.assertIsInstance(result, OrderedDict)
        self.assertIn('review', result.keys())

        review = result['review']  # Only one review, so not a list
        self.assertIn('book', review.keys())
        self.assertIn('shelves', review.keys())
        shelves = review['shelves']
        self.assertIn('shelf', shelves.keys())
        shelf = shelves['shelf']
        self.assertIn('@name', shelf[0])
        self.assertEqual('read', shelf[0]['@name'])
        self.assertEqual('true', shelf[0]['@exclusive'])
        self.assertEqual('Self #1', shelf[1]['@name'])
        self.assertEqual('false', shelf[1]['@exclusive'])

    def test_retrieve_reviews_multiple_reviews(self):
        review_count = 10
        xml = self.xml_factory.create_full_xml_response(reviews=review_count)
        response = mock.Mock()
        response.content = xml
        self.goodreads.session.post.return_value = response

        result = self.goodreads.retrieve_reviews()
        self.assertIsInstance(result, OrderedDict)
        self.assertIn('review', result.keys())

        # When there are multiple reviews, 'review' is a list
        self.assertIsInstance(result['review'], list)
        self.assertEqual(len(result['review']), review_count)
        for review in result['review']:
            self.assertIn('book', review.keys())
            self.assertIn('shelves', review.keys())

    def test_get_books_one_book(self):
        response = mock.Mock()
        response.content = self.xml_factory.create_full_xml_response()
        self.goodreads.session.post.return_value = response

        result = self.goodreads.get_books()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, self.book_title % 0)

    def test_get_books_multiple_books(self):
        review_count = 10
        xml = self.xml_factory.create_full_xml_response(reviews=review_count)
        response = mock.Mock()
        response.content = xml
        self.goodreads.session.post.return_value = response

        result = self.goodreads.get_books()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), review_count)
        for book in result:
            self.assertIsInstance(book, Book)

        self.assertEqual(result[1].title, self.book_title % 1)

    def test_get_books_two_pages(self):
        review_count = 8

        def fake_post(url, data):
            if data['page'] == 1:
                start, end = 1, 5
            elif data['page'] == 2:
                start, end = 6, 8
            else:
                self.fail("Called with page number %d" % data['page'])

            response = mock.Mock()
            response.content = self.xml_factory.create_full_xml_response(
                reviews=review_count,
                start_cnt=start,
                end_cnt=end)
            return response

        self.goodreads.session.post = fake_post

        result = self.goodreads.get_books()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), review_count)

    def test_get_books_two_pages_single_review_on_page_two(self):
        review_count = 8

        def fake_post(url, data):
            if data['page'] == 1:
                start, end = 1, 7
            elif data['page'] == 2:
                start, end = 8, 8
            else:
                self.fail("Called with page number %d" % data['page'])

            response = mock.Mock()
            response.content = self.xml_factory.create_full_xml_response(
                reviews=review_count,
                start_cnt=start,
                end_cnt=end)
            return response

        self.goodreads.session.post = fake_post

        result = self.goodreads.get_books()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), review_count)

    def test_get_books_multiple_pages(self):
        review_count = 100

        def fake_post(url, data):
            page = data['page']
            if page <= 10:
                start = (page-1) * 10 + 1
                end = page * 10
            else:
                self.fail("Called with page number %d" % data['page'])

            response = mock.Mock()
            response.content = self.xml_factory.create_full_xml_response(
                reviews=review_count,
                start_cnt=start,
                end_cnt=end)
            return response

        self.goodreads.session.post = fake_post

        result = self.goodreads.get_books()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), review_count)

    def test_get_books_multiple_pages_single_review(self):
        review_count = 12

        def fake_post(url, data):
            if data['page'] <= review_count:
                start, end = data['page'], data['page']
            else:
                self.fail("Called with page number %d" % data['page'])

            response = mock.Mock()
            response.content = self.xml_factory.create_full_xml_response(
                reviews=review_count,
                start_cnt=start,
                end_cnt=end)
            return response

        self.goodreads.session.post = fake_post

        result = self.goodreads.get_books()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), review_count)
