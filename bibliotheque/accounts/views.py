from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import ReaderSignupForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('books:book-list')

    if request.method == 'POST':
        form = ReaderSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Compte lecteur créé avec succès.')
            return redirect('books:book-list')
    else:
        form = ReaderSignupForm()

    return render(request, 'accounts/signup.html', {'form': form})
