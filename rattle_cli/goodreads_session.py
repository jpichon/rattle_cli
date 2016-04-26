import logging
import os

from rauth.service import OAuth1Service
from rauth.session import OAuth1Session


class GoodreadsSession():

    session = None
    filename = '.access_token'

    def __init__(self, api_key, api_secret):
        self.logger = logging.getLogger('goodreads_session')
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = None
        self.access_token_secret = None

    def set_session(self):
        # Did we save the access tokens last time?
        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as f:
                access_token = f.readlines()
            self.access_token = access_token[0].strip()
            self.access_token_secret = access_token[1].strip()
            self.reopen_session()
        else:
            # Let's get a brand new session then
            self.get_new_session()
            try:
                # Let's save these tokens for future convenience
                with open(self.filename, 'w') as f:
                    print(self.access_token, file=f)
                    print(self.access_token_secret, file=f)
            except:
                self.logger.exception("Couldn't save the token")

    def get_new_session(self):
        goodreads = OAuth1Service(
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            name='goodreads',
            request_token_url='https://www.goodreads.com/oauth/request_token',
            authorize_url='https://www.goodreads.com/oauth/authorize',
            access_token_url='https://www.goodreads.com/oauth/access_token',
            base_url='https://www.goodreads.com/'
        )

        req_token, req_token_secret = goodreads.get_request_token(
            header_auth=True)
        authorise_url = goodreads.get_authorize_url(req_token)

        print('Visit this URL in your browser: ' + authorise_url)
        accepted = 'n'
        while accepted.lower() != 'y':
            accepted = input('Have you authorized me? (y/n) ')
            session = goodreads.get_auth_session(req_token, req_token_secret)
            self.access_token = session.access_token
            self.access_token_secret = session.access_token_secret
            self.session = session

    def reopen_session(self):
        self.session = OAuth1Session(
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret)

    def get(self, *args, **kwargs):
        if self.session is None:
            self.set_session()
        return self.session.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.session is None:
            self.set_session()
        return self.session.post(*args, **kwargs)
