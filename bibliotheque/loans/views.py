from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from accounts.utils import is_bibliothecaire

from .forms import LoanCreateForm, LoanReturnForm
from .models import Loan


@login_required
def loan_list(request):
    if is_bibliothecaire(request.user):
        loans = Loan.objects.select_related('book', 'reader').all()
    else:
        loans = Loan.objects.select_related('book', 'reader').filter(reader=request.user)
    return render(request, 'loans/loan_list.html', {'loans': loans})


@login_required
@user_passes_test(is_bibliothecaire)
def loan_create(request):
    form = LoanCreateForm(request.POST or None)
    if form.is_valid():
        loan = form.save()
        book = loan.book
        book.available_copies -= 1
        book.save(update_fields=['available_copies'])
        messages.success(request, 'Emprunt enregistré avec succès.')
        return redirect('loans:loan-list')
    return render(request, 'loans/loan_form.html', {'form': form})


@login_required
@user_passes_test(is_bibliothecaire)
def loan_return(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    form = LoanReturnForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        loan.mark_returned()
        messages.success(request, 'Retour validé.')
        return redirect('loans:loan-list')
    return render(request, 'loans/loan_return.html', {'loan': loan, 'form': form})
