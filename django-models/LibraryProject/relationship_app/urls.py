from django.urls import path
from . import views
from .views import LibraryDetailView

urlpatterns = [
    path('books/', views.books, name='books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail')
]
