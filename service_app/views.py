from django.shortcuts import render
from django.views import View


# Create your views here.


class MainPage(View):
    def get(self, request):
        return render(request, 'main.html')


class About(View):
    def get(self, request):
        return render(request, 'about.html')
