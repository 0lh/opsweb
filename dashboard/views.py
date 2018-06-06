from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

# Create your views here.
'''
第一种登录验证
@login_required
def index(request):
    return render(request, "index.html")
'''


# 1.11新增功能，LoginRequiredMixin
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    # @method_decorator，第二种登录验证
    def get(self, request, *args, **kwargs):
        return super(IndexView, self).get(request, *args, **kwargs)


# args
def user_detail(requesti, *args, **kwargs):
    print(args)  # 类型为Tuple
    return HttpResponse("")
