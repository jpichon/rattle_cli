import logging

from rauth.service import OAuth1Service, OAuth1Session
import xmltodict

from goodreads import Goodreads
try:
    from secrets import api_key, api_secret, \
        access_token, access_token_secret
except:
    exit("No API key/access tokens found.")


def reopen_session(api_key, api_secret, access_token, access_token_secret):
    session = OAuth1Session(consumer_key = api_key,
                            consumer_secret = api_secret,
                            access_token = access_token,
                            access_token_secret = access_token_secret,
                           )
    return session

def main():
    log_format = '%(asctime)s - %(levelname)s:%(name)s:%(message)s'
    logging.basicConfig(filename='rattle.log', level=logging.INFO,
                        format=log_format)

    session = reopen_session(api_key, api_secret,
                             access_token, access_token_secret)

    goodreads = Goodreads(session)
    reviews = goodreads.get_reviews()


if __name__ == "__main__":
    main()
