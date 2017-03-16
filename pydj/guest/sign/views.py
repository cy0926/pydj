from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404


# Create your views here.
def index(request):
    return render(request, "index.html")


# 登录动作
def login_action(request):
    # global username, password
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 调用auth的登录方法登录
            # response.set_cookie('user', username, 3600)  # 添加浏览器 cookie
            request.session['user'] = username  # 将session信息记录到浏览器
            response = HttpResponseRedirect('/event_manage')
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error~!'})


# 发布会管理
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    # username = request.COOKIES.get('user', '')  # 读取浏览器 cookie
    username = request.session.get('user', '')  # 读取浏览器 session
    return render(request, "event_manage.html", {"user": username,
                                                 "events": event_list})


# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username,
                                                 "events": event_list})


# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)  # 把查询出来的所有的嘉宾表guest_list放到Paginator类中，划分每页显示2条数据
    page = request.GET.get('page')  # 通过GET请求得到当前要显示第几页的数据
    try:
        contacts = paginator.page(page)  # 获取第n页面的数据
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range(e.g.  9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": contacts})


# 嘉宾名称搜索
'''
  嘉宾搜索的翻页功能有bug，当搜索结果大于1页的时候，翻至第二页会跟搜索关键字无关-----后期优化
'''


@login_required
def search_realname(request):
    username = request.session.get('user', '')
    search_realname = request.GET.get("realname", "")
    # search_phone = request.GET.get("phone", "")  # 想再添加一个可以电话搜索的功能。。。此处后期增加，现在不会
    guest_list = Guest.objects.filter(realname__contains=search_realname)
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range(e.g.  9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": contacts})


# 签到页面
@login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index.html', {'event': event})


# 签到动作
@login_required
def sign_index_action(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get('phone', '')

    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'phone error.'})

    result = Guest.objects.filter(phone=phone, event_id=event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'event id or phone error.'})
    result = Guest.objects.get(phone=phone)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': "user has sign in."})
    else:
        Guest.objects.filter(phone=phone).update(sign='1')
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'sign in success!',
                                                   'guest': result})


# 退出登录
@login_required
def logout(request):
    auth.logout(request)  # 退出登录
    response = HttpResponseRedirect('/index/')
    return response
