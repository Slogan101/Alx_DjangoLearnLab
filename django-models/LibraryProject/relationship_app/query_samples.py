from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author.
author = Author.objects.get(name='slogan')
book_by_author = Book.objects.filter(author=author)

# or
# book_by_author = Book.objects.filter(author__name='slogan')

# List all books in a library.
library = Library.objects.get(name='central')
books_in_library = library.books.all()


# Retrieve the librarian for a library.
library = Library.objects.get(name='central')
liberian = Librarian.objects.get(library=library)