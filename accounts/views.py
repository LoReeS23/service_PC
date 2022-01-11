import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.models import User as Auth_user
from django.shortcuts import render, redirect
from service_app.forms import RegisterForm, LoginForm
from django.views import View
# Create your views here.
from service_app.models import Wallet, DayInWork


class RegisterView(View):
    def get(self, request):

        form = RegisterForm()
        return render(request, 'registerform.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            del data['password_repeat']
            new_user = Auth_user.objects.create_user(**data)
            Wallet.objects.create(money_amount=1000, user=new_user)
            DayInWork.objects.create(day=1, user=new_user, date=datetime.date.today())
            return redirect('/main/')
        return render(request, 'registerform.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'loginform.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('/main/')
        return render(request, 'loginform.html', {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/main/')