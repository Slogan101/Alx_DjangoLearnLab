from django.shortcuts import render
from .models import Book
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters import rest_framework
from rest_framework import filters
from .serializers import BookSerializer

# Create your views here.

# This view allows for retreival of all books
class BookListView(generics.ListAPIView):

    """
    List all books with support for:
    - Filtering by title, author, publication_year
    - Searching by title and author name
    - Ordering by title or publication_year
    """
    # model = Book
    # context_object_name = 'books'
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering fields
    filterset_fields = ['title', 'author', 'publication_year']

    # Search across these fields
    search_fields = ['title', 'author__name']

    # Allow ordering by these fields
    ordering_fields = ['title', 'publication_year']

    # Optional: Default ordering
    ordering = ['title']



# This view allows for the retreival of a single book
class BookDetailView(generics.RetrieveAPIView):
    # model = Book
    # context_object_name = 'book'
    # pk_url_kwarg = 'book_id'
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



# This view allows for the creation of 
class BookCreateView(generics.CreateAPIView):
    # model = Book
    # fields = ['title', 'publication_year', 'author']

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Hook: Save any extra logic here if needed
        serializer.save()



# This view allows for updating of the book
class BookUpdateView(generics.UpdateAPIView):
    # model = Book
    # fields = ['title', 'publication_year', 'author']

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)
    
    # def test_func(self):
    #     book = self.get_object()
    #     return self.request.user == book.author

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Hook for custom update behavior
        serializer.save()
    

    
class BookDeleteView(generics.DestroyAPIView):
    # model = Book
    # success_url ='/'

    # def test_func(self):
    #     book = self.get_object()
    #     return self.request.user == book.author

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]