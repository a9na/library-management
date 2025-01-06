from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from .forms import BookForm
from .models import CustomUser, Book, Borrow

def home(request):
    # Fetch recommended books (books marked as recommended)
    recommended_books = Book.objects.filter(is_recommended=True, available=True)

    return render(request, 'library/home.html', {
        'recommended_books': recommended_books,
    })


def book_list(request):
    # Query books that are available and unavailable
    available_books = Book.objects.filter(available=True)
    unavailable_books = Book.objects.filter(available=False)

    return render(request, 'library/book_list.html', {
        'available_books': available_books,
        'unavailable_books': unavailable_books,
    })




# Add book view (only for privileged users and admins)
def is_privileged_or_admin(user):
    return user.user_type in ['privileged', 'admin']

@user_passes_test(is_privileged_or_admin)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'library/add_book.html', {'form': form})


# Register view (assigning client role by default)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.user_type = 'client'  # Default to 'client' for new users
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'library/register.html', {'form': form})


# Login view (for all users)
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


# Logout view (for all users)
def user_logout(request):
    logout(request)
    return redirect('home')


# Admin dashboard view (only for admins)
@staff_member_required
def admin_dashboard(request):
    if request.user.user_type == 'admin':  # Only admins can access
        books = Book.objects.all()
        users = CustomUser.objects.all()
        return render(request, 'admin_dashboard.html', {'books': books, 'users': users})
    else:
        return redirect('home')  # Redirect if not admin


# Member dashboard view (displays borrowed books based on user type)
def member_dashboard(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'client':
            borrowed_books = Borrow.objects.filter(user=request.user, return_date=None)  # Not returned books
            return render(request, 'member_dashboard.html', {'borrowed_books': borrowed_books})
        
        elif request.user.user_type == 'privileged':
            borrowed_books = Borrow.objects.filter(user=request.user)
            return render(request, 'privileged_dashboard.html', {'borrowed_books': borrowed_books})
        
        elif request.user.user_type == 'admin':
            borrowed_books = Borrow.objects.all()  # Admin can see all borrowed books
            return render(request, 'admin_member_dashboard.html', {'borrowed_books': borrowed_books})
    else:
        return redirect('login')  # Redirect to login page if not authenticated

def borrow_book(request, book_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not logged in

    book = get_object_or_404(Book, id=book_id)
    
    if book.available:
        Borrow.objects.create(user=request.user, book=book)
        book.available = False  # Mark the book as unavailable
        book.save()
        return redirect('book_list')  # Redirect back to the available books list
    else:
        return render(request, 'library/book_list.html', {'error': 'Book is already borrowed'})



# Returning a book (client can return borrowed books)
def return_book(request, borrow_id):
    borrow = Borrow.objects.get(id=borrow_id)
    if borrow.user == request.user:  # Ensure the borrow record belongs to the logged-in user
        borrow.return_date = request.POST.get('return_date')  # Set return date
        borrow.book.available = True  # Mark the book as available
        borrow.book.save()
        borrow.save()
        return redirect('member_dashboard')
    else:
        return redirect('home')  # Redirect if invalid access


def book_detail(request, id):
    # Fetch the book by ID
    book = get_object_or_404(Book, id=id)

    return render(request, 'library/book_detail.html', {'book': book})
