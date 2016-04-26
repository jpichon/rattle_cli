#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import unittest

from rattle_cli.bookarranger import BookArranger
from rattle_cli.goodreads import Book


class TestBookArrangerLangSort(unittest.TestCase):

    def setUp(self):
        # Let's create some books with a few shelves
        self.langs = {'en': 5, 'it': 3, 'ru': 4, 'other': 3}
        self.books = []
        for i in range(0, 15):
            shelves = ['read']
            if i % 3 == 0:
                shelves += ['en']
            if i % 2 == 0:
                shelves += ['irrelevant']
            if i % 5 == 0:
                shelves += ['another genre']
            if i in (2, 8, 13):
                shelves += ['it']
            if i in (4, 7, 11, 14):
                shelves += ['ru']

            book = Book(title="Book #%d" % i, author="An author",
                        date_read=datetime.date(2016, 4, 25),
                        shelves=shelves)
            self.books += [book]

        self.ba = BookArranger(self.books)

    def test_sort_by_language(self):
        for lang in ('en', 'it', 'ru'):
            books = self.ba.sort_by_language(languages=[lang])
            self.assertCountEqual(books.keys(), [lang])
            self.assertEqual(len(books[lang]), self.langs[lang])

    def test_sort_by_language_two(self):
        books = self.ba.sort_by_language(languages=['it', 'ru'])
        self.assertCountEqual(books.keys(), ['it', 'ru'])
        self.assertEqual(len(books['it']), self.langs['it'])
        self.assertEqual(len(books['ru']), self.langs['ru'])

    def test_sort_by_language_plus_default(self):
        books = self.ba.sort_by_language(languages=['it', 'en', 'ru'],
                                         other=True)
        self.assertCountEqual(books.keys(), ['it', 'en', 'ru', 'default'])
        self.assertEqual(len(books['it']), self.langs['it'])
        self.assertEqual(len(books['en']), self.langs['en'])
        self.assertEqual(len(books['ru']), self.langs['ru'])
        self.assertEqual(len(books['default']), self.langs['other'])

    def test_sort_by_language_two_plus_default(self):
        other_cnt = self.langs['other'] + self.langs['it']
        books = self.ba.sort_by_language(languages=['en', 'ru'],
                                         other=True)
        self.assertCountEqual(books.keys(), ['en', 'ru', 'default'])
        self.assertEqual(len(books['en']), self.langs['en'])
        self.assertEqual(len(books['ru']), self.langs['ru'])
        self.assertEqual(len(books['default']), other_cnt)

    def test_sort_by_language_change_default_label(self):
        other_cnt = self.langs['other'] + self.langs['it'] + self.langs['ru']
        books = self.ba.sort_by_language(languages=['en'],
                                         other=True,
                                         other_label='その他')
        self.assertCountEqual(books.keys(), ['en', 'その他'])
        self.assertEqual(len(books['en']), self.langs['en'])
        self.assertEqual(len(books['その他']), other_cnt)

    def test_sort_by_language_only_default(self):
        books = self.ba.sort_by_language(other=True)
        self.assertCountEqual(books.keys(), ['default'])
        self.assertEqual(len(books['default']), len(self.books))

    def test_sort_by_language_no_books_for_that_language(self):
        books = self.ba.sort_by_language(languages=['sp'])
        self.assertCountEqual(books.keys(), ['sp'])
        self.assertEqual(len(books['sp']), 0)

    def test_sort_by_language_no_books_for_a_language(self):
        books = self.ba.sort_by_language(languages=['en', 'sp'])
        self.assertCountEqual(books.keys(), ['sp', 'en'])
        self.assertEqual(len(books['en']), self.langs['en'])
        self.assertEqual(len(books['sp']), 0)

    def test_sort_by_language_no_books_for_that_language_plus_default(self):
        books = self.ba.sort_by_language(languages=['sp'],
                                         other=True)
        self.assertCountEqual(books.keys(), ['sp', 'default'])
        self.assertEqual(len(books['default']), len(self.books))
        self.assertEqual(len(books['sp']), 0)

    def test_sort_by_language_no_languages(self):
        books = self.ba.sort_by_language()
        self.assertEqual(books, {})

    def test_sort_by_language_and_year(self):
        books = self.ba.sort_by_language(languages=['it'],
                                         year=2016)
        self.assertCountEqual(books.keys(), ['it'])
        self.assertEqual(len(books['it']), self.langs['it'])


class TestBookArrangerLangYearSort(unittest.TestCase):

    def setUp(self):
        self.books = [
            Book(title="A book (1)", author="An author",
                 date_read=datetime.date(2016, 4, 25),
                 shelves=['read', 'en']),
            Book(title="A book (2)", author="An author",
                 date_read=datetime.date(2015, 4, 25),
                 shelves=['read', 'es']),
            Book(title="A book (3)", author="An author",
                 date_read=datetime.date(2016, 4, 25),
                 shelves=['read', 'es']),
            Book(title="A book (4)", author="An author",
                 date_read=datetime.date(2015, 4, 25),
                 shelves=['read', 'es']),
            Book(title="A book (5)", author="An author",
                 date_read=datetime.date(2016, 4, 25),
                 shelves=['read', 'fr'])]

        self.ba = BookArranger(self.books)

    def test_one_lang(self):
        books = self.ba.sort_by_language(languages=['en'],
                                         year=2016)
        self.assertCountEqual(books.keys(), ['en'])
        self.assertEqual(len(books['en']), 1)

    def test_one_lang_plus_default(self):
        books = self.ba.sort_by_language(languages=['en'],
                                         other=True,
                                         year=2016)
        self.assertCountEqual(books.keys(), ['en', 'default'])
        self.assertEqual(len(books['en']), 1)
        self.assertEqual(len(books['default']), 2)

    def test_missing_lang_plus_default(self):
        books = self.ba.sort_by_language(languages=['de'],
                                         other=True,
                                         year=2015)
        self.assertCountEqual(books.keys(), ['de', 'default'])
        self.assertEqual(len(books['de']), 0)
        self.assertEqual(len(books['default']), 2)

    def test_no_book_that_year(self):
        books = self.ba.sort_by_language(languages=['en'],
                                         other=True,
                                         year=2014)
        self.assertCountEqual(books.keys(), ['en', 'default'])
        self.assertEqual(len(books['en']), 0)
        self.assertEqual(len(books['default']), 0)

    def test_no_book_in_that_lang_that_year(self):
        books = self.ba.sort_by_language(languages=['en'],
                                         year=2015)
        self.assertCountEqual(books.keys(), ['en'])
        self.assertEqual(len(books['en']), 0)
