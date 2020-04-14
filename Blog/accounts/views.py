from django.http import HttpResponse
from django.shortcuts import render,redirect
#from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#from django.contrib.auth import login
#from django.contrib.auth import logout as logout_user
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .import forms

class SignUp(CreateView):
    form_class = forms.UserSignupForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

"""
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('blog_app:post_list')
    else:
        form = UserCreationForm()
    return render(request,'accounts/signup.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('blog_app:post_list')
    else:
        form = AuthenticationForm()
    return render(request,'accounts/login.html',{'form':form})

def logout_view(request):
    logout_user(request)
    return redirect('blog_app:post_list')
"""
