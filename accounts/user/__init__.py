from django.views.generic import ListView, View
from django.contrib.auth.models import User, Group
# from accounts.views import LoginRequiredMixin

# 验证所有视图的登录验证
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse


# 使用django 内置ListView
class UserListView(LoginRequiredMixin, ListView):
    template_name = "user/user_list.html"
    model = User
    paginate_by = 8
    before_range_num = 4
    after_range_num = 5
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
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)

        # d当前页的前3条
        context["page_range"] = self.get_page_range(context['page_obj'])

        return context

    def get_page_range(self, page_obj):
        current_index = page_obj.number
        start = current_index - self.before_range_num
        end = current_index + self.after_range_num
        if start <= 0:
            start = 1

        if end > page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages
        return range(start, end)


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
        groups = Group.objects.all()
        # 转换成字典
        return JsonResponse(list(groups.values("id", "name")), safe=False)
