from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

class DashboardView(View):
    ...

@method_decorator(login_required, name='dispatch')
class DashboardHomeView(TemplateView):
    template_name = 'dashboard/home.html'