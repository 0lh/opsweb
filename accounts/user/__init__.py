from django.views.generic import ListView, View
from django.contrib.auth.models import User, Group
# 验证所有视图的登录验证
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, QueryDict
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.shortcuts import reverse
from django.conf import settings


# 使用django 内置ListView
class UserListView(LoginRequiredMixin, ListView):
    template_name = "user/user_list.html"
    model = User
    paginate_by = 8
    before_range_num = 4
    after_range_num = 5
    ordering = 'id'
    ''' 
    源码写死
    context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset
            }
    '''

    def get_queryset(self):
        queryset = super(UserListView, self).get_queryset()
        # 排除管理员账号显示
        queryset = queryset.exclude(is_superuser=True)
        username = self.request.GET.get("search_username", None)
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)

        # d当前页的前3条
        context["page_range"] = self.get_page_range(context['page_obj'])
        # 处理搜索条件
        search_data = self.request.GET.copy()
        try:
            search_data.pop("page")
        except:
            pass
        context.update(search_data.dict())
        context['search_data'] = "&" + search_data.urlencode()
        return context

    def get_page_range(self, page_obj):
        current_index = page_obj.number
        start = current_index - self.before_range_num
        end = current_index + self.after_range_num
        if start <= 0:
            start = 1

        if end >= page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages
        return range(start, end + 1)

    # @method_decorator(permission_required("auth.add_user", login_url=reverse('error', kwargs={'next': 'dashboard',

    # 不拥有add_user权限，则会返回到主页面
    @method_decorator(permission_required("auth.add_user", login_url='/'))
    def get(self, request, *args, **kwargs):
        return super(UserListView, self).get(request, *args, **kwargs)


class ModifyUserStatusView(View):
    def post(self, request):
        print(request.POST)
        uid = request.POST.get("uid", "")
        ret = {"status": 0}
        try:
            user_obj = User.objects.get(id=uid)
            user_obj.is_active = False if user_obj.is_active else True
            user_obj.save()
            '''
            if user_obj.is_active:
                user_obj.is_active = False
            else:
                user_obj.is_active = True
            '''
        except User.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "该用户不存在"
        return JsonResponse(ret)


class ModifyUserGroupView(View):
    def get(self, request):
        uid = request.GET.get("uid", "")
        group_objs = Group.objects.all()
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            pass
        else:
            # group_objs-
            # 排除用户原来的组,select * from group where id not in (1,2,3,..)
            group_objs = group_objs.exclude(id__in=user_obj.groups.values_list("id"))

        # 转换成字典,QuerySet不能被序列化，
        return JsonResponse(list(group_objs.values("id", "name")), safe=False)

    def put(self, request):
        ret = {"status": 0}
        print(request.POST)
        print(request.body)
        data = QueryDict(request.body)
        print(data)
        uid = data.get("uid", "")
        gid = data.get("gid", "")
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = '该用户不存在'
            return JsonResponse(ret)
        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = '该用户组不存在'
            return JsonResponse(ret)
        user_obj.groups.add(group_obj)
        return JsonResponse(ret)

    def delete(self, request):
        ret = {"status": 0}
        print(request.body)
        data = QueryDict(request.body)
        try:
            user_obj = User.objects.get(id=data.get("uid", ""))
            group_obj = Group.objects.get(id=data.get("gid", ""))

            # 第一种删除方式
            user_obj.groups.remove(group_obj)

            # 第二种
            # group_obj.user_set.remove(user_obj)
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户不存在"
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户组不存在"
        return JsonResponse(ret)
