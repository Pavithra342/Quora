from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import UserRegisterForm, QuestionForm, AnswerForm
from .models import Question, Answer
from django.views import View
from django.contrib.auth import logout


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'quora/register.html', {'form': form})

def home(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'quora/home.html', {'questions': questions})

def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'quora/ask.html', {'form': form})

def view_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question).order_by('-created_at')
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('view_question', question_id=question.id)
    else:
        form = AnswerForm()
    return render(request, 'quora/view_question.html', {'question': question, 'answers': answers, 'form': form})

def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    answer.likes.add(request.user)
    return redirect('view_question', question_id=answer.question.id)
