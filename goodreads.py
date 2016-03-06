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

        self.initialise_user()

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
            logging.exception(msg, url, response.status_code)
            logging.debug(response.text)
            exit(msg % (url, response.status_code))

    def retrieve_reviews(self, page=1):
        data = {'id': self.user_id,
                'v': '2',
                'page': page,
                'shelf': 'read',
                'sort': 'date_read'}

        url = 'https://www.goodreads.com/review/list/%s.xml' % self.user_id
        response = self.session.post(url, data)
        logging.info("Getting reviews (%s, page %s): %s",
                     url, page, response.status_code)
        return xmltodict.parse(response.content)[self.main_tag]['reviews']

    def get_books(self):
        page, end, total = 0, 0, 1

        while end < total:
            page += 1
            reviews = self.retrieve_reviews(page)
            end = int(reviews['@end'])
            total = int(reviews['@total'])

            for review in reviews['review']:
                title = review['book']['title']
                try:
                    date_read = datetime.strptime(review['read_at'],
                                                  self.date_format)
                except:
                    date_read = review['read_at']
                    logging.debug("Failed to parse date %s for book %s",
                                  date_read, title)

                if type(review['book']['authors']['author']) == list:
                    authors = [a['name']
                               for a in review['book']['authors']['author']]
                    author = ', '.join(authors)
                else:
                    author = review['book']['authors']['author']['name']

                if type(review['shelves']['shelf']) == list:
                    shelves = [shelf['@name']
                               for shelf in review['shelves']['shelf']]
                else:
                    shelves = [review['shelves']['shelf']['@name']]

                book = Book(title, author, date_read, shelves)
                self.books.append(book)

        return self.books


class Book():

    def __init__(self, title, author, date_read=None, shelves=None):
        self.title = title
        self.author = author
        self.date_read = date_read
        if shelves is None:
            self.shelves = []

    def __repr__(self):
        return "Book(%s, by %s)" % (self.title, self.author)
