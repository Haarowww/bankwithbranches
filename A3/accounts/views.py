from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.template.response import TemplateResponse
from django.core.validators import validate_email


# Create your views here.
def register(request):
    if request.method == "GET":
        return TemplateResponse(request, 'accounts/signup.html')
    elif request.method == "POST":
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        error1, error2, error3, error4 = "", "", "", ""
        if password1 != password2:
            error2, error3 = "The two password fields didn't match", "The two password fields didn't match"
        if 0 < len(password1) < 8:
            error2 = "This password is too short. It must contain at least 8 characters"

        try:
            validate_email(email)
        except ValidationError:
            error4 = "Enter a valid email address"

        if username == "":
            error1 = "This field is required"
        if password1 == "":
            error2 = "This field is required"
        if password2 == "":
            error3 = "This field is required"

        if error1 == "" and error2 == "" and error3 == "":
            try:
                User.objects.create_user(username=username, password=password1, email=email,
                                         first_name=first_name, last_name=last_name)
            except IntegrityError:
                error1 = "A user with that username already exists"

        if error1 != "" or error2 != "" or error3 != "" or error4 != "":
            return TemplateResponse(request, 'accounts/signup.html',
                                    {'error1': error1, 'error2': error2, 'error3': error3, 'error4': error4})

        # Create a user
        return HttpResponseRedirect("/accounts/login/")
    else:
        return HttpResponseNotFound()


def loginforuser(request):
    if request.method == "GET":
        return TemplateResponse(request, 'accounts/login.html')
    elif request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        check_exist = User.objects.filter(username=username).exists()
        if check_exist:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/accounts/profile/view/")
            else:
                error = "Username or password is invalid"
                return TemplateResponse(request, 'accounts/login.html', {'error': error, 'username': username})
        else:
            error = "Username or password is invalid"
            return TemplateResponse(request, 'accounts/login.html', {'error': error, 'username': username})
    else:
        return HttpResponseNotFound()


def logoutuser(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            logout(request)
            return HttpResponseRedirect("/accounts/login/")
        else:
            return HttpResponseRedirect("/accounts/login/")
    else:
        return HttpResponseNotFound()


def view_profile(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            response = {'id': request.user.id, 'username': request.user.username, 'email': request.user.email,
                        'first_name': request.user.first_name, 'last_name': request.user.last_name}
            return JsonResponse(response, safe=False)
        else:
            return HttpResponse('HTTP 401 UNAUTHORIZED', status=401)
    else:
        return HttpResponseNotFound()


def edit_profile(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            first_name = request.user.first_name
            last_name = request.user.last_name
            email = request.user.email
            return TemplateResponse(request, 'accounts/edit.html', {'first_name': first_name, 'last_name': last_name,
                                                                    'email': email})
        else:
            return HttpResponse('HTTP 401 UNAUTHORIZED', status=401)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')

            error1, error2, error3 = "", "", ""
            if 0 < len(password1) < 8:
                error1 = "This password is too short. It must contain at least 8 characters"
            if password1 != "" and password1 != password2:
                error2 = "The two password fields didn't match"
            if email != "":
                try:
                    validate_email(email)
                except ValidationError:
                    error3 = "Enter a valid email address"

            if error1 != "" or error2 != "" or error3 != "":
                return TemplateResponse(request, 'accounts/edit.html', {'error1': error1, 'error2': error2,
                                                                        'error3': error3, 'first_name': first_name,
                                                                        'last_name': last_name, 'email': email})

            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            if len(password1) != 0:
                request.user.set_password(password1)
            request.user.save()
            login(request, request.user)
            return HttpResponseRedirect("/accounts/profile/view/")
        else:
            return HttpResponse('HTTP 401 UNAUTHORIZED', status=401)
    else:
        return HttpResponseNotFound()
