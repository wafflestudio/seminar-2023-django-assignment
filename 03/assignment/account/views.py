from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from account.models import User
from .forms import LoginForm, SignupForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('post-index')

    if request.method == "POST":
        login_form = LoginForm(request, request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            currentUser = authenticate(request, username=username, password=password)

            if currentUser:
                login(request, currentUser)
                return redirect('post-index')
            else:
                if currentUser is None:
                    login_form.add_error(username, "존재하지 않는 ID입니다.")
                elif not currentUser.check_password(password):
                    login_form.add_error(password, "잘못된 비밀번호입니다.")
                else:
                    login_form.add_error(None, "잘못된 자격증명입니다.")
                login_form = LoginForm()
    else:
        login_form = LoginForm()
    return render(request, 'account/login.html', {"form": login_form})


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('post-index')

    if request.method == "POST":
        logout(request)
        return redirect('post-index')
    else:
        return render(request, 'account/logout.html')


def signup_view(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            username = signup_form.cleaned_data["username"]
            password1 = signup_form.cleaned_data["password1"]
            password2 = signup_form.cleaned_data["password2"]
            nickname = signup_form.cleaned_data["nickname"]

            if password1 != password2:
                signup_form.add_error('password2', "비밀번호가 일치하지 않습니다")
            if User.objects.filter(username=username).exists():
                signup_form.add_error('username', "이미 사용중인 ID입니다.")
            if signup_form.errors:
                return render(request, "account/signup.html", {"form": signup_form})
            else:
                newUser = User.objects.create_user(
                    username=username,
                    password=password1,
                    nickname=nickname,
                )
                login(request, newUser)
                return redirect('post-index')
    else:
        signup_form = SignupForm()

    return render(request, 'account/signup.html', {'form': signup_form})
