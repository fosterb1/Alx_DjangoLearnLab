# relationship_app/query_samples.py
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Create sample data for testing relationships"""
    print("Creating sample data...")
    
    # Clear existing data
    Author.objects.all().delete()
    Book.objects.all().delete()
    Library.objects.all().delete()
    Librarian.objects.all().delete()
    
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    author3 = Author.objects.create(name="Agatha Christie")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    book3 = Book.objects.create(title="1984", author=author2)
    book4 = Book.objects.create(title="Animal Farm", author=author2)
    book5 = Book.objects.create(title="Murder on the Orient Express", author=author3)
    
    # Create libraries
    library1 = Library.objects.create(name="Central Library")
    library2 = Library.objects.create(name="City Public Library")
    
    # Add books to libraries
    library1.books.add(book1, book2, book3)
    library2.books.add(book3, book4, book5)
    
    # Create librarians
    librarian1 = Librarian.objects.create(name="Alice Johnson", library=library1)
    librarian2 = Librarian.objects.create(name="Bob Smith", library=library2)
    
    print("Sample data created successfully!")
    return author1, library1, librarian1

def demonstrate_relationships():
    """Demonstrate all the required relationship queries"""
    print("\n" + "="*50)
    print("DEMONSTRATING DJANGO MODEL RELATIONSHIPS")
    print("="*50)
    
    # Create sample data first
    author1, library1, librarian1 = create_sample_data()
    
    # 1. Query all books by a specific author
    print("\n1. QUERY ALL BOOKS BY A SPECIFIC AUTHOR:")
    print(f"Books by {author1.name}:")
    books_by_author = Book.objects.filter(author=author1)
    for book in books_by_author:
        print(f"  - {book.title}")
    
    # Alternative method using related_name
    print(f"\nUsing related_name 'books':")
    for book in author1.books.all():
        print(f"  - {book.title}")
    
    # 2. List all books in a library
    print("\n2. LIST ALL BOOKS IN A LIBRARY:")
    print(f"Books in {library1.name}:")
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
    
    # Additional relationship demonstrations
    print("\n4. ADDITIONAL RELATIONSHIP DEMONSTRATIONS:")
    
    # Many-to-Many reverse relationship: Find libraries containing a specific book
    book = Book.objects.get(title="1984")
    print(f"\nLibraries that have '1984':")
    for library in book.libraries.all():
        print(f"  - {library.name}")
    
    # ForeignKey reverse relationship: Find all authors and their books
    print(f"\nAll authors and their books:")
    for author in Author.objects.all():
        print(f"  {author.name}:")
        for book in author.books.all():
            print(f"    - {book.title}")

# Required functions for automated checks
def query_books_by_author(author_name):
    """Query all books by a specific author"""
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return Book.objects.none()

def list_books_in_library(library_name):
    """List all books in a library"""
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return Book.objects.none()

def get_librarian_for_library(library_name):
    """Retrieve the librarian for a library"""
    try:
        library = Library.objects.get(name=library_name)
        return library.librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None

if __name__ == "__main__":
    demonstrate_relationships()
    
    # Test the specific functions for automated checks
    print("\n" + "="*50)
    print("TESTING FUNCTIONS FOR AUTOMATED CHECKS")
    print("="*50)
    
    # Test query_books_by_author
    print("\nTesting: Query all books by a specific author")
    books = query_books_by_author("J.K. Rowling")
    for book in books:
        print(f"  - {book.title}")
    
    # Test list_books_in_library
    print("\nTesting: List all books in a library")
    books = list_books_in_library("Central Library")
    for book in books:
        print(f"  - {book.title}")
    
    # Test get_librarian_for_library
    print("\nTesting: Retrieve the librarian for a library")
    librarian = get_librarian_for_library("Central Library")
    if librarian:
        print(f"  - Librarian: {librarian.name}")
    else:
        print("  - No librarian found")