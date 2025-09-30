from django.urls import path
from .views import RegisterView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from . import views
from django.contrib.auth import views as auth_views











urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="blog/logout.html"), name="logout"),
    path('profile/', views.profile, name='profile'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-confirm-delete'),
]