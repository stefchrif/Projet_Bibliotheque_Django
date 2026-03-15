from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ReaderSignupForm


class RoleBasedLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to

        user = self.request.user
        if hasattr(user, 'profile') and user.profile.role == 'bibliothecaire':
            return reverse('loans:dashboard')
        return reverse('books:book-list')


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


def logout_view(request):
    if request.method in {'GET', 'POST'}:
        logout(request)
    return redirect('login')
