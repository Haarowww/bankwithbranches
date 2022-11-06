import datetime

from django.shortcuts import get_object_or_404
from django.views.generic import FormView, ListView, DetailView
from banks.forms import BankForm, BranchForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.template.response import TemplateResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from banks.models import Bank, Branch


# Create your views here.
class AddFormView(FormView):
    template_name = 'banks/banksadded.html'
    form_class = BankForm

    def get(self, request):
        if request.user.is_authenticated:
            form = BankForm()
            return TemplateResponse(request, 'banks/banksadded.html', {'form': form})
        else:
            return HttpResponse('HTTP 401 UNAUTHORIZED', status=401)

    def post(self, request):
        if request.user.is_authenticated:
            form = BankForm(request.POST)
            if form.is_valid():
                create_bank = form.save(commit=False)
                create_bank.owner = request.user
                create_bank.save()
                bank_id = create_bank.id
                return HttpResponseRedirect(f'/banks/{bank_id}/details/')
            else:
                return TemplateResponse(request, 'banks/banksadded.html', {'form': form})
        else:
            return HttpResponse('HTTP 401 UNAUTHORIZED', status=401)

    def form_valid(self, form):
        # Bank.objects.create(name=form.cleaned_data["name"],
        #                     swift_code=form.cleaned_data["swift_code"],
        #                     inst_num=form.cleaned_data["inst_num"],
        #                     description=form.cleaned_data["description"])
        # return HttpResponse(f'/banks/{Bank.objects.get(name=form.cleaned_data["name"]).id}/details/')
        return super().form_valid(form)


class AddBranchView(FormView):
    template_name = 'banks/branchesadded.html'
    form_class = BranchForm

    def get(self, request, pk):
        if request.user.is_authenticated:
            form = BranchForm()
            bank = get_object_or_404(Bank, pk=pk)
            if request.user.username != bank.owner.username:
                return HttpResponseForbidden("Wrong User")
            return TemplateResponse(request, self.template_name, {'form': form, 'pk': pk})
        else:
            return HttpResponse('HTTP 401 UNAUTHORIZED', status=401)

    def post(self, request, pk):
        if request.user.is_authenticated:
            bank = get_object_or_404(Bank, pk=pk)
            if request.user.id != bank.owner.id:
                return HttpResponseForbidden("Wrong User")
            else:
                form = BranchForm(request.POST)
                if form.is_valid():
                    create_branch = form.save(commit=False)
                    create_branch.last_modified = datetime.datetime.now()
                    create_branch.save()
                    bank.branches.add(create_branch)
                    bank.save()
                    branch_id = create_branch.id
                    return HttpResponseRedirect(f'/banks/branch/{branch_id}/details/')
                else:
                    return TemplateResponse(request, self.template_name, {'form': form, 'pk': pk})
        else:
            return HttpResponse('HTTP 401 UNAUTHORIZED', status=401)

    def form_valid(self, form):
        # Branch.objects.create(name=form.cleaned_data["name"],
        #                       transit_num=form.cleaned_data["transit_num"],
        #                       address=form.cleaned_data["address"],
        #                       email=form.cleaned_data["email"],
        #                       capacity=form.cleaned_data["capacity"])
        # return HttpResponse(f'/banks/branch/{Branch.objects.get(form.cleaned_data["name"]).id}/details/')
        return super().form_valid(form)


class BankListView(ListView):
    model = Bank

    def get_context_data(self, **kwargs):
        banks = super().get_context_data(**kwargs)
        return banks


class BankDetailView(DetailView):
    model = Bank

    def get(self, request, pk):
        bank = get_object_or_404(Bank, pk=pk)
        return TemplateResponse(request, 'banks/Bank_detail.html', {'bank': bank})


class BranchDetailView(DetailView):
    model = Branch

    def get(self, request, pk):
        branch = get_object_or_404(Branch, pk=pk)
        json_data = {'id': branch.id,
                     'name': branch.name,
                     'transit_num': branch.transit_num,
                     'address': branch.address,
                     'email': branch.email,
                     'capacity': branch.capacity,
                     'last_modified': branch.last_modified}
        return JsonResponse(json_data, safe=False)


class AllBranchesDetailView(DetailView):
    model = Branch

    def get(self, request, pk):
        bank = get_object_or_404(Bank, pk=pk)
        branches = bank.branches.all()
        data = []
        for branch in branches:
            data.append({'id': branch.id,
                         'name': branch.name,
                         'transit_num': branch.transit_num,
                         'address': branch.address,
                         'email': branch.email,
                         'capacity': branch.capacity,
                         'last_modified': branch.last_modified})
        return JsonResponse(data, safe=False)

