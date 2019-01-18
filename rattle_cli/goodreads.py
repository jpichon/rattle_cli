from datetime import datetime
import logging

import xmltodict


class Goodreads():

    main_tag = 'GoodreadsResponse'
    date_format = '%a %b %d %H:%M:%S %z %Y'

    def __init__(self, session):
        self.logger = logging.getLogger('goodreads')
        self.session = session
        self.user = None
        self.user_id = None
        self.books = []

    def initialise_user(self):
        self.user = self.get_authenticated_user()
        try:
            self.user_id = self.user['@id']
        except KeyError:
            msg = "Couldn't get the user ID from the OAuth session."
            self.logger.exception(msg)
            exit(msg)

    def get_authenticated_user(self):
        url = "https://www.goodreads.com/api/auth_user"
        self.logger.info("Getting user info at %s" % url)

        response = self.session.get(url)
        try:
            return xmltodict.parse(response.content)[self.main_tag]['user']
        except Exception:
            msg = "Couldn't get the user info (%s). Status code: %s"
            self.logger.exception(msg, url, response.status_code)
            exit(msg % (url, response.status_code))

    def retrieve_reviews(self, shelf, page=1):
        data = {'id': self.user_id,
                'v': '2',
                'page': page,
                'shelf': shelf,
                'sort': 'date_read'}

        url = 'https://www.goodreads.com/review/list/%s.xml' % self.user_id
        response = self.session.post(url, data)
        self.logger.info("Getting reviews (%s, page %s): %s",
                         url, page, response.status_code)
        return xmltodict.parse(response.content)[self.main_tag]['reviews']

    def get_books(self, shelf):
        page, end, total = 0, 0, 1

        while end < total:
            page += 1
            reviews = self.retrieve_reviews(shelf, page)
            end = int(reviews['@end'])
            total = int(reviews['@total'])
            self.logger.debug("Parsing page %s (until review #%s, total %s)",
                              page, end, total)

            # Make sure the reviews are iterable, even if only one is returned
            if type(reviews['review']) == list:
                reviews = reviews['review']
            else:
                reviews = [reviews['review']]

            for review in reviews:
                self.logger.debug("Parsing review %s", review['id'])
                title = review['book']['title']
                date_read = self.parse_date_read(review, title)
                author = self.parse_author(review)
                shelves = self.parse_shelves(review)

                book = Book(title, author, date_read, shelves)
                self.books.append(book)

        return self.books

    def parse_date_read(self, review, title):
        try:
            date_read = datetime.strptime(review['read_at'],
                                          self.date_format)

        except KeyError:
            date_read = ""
            self.logger.info("Date read is missing (review %s for %s)",
                             review['id'], title)
        except ValueError:
            date_read = review['read_at']
            self.logger.debug("Failed to parse date %s (review %s for %s)",
                              date_read, review['id'], title)
        except Exception:
            date_read = ""
            self.logger.exception("Failed to parse date for review %s (%s)",
                                  review['id'], title)

        # We're only looking at the 'read' shelf so everything in here should
        # have been read. If there is no date, it could be that the user didn't
        # give the book a rating or review. Let's try to use the updated date
        # instead.
        if date_read == "":
            try:
                date_read = datetime.strptime(review['date_updated'],
                                              self.date_format)
                self.logger.info(
                    "Using 'date updated' as backup for 'date read' "
                    "for %s (%s)", title, date_read
                )
            except ValueError:
                self.logger.exception(
                    "Failed to parse 'date_updated' date (%s) for review "
                    "%s (%s)", review['date_updated'], review['id'], title
                )

        return date_read

    def parse_author(self, review):
        try:
            if type(review['book']['authors']['author']) == list:
                authors = [a['name']
                           for a in review['book']['authors']['author']]
                author = ', '.join(authors)
            else:
                author = review['book']['authors']['author']['name']
        except Exception:
            author = ""
            self.logger.exception("Failed to parse author(s) for review %s",
                                  review['id'])
        return author

    def parse_shelves(self, review):
        try:
            if type(review['shelves']['shelf']) == list:
                shelves = [shelf['@name']
                           for shelf in review['shelves']['shelf']]
            else:
                shelves = [review['shelves']['shelf']['@name']]
        except Exception:
            shelves = []
            self.logger.exception("Failed to parse shelves for review %s",
                                  review['id'])
        return shelves


class Book():

    def __init__(self, title, author, date_read=None, shelves=None):
        self.title = title
        self.author = author
        self.date_read = date_read
        if shelves is None:
            self.shelves = []
        else:
            self.shelves = shelves

    def __repr__(self):
        return "Book(%s, by %s)" % (self.title, self.author)
