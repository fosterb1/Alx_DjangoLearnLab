# Retrieve Operation

from bookshelf.models import Book

# Retrieve all books
Book.objects.get()

# Expected Output:
# <QuerySet [<Book: 1984 by George Orwell (1949)>]>
