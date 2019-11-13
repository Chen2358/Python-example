from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from sign.models import Event, Guest

# Create your views here.
def index(request):
	return render(request, 'index.html')

#登录
def login_action(request):
	if request.method == 'POST':
		username = request.POST.get('username', '')  #'username'对应于form表单中<input>标签的name属性
		password = request.POST.get('password', '')
		if username == '' or password == '':
			return render(request, "index.html", {"error": "username or password null!"})

		user = auth.authenticate(username=username, password=password)	#登录认证
		if user is not None:
			auth.login(request, user)		#登录
			# response.set_cookie('user', username, 3600)		#添加浏览器cookie
			request.session['user'] = username					#将session信息记录到浏览器
			response = HttpResponseRedirect('/event_manage/')	#登录后跳转
			return response
		else:
			return render(request, 'index.html', {'error': 'username or password error!'})
	#防止通过浏览器直接访问/login_aciton/
	return render(request,  "index.html")


#退出
@login_required
def logout(request):
	auth.logout(request)	#退出
	response = HttpResponseRedirect('/index/')
	return response


#发布会管理
@login_required										#限制登录后才能访问
def event_manage(request):
	# username = request.COOKIES.get('user', '') 	#读取浏览器cookie
	event_list = Event.objects.all()
	username = request.session.get('username', '')		#读取浏览器session
	return render(request, "event_manage.html", {"user": username,
												"events": event_list})

#发布会名称搜索
@login_required
def search_event_name(request):
	username = request.session.get('username', '')
	search_name = request.GET.get("name", "")
	event_list = Event.objects.filter(name__contains=search_name)
	return render(request, "event_manage.html", {"user": username,
												"events": event_list})
#嘉宾管理
@login_required
def guest_manage(request):
	username = request.session.get('username', '')
	guest_list = Guest.objects.all()

	paginator = Paginator(guest_list, 3)		#每页显示数据
	page = request.GET.get('page')
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		#如果page不是整数，取第一页数据
		contacts = paginator.page(1)
	except EmptyPage:
		#如果page不再范围，取最后一页
		contacts = paginator.page(paginator.num_pages)
	return render(request, "guest_manage.html", {"user": username,
												"guests": contacts})
# #嘉宾手机号查询
# @login_required
# def search_guest_phone(request):
# 	username = request.session.get('usernme', '')
# 	search_phone = request.GET.get('phone', '')
# 	search_name_bytes = search_phone.encode(encoding="utf-8")
# 	guest_list = Guest.objects.filter(phone__contains=search_name_bytes)
	
# 	paginator = Paginator(guest_list, 3)		#每页显示数据
# 	page = request.GET.get('page')
# 	try:
# 		contacts = paginator.page(page)
# 	except PageNotAnInteger:
# 		#如果page不是整数，取第一页数据
# 		contacts = paginator.page(1)
# 	except EmptyPage:
# 		#如果page不再范围，取最后一页
# 		contacts = paginator.page(paginator.num_pages)
# 	return render(request, "guest_manage.html", {"user": username,
# 												"guests": contacts,
# 												"phone": search_phone})


#签到
@login_required
def sign_index(request, eid):
	event = get_object_or_404(Event, id=eid)
	return render(request, 'sign_index.html', {'event': event})

#签到动作
def sign_index_action(request, eid):
	event = get_object_or_404(Event, id=eid)
	phone = request.POST.get('phone', '')
	print(phone)
	result  = Guest.objects.filter(phone=phone)
	if not result:
		return render(request, 'sign_index.html', {'event': event,
												   'hint': 'phone error.'})

	result = Guest.objects.filter(phone=phone, event_id=eid)
	if not result:
		return render(request, 'sign_index.html', {'event': event,
												   'hint': ' event id or phone error.'})

	result = Guest.objects.get(phone=phone, event_id=eid)
	if result.sign:
		return render(request, 'sign_index.html', {'event': event,
												   'hint': 'user has sign in.'})
	else:
		Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
		return render(request, 'sign_index.html', {'event': event,
												   'hint': 'sign in success!',
												   'guest': result})




'''
get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错。
filter方法是从数据库的取得匹配的结果，返回一个对象列表，如果记录不存在的话，它会返回[]。
'''












