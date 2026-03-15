import csv
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import UserProfile
from accounts.utils import is_bibliothecaire
from books.models import Book, Category

from .forms import LoanCreateForm, LoanFilterForm, LoanReturnForm
from .models import Loan


def _apply_loan_filters(loans, filter_form, is_librarian):
    if not filter_form.is_valid():
        return loans

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

    overdue_only = filter_form.cleaned_data.get('overdue_only')
    if overdue_only:
        today = date.today()
        loans = loans.filter(status=Loan.STATUS_EN_COURS, due_date__lt=today)

    return loans


@login_required
def loan_list(request):
    is_librarian = is_bibliothecaire(request.user)
    if is_librarian:
        loans = Loan.objects.select_related('book', 'reader').all()
    else:
        loans = Loan.objects.select_related('book', 'reader').filter(reader=request.user)

    filter_form = LoanFilterForm(request.GET or None)
    loans = _apply_loan_filters(loans, filter_form, is_librarian)

    paginator = Paginator(loans, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)

    return render(
        request,
        'loans/loan_list.html',
        {
            'loans': page_obj,
            'page_obj': page_obj,
            'filter_form': filter_form,
            'query_string': query_params.urlencode(),
            'today': date.today(),
        },
    )


@login_required
@user_passes_test(is_bibliothecaire)
def dashboard(request):
    today = date.today()
    active_loans = Loan.objects.filter(status=Loan.STATUS_EN_COURS)
    overdue_count = active_loans.filter(due_date__lt=today).count()
    top_books = (
        Book.objects.annotate(total_loans=Count('loans'))
        .filter(total_loans__gt=0)
        .order_by('-total_loans', 'title')[:5]
    )
    recent_loans = Loan.objects.select_related('book', 'reader').order_by('-loan_date')[:10]

    context = {
        'stats': {
            'books': Book.objects.count(),
            'categories': Category.objects.count(),
            'readers': UserProfile.objects.filter(role=UserProfile.ROLE_LECTEUR).count(),
            'active_loans': active_loans.count(),
            'returned_loans': Loan.objects.filter(status=Loan.STATUS_RETOURNE).count(),
            'overdue_loans': overdue_count,
        },
        'top_books': top_books,
        'recent_loans': recent_loans,
        'today': today,
    }
    return render(request, 'loans/dashboard.html', context)


@login_required
@user_passes_test(is_bibliothecaire)
def loan_export_csv(request):
    loans = Loan.objects.select_related('book', 'reader').all()
    filter_form = LoanFilterForm(request.GET or None)
    loans = _apply_loan_filters(loans, filter_form, True)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="emprunts.csv"'
    writer = csv.writer(response)
    writer.writerow(['Livre', 'Lecteur', 'Date emprunt', 'Date retour prévue', 'Date retour', 'Statut'])
    for loan in loans:
        writer.writerow([
            loan.book.title,
            loan.reader.username,
            loan.loan_date,
            loan.due_date,
            loan.return_date or '',
            loan.get_status_display(),
        ])
    return response


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
