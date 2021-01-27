import re

from django import http
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from meiduo_cs.meiduo_mail.utils.response_code import RETCODE


# Create your views here.


class UsernameCountView(View):
    def get(self, request, username):
        """

        :param request:
        :param username:
        :return: json
        """
        count = User.objects.filter(username=username).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'count': count})
        pass


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')

        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden('缺少参数')

        if not re.match(r'[a-zA-Z0-9_-]{5,20}', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')

        if not re.match(r'[0-9A-Za-z]{8,20}', password):
            return http.HttpResponseForbidden('请输入8-20个字符的mm')

        if password != password2:
            return http.HttpResponseForbidden('两次输入密码不一致')

        if not re.match(r'1[3-9]\d{9}', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号')

        if allow != 'on':
            return http.HttpResponseForbidden('')

        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})

        login(request, user)
        return redirect(reverse('contents:index'))
