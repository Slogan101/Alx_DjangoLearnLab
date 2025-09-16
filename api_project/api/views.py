from urllib import response
from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView


# Create your views here.

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class MyProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return response({"message": "You're authenticated!"})
    

class AdminOnlyView(APIView):
    permission_classes = [IsAdminUser]


from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Write permissions are only allowed to the owner of the object
        return obj.owner == request.user
