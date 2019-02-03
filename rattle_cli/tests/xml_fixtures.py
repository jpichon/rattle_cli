#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, timezone


class GoodreadsXMLFactory():

    date_format = '%a %b %d %H:%M:%S %z %Y'
    goodreads_tz = timezone(offset=timedelta(hours=-8))

    main_tag = """<?xml version="1.0" encoding="UTF-8"?>
<GoodreadsResponse>
  <Request/>
  <reviews start="{review_start_cnt}" end="{review_end_cnt}" total="{review_total_cnt}">
  {reviews}
</reviews>
</GoodreadsResponse>"""  # noqa

    review_tag = """
<review>
  <id>1234567890</id>
  <book>{book}</book>
  <shelves>{shelves}</shelves>
  <read_at>{read_at}</read_at>
  <body>
      <![CDATA[面白かったです。]]>
  </body>
</review>"""

    book_tag = """
  <id type="integer">123456</id>
  <isbn>0000000000</isbn>
  <title>{title}</title>
  <authors>{authors}</authors>"""

    author_tag = """
<author>
  <id>12345</id>
  <name>{author_name}</name>
</author>"""

    shelf_tag = """
    <shelf name="{shelf_name}" exclusive="false" review_shelf_id="1237" />"""

    def create_full_xml_response(self, reviews=1, authors=1, d=None, shelves=1,
                                 start_cnt=1, end_cnt=None):
        total_cnt = reviews

        if end_cnt is None:
            end_cnt = reviews
        else:
            reviews = end_cnt - start_cnt + 1

        response = ""
        for n in range(0, reviews):
            response += self.create_review(n, authors, d, shelves)

        details = {'reviews': response,
                   'review_end_cnt': end_cnt,
                   'review_start_cnt': start_cnt,
                   'review_total_cnt': total_cnt}

        return self.main_tag.format_map(details)

    def create_review(self, num=1, authors=1, d=None, shelves=1):
        authors = self.create_authors(authors)
        book = self.create_book("Wonderful Book Title %d" % num,
                                authors)
        read_at = self.create_read_at_date(d)
        shelves = self.create_shelves(shelves)

        review = self.review_tag.format_map({'book': book,
                                             'shelves': shelves,
                                             'read_at': read_at})

        return review

    def create_book(self, title, authors):
        details = {'title': title,
                   'authors': authors}
        return self.book_tag.format_map(details)

    def create_authors(self, num=1):
        authors = ""
        name = "Author #%s"

        for n in range(0, num):
            details = {'author_name': name % n}
            authors += self.author_tag.format_map(details)

        return authors

    def create_read_at_date(self, d=None):
        if d is None:
            d = datetime.now(tz=self.goodreads_tz)
        read_at = datetime.strftime(d, self.date_format)
        return read_at

    def create_shelves(self, num=1):
        shelves = ""
        name = "Self #%s"

        for n in range(0, num):
            details = {'shelf_name': name % n}
            shelves += self.shelf_tag.format_map(details)

        return shelves
