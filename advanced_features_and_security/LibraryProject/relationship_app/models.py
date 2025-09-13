from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager


# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("can_add_book", "Can add a book"),
            ("can_change_book", "Can change a book"),
            ("can_delete_book", "Can delete a book"),
        ]
        

    def __str__(self):
        return f'{self.title}, {self.author}'




class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return f'{self.name}, {self.books}'

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}, {self.library}'
    

class UserProfile(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'Admin', 'Admin'
        LIBRARIAN = 'librarian', 'librarian'
        MEMBER = 'Member', 'Member'
        
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        choices=Role.choices
        # default=Role.MEMBER
    )

    def __str__(self):
        return f'{self.user}, {self.role}'



class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have email address.')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)




class CustomUser(AbstractUser):
    date_of_birth = models.DateField()
    profile_photo = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username


