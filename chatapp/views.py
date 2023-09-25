from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import date, timedelta
from .models import QuestionAnswer
from django.shortcuts import render
from django.http import JsonResponse
import requests
import json

# Create your views here.
# API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
# headers = {"Authorization": "Bearer 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"}

# def query(payload):
#         data = json.dumps(payload)
#         response = requests.post(API_URL, headers=headers, data=data)
#         return json.loads(response.content.decode("utf-8"))

@login_required(login_url='signin')
def index(request):
    today = date.today()
    yesterday = date.today() - timedelta(days=1)
    seven_days_ago = date.today() - timedelta(days=7)
    
    questions = QuestionAnswer.objects.filter(user=request.user)
    t_questions = questions.filter(created=today)
    y_questions = questions.filter(created=yesterday)
    s_questions = questions.filter(created__gte=seven_days_ago, created__lte=today)
    
    context = {"t_questions":t_questions, "y_questions": y_questions, "s_questions": s_questions}

    return render(request, "C:/Users/SANIA/chatgpt/chatapp/templates/index.html", context)


def signup(request):
    if request.user.is_authenticated:
        return redirect("index")
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST["username"]
            password = request.POST["password1"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
    context = {"form": form}
    return render(request, "C:/Users/SANIA/chatgpt/chatapp/templates/signup.html", context)


def signin(request):
    err = None
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == 'POST':
        
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        
        else:
            err = "Invalid Credentials"
        
        
    context = {"error": err}
    return render(request, "C:/Users/SANIA/chatgpt/chatapp/templates/signin.html", context)


def signout(request):
    logout(request)
    return redirect("signin")



# def chatbot(request):
#     if request.method == 'POST':
#          message= request.POST.get('message')
#          print(message)
#          response = query({"inputs": {
# 		"text": message,}, })
#          ans=response['generated_text']
#          return JsonResponse({'message':message, 'response': ans})
#     return render(request, 'chatbot.html')
# def query(payload):
# 	response = requests.post(API_URL, headers=headers, json=payload)
# 	return response.json()
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": "Bearer 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"}

def query(payload):
        data = json.dumps(payload)
        response = requests.post(API_URL, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))

def getValue(request):
    data = json.loads(request.body)
    print(data)
    message = data["msg"] 
    print(message)
    payload={
        "inputs":message,
        "max_length":200
    }
    response = query(payload)
    answer = response.get("generated_text")
    QuestionAnswer.objects.create(user=request.user, question=message, answer = answer)
    return JsonResponse({"msg":message,"res":answer})
