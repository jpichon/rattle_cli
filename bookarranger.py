class BookArranger():

    def __init__(self, books):
        self.books = books

    # The language code is not available on the general reviews list,
    # and even on the book details page it is not always
    # present. Because of this, let's use shelf names instead of
    # language codes. This assumes only one language per book.
    def sort_by_language(self, languages=None, other=False,
                         other_label='default', year=None):
        sorted_books = {}
        if languages is None:
            languages = []
        for lang in languages:
            sorted_books[lang] = []
        if other:
            sorted_books[other_label] = []

        for book in self.books:
            if year is not None:
                if book.date_read.year != year:
                    continue

            for lang in languages:
                if lang in book.shelves:
                    sorted_books[lang].append(book)
                    break
            else:
                if other:
                    sorted_books[other_label].append(book)

        return sorted_books

    def print_sorted_books_nicely(self, books, details=False):
        print("Books read based on Goodreads reviews")

        for lang in books.keys():
            print("%s: %d" % (lang, len(books[lang])))
            if details:
                for book in books[lang]:
                    print("%s, by %s" % (book.title, book.author))
                print("")
