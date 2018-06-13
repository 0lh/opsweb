from django.shortcuts import render, reverse, redirect
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


class SuccessView(TemplateView):
    template_name = "public/success.html"

    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        success_name = self.kwargs.get("next", "")
        next_url = '/'
        try:
            next_url = reverse(success_name)
        except:
            pass
        context['next_url'] = next_url
        return context


class ErrorView(TemplateView):
    template_name = 'public/error.html'

    def get_context_data(self, **kwargs):
        context = super(ErrorView, self).get_context_data(**kwargs)
        error_name = self.kwargs.get("next", "")
        errmsg = self.kwargs.get('msg', "")
        next_url = '/'
        try:
            next_url = reverse(error_name)
        except:
            pass
        context['next_url'] = next_url
        context['errmsg'] = errmsg
        return context
