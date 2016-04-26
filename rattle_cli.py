import argparse
import logging

from bookarranger import BookArranger
from goodreads import Goodreads
from goodreads_session import GoodreadsSession
try:
    from secrets import api_key, api_secret
except:
    exit("No API key/secret found.")


def retrieve_and_sort_books(languages=None, other=False, other_label='default',
                            year=None, details=False):
    session = GoodreadsSession(api_key, api_secret)
    goodreads = Goodreads(session)
    goodreads.initialise_user()

    books = goodreads.get_books()
    arranger = BookArranger(books)

    sorted_books = arranger.sort_by_language(languages, other, other_label,
                                             year)
    arranger.print_sorted_books_nicely(sorted_books, details)


def main():
    log_format = '%(asctime)s - %(levelname)s:%(name)s:%(message)s'
    logging.basicConfig(filename='rattle.log',
                        filemode='w',
                        level=logging.WARNING,
                        format=log_format)

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Show simple reading stats per language shelf, based on your Goodreads \
reviews.""",
        epilog="""
For example, if you have a shelf named 'fr' to track your reading in French
and another named 'sp' to track your reading in Spanish, you could do the
following:

   $ python %(prog)s --lang fr sp --year 2016
   Books read based on Goodreads reviews
   fr: 7
   sp: 4

Additionally, if you don't put books in English on a specific shelf because
it's your default language, you could add the following arguments to include
them in the final count regardless:

  $ python %(prog)s --lang fr sp --year 2016 --other --other-label en
   Books read based on Goodreads reviews
   en: 18
   fr: 7
   sp: 4
""")

    parser.add_argument("--lang", "--languages",
                        help="Space-separated shelf name(s) matching the \
                        languages to compile stats on",
                        nargs="*")
    parser.add_argument("--other", "--include-other",
                        help="If a book isn't associated with any of the \
                        shelves/languages given in --lang, include it in a \
                        separate list",
                        action="store_true")
    parser.add_argument("--other-label", default="default",
                        help="If --other is set, what to call this new list \
                        (e.g. if your default language is English and you \
                        never set a shelf for it, you could call it 'en'")
    parser.add_argument("--year", type=int,
                        help="Which year to calculate the stats for. Defaults \
                        to all books ever read on Goodreads")
    parser.add_argument("--details",
                        help="Also show the book details for each language",
                        action="store_true")
    args = parser.parse_args()

    retrieve_and_sort_books(languages=args.lang,
                            other=args.other,
                            other_label=args.other_label,
                            year=args.year,
                            details=args.details)


if __name__ == "__main__":
    main()
