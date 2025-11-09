# relationship_app/query_samples.py
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Create sample data for testing relationships"""
    # Clear existing data
    Author.objects.all().delete()
    Book.objects.all().delete()
    Library.objects.all().delete()
    Librarian.objects.all().delete()
    
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    book3 = Book.objects.create(title="1984", author=author2)
    book4 = Book.objects.create(title="Animal Farm", author=author2)
    
    # Create libraries
    library1 = Library.objects.create(name="Central Library")
    library2 = Library.objects.create(name="City Public Library")
    
    # Add books to libraries
    library1.books.add(book1, book2, book3)
    library2.books.add(book3, book4)
    
    # Create librarians
    librarian1 = Librarian.objects.create(name="Alice Johnson", library=library1)
    librarian2 = Librarian.objects.create(name="Bob Smith", library=library2)
    
    return author1, library1, librarian1

def demonstrate_relationships():
    """Demonstrate all the required relationship queries"""
    
    # Create sample data first
    author1, library1, librarian1 = create_sample_data()
    
    # 1. Query all books by a specific author
    print("1. QUERY ALL BOOKS BY A SPECIFIC AUTHOR:")
    books_by_author = Book.objects.filter(author=author1)
    for book in books_by_author:
        print(f"  - {book.title}")
    
    # 2. List all books in a library
    print("\n2. LIST ALL BOOKS IN A LIBRARY:")
    books_in_library = library1.books.all()
    for book in books_in_library:
        print(f"  - {book.title} (by {book.author.name})")
    
    # 3. Retrieve the librarian for a library
    print("\n3. RETRIEVE THE LIBRARIAN FOR A LIBRARY:")
    try:
        librarian = library1.librarian
        print(f"Librarian for {library1.name}: {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian found for {library1.name}")

if __name__ == "__main__":
    demonstrate_relationships()