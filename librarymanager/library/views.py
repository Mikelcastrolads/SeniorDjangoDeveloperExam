from django.utils import timezone
from pyexpat.errors import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book, Author, Genre, Borrow
from .forms import BookForm, AuthorForm, GenreForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# user registration
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# authenticator
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class LibrarianOrAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='Librarians').exists()

def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

# books
class BookListView(ListView):
    model = Book
    template_name = 'library/books/books.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        genre_filter = self.request.GET.get('genre', '')
        status_filter = self.request.GET.get('status', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(author__name__icontains=search_query) |
                Q(genre__name__icontains=search_query)
            )
        
        if genre_filter:
            queryset = queryset.filter(genre__genre_id=genre_filter)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = Genre.objects.all() 
        context['status'] = Book.STATUS 
        return context
    
class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'library/books/book_info.html'
    context_object_name = 'book'

    def get_object(self): 
        return super().get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['can_edit'] = self.request.user.is_superuser or self.request.user.groups.filter(name='Librarians').exists()
        context['can_borrow'] = self.object.status == 'available'
        context['can_return'] = self.object.status == 'borrowed'
        return context
    
class BookCreateView(LibrarianOrAdminMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'library/books/add_books.html'
    success_url = reverse_lazy('book_list')

class BookUpdateView(LibrarianOrAdminMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'library/books/edit_books.html'
    success_url = reverse_lazy('book_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Book, book_id=self.kwargs['pk'])
    
class BorrowBookView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self): 
        return self.request.user.is_authenticated

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, book_id=kwargs['pk'])
        if book.status == 'available':
            book.status = 'borrowed'
            book.save()
            Borrow.objects.create(user=request.user, book=book)
        return redirect('book_list')

class ReturnBookView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self): 
        return self.request.user.is_authenticated

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, book_id=kwargs['pk'])
        try:
            borrowing = Borrow.objects.get(book=book, user=request.user, returned_at__isnull=True)
            borrowing.returned_at = timezone.now()
            borrowing.save()
            book.status = 'available'
            book.save()
        except Borrow.DoesNotExist:
            # Optionally handle the case where the user did not borrow the book
            pass
        return redirect('book_list')

class BookDeleteView(LibrarianOrAdminMixin, DeleteView):
    model = Book
    template_name = 'library/books/delete_books.html'
    success_url = reverse_lazy('book_list')

# author
class AuthorListView(ListView):
    model = Author
    context_object_name = 'authors'
    template_name = 'library/author/authors.html'
    paginate_by = 10

class AuthorDetailView(DetailView):
    model = Author
    context_object_name = 'author'
    template_name = 'library/author/author_info.html'

class AuthorCreateView(LibrarianOrAdminMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'library/author/add_author.html'
    success_url = reverse_lazy('author_list')

class AuthorUpdateView(LibrarianOrAdminMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'library/author/edit_author.html'
    success_url = reverse_lazy('author_list')

class AuthorDeleteView(LibrarianOrAdminMixin, DeleteView):
    model = Author
    template_name = 'library/author/delete_author.html'
    success_url = reverse_lazy('author_list')

# genre
class GenreListView(ListView):
    model = Genre
    context_object_name = 'genres'
    template_name = 'library/genre/genres.html'
    paginate_by = 10

class GenreDetailView(DetailView):
    model = Genre
    context_object_name = 'genre'
    template_name = 'library/genre/genre_info.html'

class GenreCreateView(LibrarianOrAdminMixin, CreateView):
    model = Genre
    form_class = GenreForm
    template_name = 'library/genre/add_genre.html'
    success_url = reverse_lazy('genre_list')

class GenreUpdateView(LibrarianOrAdminMixin, UpdateView):
    model = Genre
    form_class = GenreForm
    template_name = 'library/genre/edit_genre.html'
    success_url = reverse_lazy('genre_list')

class GenreDeleteView(LibrarianOrAdminMixin, DeleteView):
    model = Genre
    template_name = 'library/genre/delete_genre.html'
    success_url = reverse_lazy('genre_list')
     