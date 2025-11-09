from relationship_app.models import Author, Book, Library, Librarian

# 1️⃣ Query all books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = author.books.all()  # uses related_name='books'
    return books


# 2️⃣ List all books in a specific library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    return books


# 3️⃣ Retrieve the librarian for a specific library
def get_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian  # uses related_name='librarian'


# ✅ Sample Data Setup (you can test this in shell)
if __name__ == "__main__":
    # Create sample records
    author = Author.objects.create(name="George Orwell")
    book1 = Book.objects.create(title="1984", author=author)
    book2 = Book.objects.create(title="Animal Farm", author=author)
    library = Library.objects.create(name="Central Library")
    library.books.add(book1, book2)
    librarian = Librarian.objects.create(name="John Doe", library=library)

    # Example queries
    print("Books by George Orwell:", list(get_books_by_author("George Orwell")))
    print("Books in Central Library:", list(get_books_in_library("Central Library")))
    print("Librarian for Central Library:", get_librarian_for_library("Central Library"))
