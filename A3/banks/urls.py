from django.urls import path
from banks.views import AddFormView, AddBranchView, BankListView, BankDetailView, BranchDetailView, \
    AllBranchesDetailView


app_names = 'banks'

urlpatterns = [
    path('add/', AddFormView.as_view(), name='add'),
    path('<pk>/branches/add/', AddBranchView.as_view(), name='branches_add'),
    path('all/', BankListView.as_view(), name='all'),
    path('<pk>/details/', BankDetailView.as_view(), name='bank_details'),
    path('branch/<pk>/details/', BranchDetailView.as_view(), name='branch_details'),
    path('<pk>/branches/all/', AllBranchesDetailView.as_view(), name='branches_details')
]
