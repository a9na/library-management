from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import PermissionDenied
from .forms import BookForm
from .models import CustomUser, Book, Borrow
from django.utils import timezone



def home(request):

    recommended_books = Book.objects.filter(is_recommended=True)

    recommended_books = recommended_books.exclude(borrow__returned=False)

    print(f"User: {request.user}, User Type: {getattr(request.user, 'user_type', 'Not set')}")  # Debug

    return render(request, 'library/home.html', {
        'recommended_books': recommended_books,
    })

    
def is_librarian_or_admin(user):
    return user.user_type in ['librarian', 'admin']

def is_librarian_or_admin(user): return user.user_type in ['librarian', 'admin'] @user_passes_test(is_librarian_or_admin) 

def add_book(request): 
    if request.method == 'POST': 
        form = BookForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('book_list') 
    else: 
        form = BookForm() 
    return render(request, 'library/add_book.html', {'form': form})


@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.available:
        borrow = Borrow(user=request.user, book=book, borrow_date=timezone.now())
        borrow.save()

        book.available = False 
        book.save()

        if request.user.user_type == 'reader':
            return redirect('reader_dashboard')
        else:
            return redirect('librarian_dashboard')
    else:
        return redirect('book_list')


    
@login_required
def return_book(request, borrow_id):
    borrow = get_object_or_404(Borrow, id=borrow_id)

    if borrow.user == request.user or request.user.user_type in ['admin', 'librarian']:
        
        borrow.return_date = timezone.now()
        borrow.returned = True  
        borrow.book.available = True
        borrow.book.save()

        borrow.save()
        
        if request.user.user_type == 'reader':
            return redirect('reader_dashboard')  
        elif request.user.user_type == 'librarian':
            return redirect('librarian_dashboard') 
        else:
            return redirect('home')  
    else:
        raise PermissionDenied



def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    
    return render(request, 'library/book_detail.html', {'book': book})



from django.db.models import Count, Q

@login_required
def book_list(request):
    books = Book.objects.all().annotate(borrowed_count=Count('borrow', filter=~Q(borrow__returned=True)))

    available_books = [book for book in books if book.borrowed_count == 0]
    unavailable_books = [book for book in books if book.borrowed_count > 0]

    if request.method == 'POST' and 'borrow_book' in request.POST:
        book_id = request.POST.get('book_id')
        book = Book.objects.get(id=book_id)

        Borrow.objects.create(user=request.user, book=book)

        book.available = False
        book.save()

        if request.user.user_type == 'reader':
            return redirect('reader_dashboard')
        else:
            return redirect('librarian_dashboard')

    return render(request, 'library/book_list.html', {
        'available_books': available_books,
        'unavailable_books': unavailable_books,
    })



def is_librarian_or_admin(user):
    return user.user_type in ['librarian', 'admin']



from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)  
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'library/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'library/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def librarian_dashboard(request):
    if request.user.user_type != 'librarian':
        raise PermissionDenied  
    borrowed_books = Borrow.objects.filter(user=request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
            return redirect('librarian_dashboard') 
    else:
        form = BookForm()

    books = Book.objects.all()

    return render(request, 'library/librarian_dashboard.html', {
        'borrowed_books': borrowed_books,
        'form': form, 
        'books': books, 
    })



@login_required
def reader_dashboard(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'reader':
            borrowed_books = Borrow.objects.filter(user=request.user, return_date=None) 
            return render(request, 'library/reader_dashboard.html', {'borrowed_books': borrowed_books})
        elif request.user.user_type == 'librarian':
            return redirect('librarian_dashboard')  
        elif request.user.user_type == 'admin':
            return redirect('admin_dashboard') 
    else:
        return redirect('login') 

