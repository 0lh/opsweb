from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import View, TemplateView
from django.core.paginator import Paginator
# 验证所有视图的登录验证
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# request 是一个HttpRequest对象,由django处理形成
'''
def login_view(request):
    if request.method == "GET":
        return render(request, "public/login.html")
    else:
        username = request.POST.get("username", "")
        userpass = request.POST.get("password", "")
        user = authenticate(username=username, password=userpass)
        ret = {"status": 0, "errmsg": ""}
        if user:
            login(request, user)
            ret['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret['status'] = 1
            ret['errmsg'] = "用户名或密码错误，请联系管理员"
        # return JsonResponse(ret)
'''


# 需要模板的继承TemplateView
class UserLoginView(TemplateView):
    '''
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    '''
    # 默认行为，get方法加载模板
    template_name = "public/login.html"

    # 接受一个request对象
    def post(self, request):
        username = request.POST.get("username", "")
        userpass = request.POST.get("password", "")
        user = authenticate(username=username, password=userpass)
        ret = {"status": 0, "errmsg": ""}
        if user:
            login(request, user)
            ret['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret['status'] = 1
            ret['errmsg'] = "用户名或密码错误，请联系管理员"
        return JsonResponse(ret)


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("user_login"))


'''
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("user_login"))
'''


def user_list_view(request):
    user_queryset = User.objects.all()
    for user in user_queryset:
        print(user.username, user.email)
    return render(request, "user/user_list.html", {"user_list": user_queryset})


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class User_ListView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user_queryset = User.objects.all()
        for user in user_queryset:
            print(user.username, user.email)
        return render(request, "user/user_list.html", {"user_list": user_queryset})


class UserListView(TemplateView):
    # 默认找get方法
    template_name = "user/user_list.html"
    per = 10

    # 讲变量传到模板，复写父类方法
    def get_context_data(self, **kwargs):
        # 覆盖父类函数
        try:
            # 默认page为1
            page_num = int(self.request.GET.get('page', 1))
        except:
            page_num = 1
        # end = self.per * page
        # start = end - self.per
        context = super(UserListView, self).get_context_data(**kwargs)
        user_list = User.objects.all()
        paginator = Paginator(user_list, self.per)
        # 当前页面
        context['page_obj'] = paginator.page(page_num)
        context["object_list"] = context["page_obj"].object_list
        return context

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(UserListView, self).get(request, *args, **kwargs)


class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("{}?next={}".format(reverse("user_login"), "/dashboard/"))

        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
