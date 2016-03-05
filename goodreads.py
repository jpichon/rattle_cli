import logging

import xmltodict

class Goodreads():

    main_tag = 'GoodreadsResponse'

    def __init__(self, session):
        self.logger = logging.getLogger('goodreads')
        self.session = session
        self.user = None
        self.user_id = None

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
            exit(msg % (url, response.status_code))

    def get_reviews(self):
        data = {'id': self.user_id,
                'v': '2',
                'shelf': 'read',
                'sort': 'date_read'}

        url = 'https://www.goodreads.com/review/list/%s.xml' % self.user_id
        response = self.session.post(url, data)

        logging.info("Getting user reviews: %s", response.status_code)
