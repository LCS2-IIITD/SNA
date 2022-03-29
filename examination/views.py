from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from django.http import Http404
from django.db import transaction
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .models import Question, Answer, Test, UserTests, UserResponse
import datetime
from token_validation.models import Account

# Create your views here.
def givenTests(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        givenTests = UserTests.objects.filter(user=request.user)
        context = {
            'given_tests': givenTests
        }
        return render(request, 'given_test.html', context)

def pendingTests(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        pendingTests = Test.objects.filter(active=True).exclude(usertests__user=request.user)
        context = {
            'pending_tests': pendingTests
        }
        return render(request, 'pending_test.html', context)

def getTest(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        if request.method == 'GET':
            return redirect('/login')
        else:
            try:
                test_id = request.POST['test_id']
            except KeyError:
                raise Http404("Poll does not exist")
            hasUserGivenTest = UserTests.objects.filter(user=request.user, test__id=test_id)
            if (hasUserGivenTest.count() == 0):
                # User can give test
                test = Test.objects.get(pk=test_id, active=True)
                # userTest = UserTests(user = request.user, test=test)
                # userTest.save()
                if not test:
                    return redirect('/examination/pending/', {'error': 'Test is not active anymore.'})
                questions = Question.objects.filter(test__pk=test_id).order_by('?')[:test.num_questions]
                sess_ques_set = {}
                ques_answer_map = []
                for ques in questions:
                    ques_answer_map.append({
                        'id': ques.id,
                        'html': ques.question,
                        'topic': ques.topic.name,
                        'answer': ques.answer.all().order_by('?')
                    })
                    sess_ques_set[ques.id] = True
                request.session['ques_set'] = sess_ques_set
                request.session['test_id'] = test.id
                request.session['timestamp'] = datetime.datetime.now().isoformat()
                # print(ques_answer_map)
                userTest = UserTests(user = request.user, test=Test.objects.filter(pk=int(request.POST['test_id']))[0])
                userTest.save()
                return render(request, 'test.html', {'ques_map': ques_answer_map, 'test': test,})
            else:
                # if (test_id == request.session.get('test_id', "_")):
                #     test = Test.objects.filter(pk=test_id)[0]

                #     return render(request, 'test.html', {'ques_map': ques_answer_map, 'test': test,})
                return redirect('/examination/pending/', {'error': 'You have already given that test'})
        
def confirm_test(request):
    if not request.user.is_authenticated:
        return redirect('/login')   
    else:
        if request.method == 'GET':
            return redirect('/login')
        else:
            try:
                test_id = request.POST['test_id']
            except KeyError:
                raise Http404("Poll does not exist")
            hasUserGivenTest = UserTests.objects.filter(user=request.user, test__id=test_id)
            if (hasUserGivenTest.count() == 0):
                # User can give test
                test = Test.objects.filter(pk=test_id, active=True)[0]
                return render(request, 'confirm_test.html', {'test': test,})
            else:
                return redirect('/examination/pending/', {'error': 'You have already given that test'})

def give_test(request, test_code):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        if request.method == 'GET':
            return redirect('/login')
        else:
            pass        
    pass

def submit_test(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        if request.method == 'GET':
            return redirect('/login')
        else:
            if int(request.session['test_id']) != int(request.POST['test_id']):
                # Different test ID
                raise Http404("Session Test Id and response Test Id do not match.")
            sess_ques_set = request.session['ques_set']
            responses = []
            T = Test.objects.get(pk=int(request.POST['test_id']))
            if T.active == False:
                return redirect('/examination/pending/', {'error': 'You have already given that test'})
            with transaction.atomic():
                userTest = UserTests.objects.get(user = request.user, test=Test.objects.get(pk=int(request.POST['test_id'])))
                userTest.save()
                for q in sess_ques_set:
                    resp = request.POST.get(f'ques_{q}', None)
                    if resp == None:
                        #raise Http404("Required questions not found!")
                        ans = None
                    else:
                        ans = Answer.objects.filter(pk=int(resp))[0]
                    ques = Question.objects.filter(pk=q)[0]
                    responses.append(UserResponse(response=ans, test=userTest, ques=ques))
                UserResponse.objects.bulk_create(responses)
            userTest.completed = True
            userTest.save()
            return redirect('/examination/pending/', {'error': 'You have already given that test'})
            # return raise Http404("Poll does not exist")
            
def check_answers(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        if request.method == 'GET':
            return render(request, 'check_answer.html')
        try:
            T = Test.objects.get(test_code=request.POST['test_id'])
            U = Account.objects.get(token__token=request.POST['user_token'])
        except:
            return redirect('/check_answer', {'error': 'Incorrect Test code or User token'})
        userTest=UserTests.objects.get(user = U, test=T)
        # print(userTest)
        # print(U)
        # print(T)
        user_responses = UserResponse.objects.filter(test=userTest)
        # print(user_responses)
        return render(request, 'check_answer.html', {'user_responses':user_responses, 'test_id': request.POST['test_id'], 'user_token': request.POST['user_token']})