#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :order.py
@说明    :
@时间    :2023/02/13 16:22:10
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.contrib.auth import get_user_model

from baykeCore.common.mixin import LoginRequiredMixin

User = get_user_model()




