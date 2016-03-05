import logging

from rauth.service import OAuth1Service, OAuth1Session
import xmltodict

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

def get_user(session):
    url = "https://www.goodreads.com/api/auth_user"
    logging.info("Getting user info at %s" % url)

    try:
        response = session.get(url)
        return xmltodict.parse(response.content)['GoodreadsResponse']['user']
    except Exception:
        msg = "Couldn't get the user info (%s). Status code: %s"
        logging.exception(msg, url, response.status_code)
        exit(msg % (url, response.status_code))

def get_user_reviews(session, uid):
    data = {'id': uid,
            'v': '2',
            'shelf': 'read',
            'per_page': 1,
            'sort': 'date_read'}

    url = 'https://www.goodreads.com/review/list/%s.xml' % uid
    response = session.post(url, data)

    logging.info("Getting user reviews: %s", response.status_code)

def main():
    logging.basicConfig(filename='rattle.log', level=logging.INFO)

    session = reopen_session(api_key, api_secret,
                             access_token, access_token_secret)
    user = get_user(session)

    try:
        user_id = user['@id']
    except KeyError:
        exit("Couldn't get the user ID from the OAuth session.")

    get_user_reviews(session, user_id)


if __name__ == "__main__":
    main()
