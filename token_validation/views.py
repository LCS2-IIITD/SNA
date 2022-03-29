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
from .models import Account, Subscription, Tokens
from .forms import RegistrationForm, PasswordChangeForm, SubscriptionForm, TokenUploadForm
from examination.models import *
import csv
import io
import sys
from django.contrib.auth.decorators import login_required, permission_required

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
                tokenID=request.POST['token_inp']
                try:
                    TOKEN = Tokens.objects.get(token=tokenID)
                except:
                    return render(request, 'registration/register.html', {'form': form, 'messages': ['The entered access code is invalid.']})
                if TOKEN.active == True:
                    return render(request, 'registration/register.html', {'form': form, 'messages': ['This access code is being used by another user.']})
                password = form.cleaned_data['password1']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                user = Account(email=email, first_name=first_name, last_name=last_name, token=TOKEN)
                user.set_password(password)
                user.is_active = True
                user.save()
                TOKEN.active=True
                TOKEN.save()
                current_site = get_current_site(request)
                mail_subject = 'Thankyou for registerigng with us. Just one last step.'
                message = render_to_string("Verification/account_verification.html", {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    subject=mail_subject, body=message, to=[to_email],
                    from_email="Social Network Analysis"
                )
                # user.email_user(mail_subject, message)
                email.send()
                # print("HERE!")
                # auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('/login', {'message': 'Verfiy your email to complete sign up process.'})
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
        pendingTests = Test.objects.filter(active=True).exclude(usertests__user=request.user)
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

def testimonial(request):
    return render(request, 'registration/testimonial.html')

def resources(request):
    return render(request, 'registration/resources.html')

def errata(request):
    return render(request, "registration/errata.html")

def classes(request):
    return render(request, "registration/class.html")

def sna_winter_22(request):
    return render(request, "registration/sna_winter_22.html")

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def forgot_password(request):
    return redirect('/password-reset')
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

def subscribe(request):
    if request.method == 'POST' and request.is_ajax():
        form=SubscriptionForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            try:
                subs = Subscription(email=email)
                subs.save()
                return JsonResponse({
                    'code': 0,
                    'msg': 'Email recorded successfully.'
                }, status=200)
            except:
                return JsonResponse({
                    'code': 2,
                    'msg': 'Email is already subscribed.'
                }, status=400)
        return JsonResponse({
            'code': 1,
            'msg': 'Form input is not valid.'
        }, status=400)
    return JsonResponse({
        'code': 1,
        'msg': 'Unsupported request method.'
    }, status=400)

@login_required
@permission_required('token_validation.can_bulk_upload')
def upload_tokens(request):
    if not request.user.is_admin:
        return redirect('/')
    if request.method == "POST":
        try:
            content = io.StringIO(request.FILES["csv"].read().decode('utf-8'))
            reader = csv.reader(content, delimiter=';')
            bulk_tokens = []
            # with io.TextIOWrapper(request.FILES["csv"], encoding="utf-8", newline='\n') as text_file:
            #     reader = csv.reader(text_file, delimiter=';')                
            for row in reader:
                bulk_tokens.append(Tokens(token=row[0], active=False))
            Tokens.objects.bulk_create(bulk_tokens)
            form = TokenUploadForm()
            payload = {"form": form, "message": "Tokens uploaded successfully!"}
            return render(
                request, "registration/add_token.html", payload
            )
        except Exception as e:
            # print(e)
            form = TokenUploadForm()
            payload = {"form": form, "message": e}
            print(e)
            return render(
                request, "registration/add_token.html", payload
            )
    form = TokenUploadForm()
    payload = {"form": form, "message": ""}
    return render(
        request, "registration/add_token.html", payload
    )