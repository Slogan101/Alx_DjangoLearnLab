from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, CommentForm, PostForm
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from taggit.models import Tag
from .models import Post, Comment
from django.urls import reverse_lazy
from taggit.forms import TagWidget

# Create your views here.

def home(request):
    return render(request, 'blog/home.html')


# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#         else:
#             print(form.errors)
#     else:
#         form = UserRegistrationForm()

#     return render (request, 'blog/register.html', {'form': form})

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'blog/register.html'


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile Updated")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, "blog/profile.html", context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    # paginate_by = 2

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'tags']
    widgets = {
            'tags': TagWidget(attrs={'class': 'form-control'}),
        }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
# SECTION VIEWS FOR COMMENTS

# @login_required
# def add_comment(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.author = request.user
#             comment.save()
#             return redirect('post-detail', pk=post.id)
#     else:
#         form = CommentForm()
#     return render(request, 'blog/post_detail.html', {'form': form, 'post': post})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/post_detail.html'  # or use your template

    def form_valid(self, form):
        # Attach author and post to the comment before saving
        form.instance.author = self.request.user
        post_id = self.kwargs.get('post_id')
        form.instance.post = get_object_or_404(Post, id=post_id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs.get('post_id')})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass post so template has it
        context['post'] = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return context






# @login_required
# def edit_comment(request, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id, author=request.user)
#     if request.method == 'POST':
#         form = CommentForm(request.POST, instance=comment)
#         if form.is_valid():
#             form.save()
#             return redirect('post-detail', pk=comment.post.id)
#     else:
#         form = CommentForm(instance=comment)
#     return render(request, 'blog/edit_comment.html', {'form': form, 'comment': comment})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/edit_comment.html'

    def test_func(self):
        # Only comment author can update
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.id})



# @login_required
# def delete_comment(request, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id, author=request.user)
#     post_id = comment.post.id
#     if request.method == 'POST':
#         comment.delete()
#         return redirect('post-detail', pk=post_id)
#     return render(request, 'blog/delete_comment.html', {'comment': comment})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/delete_comment.html'

    def test_func(self):
        # Only comment author can delete
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.id})
    

def search_posts(request):
    query = request.GET.get('q')
    results = Post.objects.all()

    if query:
        results = results.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    return render(request, 'blog/search_results.html', {'posts': results, 'query': query})


def posts_by_tag(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    posts = Post.objects.filter(tags=tag)

    return render(request, 'blog/tag_posts.html', {'tag': tag, 'posts': posts})