from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth_login, logout
# from django.contrib import messages
from .models import Account, Tokens
from .forms import RegistrationForm, PasswordChangeForm
from examination.models import *

UserModel = get_user_model()

# Create your views here.
def RegistrationView(request):
    form = RegistrationForm()
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                #this part of code is for referal validation
                tokenID=request.POST['token_inp']
                try:
                    TOKEN=Tokens.objects.get(token=tokenID, active=False)
                except:
                    # print("in except")
                    # messages.success(request,"Invalid Token")
                    return render(request, 'registration/register.html', {'form': form})
                
                password = form.cleaned_data['password1']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                user = Account(email=email, first_name=first_name, token=TOKEN)
                user.set_password(password)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string("Verification/account_verification.html", {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                print("HERE!")
                
                # auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('/', {'message': 'Verfiy your email to complete sign up process.'})
            else:
                return render(request, 'registration/register.html', {'form': form})
        else:
            form = RegistrationForm()
            return render(request, 'registration/register.html', {'form': form})

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'registration/index.html')
    else:
        givenTests = UserTests.objects.filter(user=request.user)
        pendingTests = Test.objects.exclude(usertests__user=request.user)
        score_labels = []
        score_values = []
        for g in givenTests:
            score_labels.append(g.test.test_name)
            score_values.append((g.calculate_score/g.total_questions)*100)
        context = {
            'given_tests': givenTests,
            'pending_tests': pendingTests,
            'score_labels': score_labels,
            'score_values': score_values,
        }
        return render(request, 'dashboard.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def forgot_password(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            pass
        else:
            return render(request, 'registration/forgot_password.html')

def reset_password(request):
    if not request.user.is_authenticated:
        return redirect('/')
    isWrong=False
    error=''
    form=PasswordChangeForm()
    if request.method=='POST':
        form=PasswordChangeForm(request.POST)
        if form.is_valid():
            previous_password=request.POST['previous_password']
            password1=request.POST['password1']
            password2=request.POST['password2']
            if not request.user.check_password(previous_password):
                isWrong = True
                error = "This is not your previous password"
                context = {'form': form, 'isWrong': isWrong, 'error': error}
                return render(request, 'registration/reset_password.html', context)
            if password1!=password2:
                isWrong=True
                error="Passwords don't match"
                context = {'form': form, 'isWrong': isWrong, 'error': error}
                return render(request, 'registration/reset_password.html', context)
            if request.user.check_password(password1):
                isWrong = True
                error = "This is your old password"
                context = {'form': form, 'isWrong': isWrong, 'error': error}
                return render(request, 'registration/reset_password.html', context)
            request.user.set_password(password1)
            request.user.save()
            auth_login(request, request.user)
            return redirect('/login')
    context={'form':form, 'isWrong':isWrong, 'error':error}
    return render(request, 'registration/reset_password.html', context)