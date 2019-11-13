#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from polls.models import User
import datetime

def index(request):
	if 'user' not in request.session:
		return HttpResponseRedirect('show_login')
	template = loader.get_template('polls/main.html')
	return HttpResponse(template.render({'name':request.session['user']},request))

def show_login(request):
	template = loader.get_template('polls/index.html')
	return HttpResponse(template.render({},request))

def login(request):
	if 'HTTP_REFERER' not in request.META or request.META['HTTP_REFERER'] != 'http://localhost:8000/polls/show_login':
		return HttpResponse('登录失败')
	if 'commit' not in request.POST or request.POST['commit'] != 'Login':
		return HttpResponse('登录失败')
	q = User.objects.filter(name=request.POST['name'],pwd=request.POST['pwd'])
	if len(q) == 1:
		request.session['user'] = q[0].name
		return HttpResponseRedirect('.')
	else:
		return HttpResponse('登录失败')

def logout(request):
	if 'user' in request.session and request.session['user'] == request.GET['user']:
		del request.session['user']
		return HttpResponseRedirect('show_login')
def date(request):
	if 'user' not in request.session:
		return HttpResponseRedirect('show_login')
	return HttpResponse(str(datetime.datetime.now()))