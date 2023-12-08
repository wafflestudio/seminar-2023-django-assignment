from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserForm


# Create your views here.
class LoginView(auth_views.LoginView):
    template_name = "login.html"


class LogoutView(auth_views.LogoutView):
    template_name = "logout.html"


def create(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('/auth/login/')
    else:
        form = UserForm()
    return render(request, 'create.html', {'form': form})