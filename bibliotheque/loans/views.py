from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from accounts.utils import is_bibliothecaire

from .forms import LoanCreateForm, LoanFilterForm, LoanReturnForm
from .models import Loan


@login_required
def loan_list(request):
    is_librarian = is_bibliothecaire(request.user)
    if is_librarian:
        loans = Loan.objects.select_related('book', 'reader').all()
    else:
        loans = Loan.objects.select_related('book', 'reader').filter(reader=request.user)

    filter_form = LoanFilterForm(request.GET or None)
    if filter_form.is_valid():
        reader = filter_form.cleaned_data.get('reader')
        if is_librarian and reader:
            loans = loans.filter(reader=reader)

        book_title = filter_form.cleaned_data.get('book_title')
        if book_title:
            loans = loans.filter(book__title__icontains=book_title)

        loan_date = filter_form.cleaned_data.get('loan_date')
        if loan_date:
            loans = loans.filter(loan_date=loan_date)

        return_date = filter_form.cleaned_data.get('return_date')
        if return_date:
            loans = loans.filter(return_date=return_date)

        status = filter_form.cleaned_data.get('status')
        if status:
            loans = loans.filter(status=status)

    paginator = Paginator(loans, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)

    return render(
        request,
        'loans/loan_list.html',
        {'loans': page_obj, 'page_obj': page_obj, 'filter_form': filter_form, 'query_string': query_params.urlencode()},
    )


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
