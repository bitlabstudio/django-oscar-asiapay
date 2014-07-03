from django.views import generic
from django.conf import settings

from asiapay.paydollar import models


class TransactionListView(generic.ListView):
    model = models.PaydollarTransaction
    template_name = 'asiapay/paydollar/dashboard/transaction_list.html'
    context_object_name = 'transactions'


class TransactionDetailView(generic.DetailView):
    model = models.PaydollarTransaction
    template_name = 'asiapay/paydollar/dashboard/transaction_detail.html'
    context_object_name = 'txn'

    def get_context_data(self, **kwargs):
        ctx = super(TransactionDetailView, self).get_context_data(**kwargs)
        ctx['show_form_buttons'] = True
        return ctx
