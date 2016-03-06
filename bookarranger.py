class BookArranger():

    def __init__(self, books):
        self.books = books

    # Can't get the language via the API so using shelf names instead of
    # languages for now.
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
