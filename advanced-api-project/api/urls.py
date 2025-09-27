from django.urls import path
from .views import BookCreateView, BookListView, BookDetailView, BookUpdateView, BookDeleteView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-view'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/detail/', BookUpdateView.as_view(), name='book-detail'),
    path('books/<int:pk>/delete', BookDeleteView.as_view(), name='book-delete'),
]