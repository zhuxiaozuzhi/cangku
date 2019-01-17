import hashlib
import re

from django.shortcuts import render, redirect
from django.urls import reverse

from reg_log.forms import UsersForm
from reg_log.models import Users


def register(request):
    if request.method == 'GET':
        usersform = UsersForm()
        return render(request, 'yougou/sign-in.html', locals())

    elif request.method == 'POST':
        users = Users.objects.all()  # 查出数据库中所有用户
        data = {}
        regemail = request.POST.get('regemail')
        if regemail not in users['email']:  # 判断email是否重复
            data['email_status'] = '900'
        else:
            data['email_status'] = '901'

        regname = request.POST.get('regname')
        if regname not in users['name']:  # 判断用户名是否重复
            data['name_status'] = '900'
        else:
            data['name_status'] = '901'

        regtel = request.POST.get('regtel')
        rp = re.compile('(^1(3[\d])|(47|45)|(5[^3|4])|(66)|(7[013678])|(8[\d])|(9[89]))\d{8}$')
        tel = rp.match(regtel)
        if tel:  # 判断电话号码是否合法
            data['tel_status'] = '900'
        else:
            data['tel_status'] = '901'

        regpwd = request.POST.get('regpwd')
        if len(regpwd) < 8:  # 判断密码是否有效
            data['regpwd_status'] = '900'
        else:
            p = re.compile('^[a-z]|[A-Z]')
            regpwd = p.match(regpwd)
            data['regpwd_status'] = '901'

        c_pwd = request.POST.get('c_pwd')
        if c_pwd == regpwd:
            data['c_pwd'] = '900'
        else:
            data['c_pwd'] = '901'
        new_user = Users()  # 实例化新用户对象，新用户属性
        new_user.email = regemail
        new_user.name = regname
        new_user.tel = tel
        md5 = hashlib.md5()
        md5.update(regpwd.encode("utf-8"))
        new_user.pwd = md5.hexdigest()

        new_user.save()
        return render(request, 'yougou/sign-in.html', {'data': data})


def login(request):
    if request.method == 'GET':
        return render(request, 'yougou/sign-in.html')

    elif request.method == 'POST':
        loginname = request.POST.get("loginname")
        loginpwd = request.POST.get('loginpwd')
        md5 = hashlib.md5()
        md5.update(loginpwd.encode("utf-8"))
        loginpwd = md5.hexdigest()

        users = Users.objects.filter(name=loginname, pwd=loginpwd)
        if users:
            user = users.first()
            request.session['user_id'] = user.id  # 登录成功后设置session属性
            return redirect(reverse('yougou:index'))
        else:
            return redirect(reverse('yougou:sign-in.html'))


def logout(request):
    request.session.flush()  # 如果退出登录，则彻底删除之前设置的session
    return redirect(reverse('yougou:index'))
