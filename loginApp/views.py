from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm

#Imports for Email
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request, 'homepage.html')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account created for: ' + user)
                return redirect('login')

        context={'form': form}
        return render(request, 'register.html', context)


def loginPage(request):
    if request.user.is_authenticated: return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')

            else: messages.info(request, 'Username of Password is Incorrect!')
        
        context={}
        return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def sendEmail(request):
    template = render_to_string('email_template.html',{'name':request.user})

    user_email = request.user.email

    email = EmailMessage(
        'Tickets Confirmation Email',
        template,
        settings.EMAIL_HOST_USER,
        [user_email],
    )

    email.fail_silently = False
    email.send()

    return redirect('home')
