# Update Operation

from bookshelf.models import Book

# Update the book title
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Verify update
Book.objects.get(id=book.id)

# Expected Output:
# <Book: Nineteen Eighty-Four by George Orwell (1949)>
