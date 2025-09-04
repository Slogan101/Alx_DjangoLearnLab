from django.urls import path
from . import views
from .views import LibraryDetailView, RegisterView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('books/', views.books, name='books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
