from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            #user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('blog:post-list')  # 회원 가입 후 홈페이지로 이동
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})