# 用户组列表
from django.views.generic import ListView, View, TemplateView
from django.contrib.auth.models import Group
from django.http import JsonResponse, Http404
from django.db import IntegrityError


class GroupListView(ListView):
    model = Group
    template_name = "user/group_list.html"


'''
View 通用
template_view带有模板的时候使用
ListView 在展示列表的时候使用
'''


class GroupCreateView(View):
    def post(self, request):
        ret = {"status": 0}
        print(request.POST)
        # < QueryDict: {'name': ['liuhao']} >
        group_name = request.POST.get("name", "")
        if not group_name:
            ret['status'] = 1
            ret['errmsg'] = "用户组不能为空"
            return JsonResponse(ret)
        try:
            g = Group(name=group_name)
            g.save()
        except Exception as e:
            ret['status'] = 1
            ret['errmsg'] = "该用户组已存在"
        except Exception as e:
            print("all error")
            print(e.args)

        return JsonResponse(ret)


class GroupUserList(TemplateView):
    template_name = "user/group_member_list.html"

    def get_context_data(self, **kwargs):
        context = super(GroupUserList, self).get_context_data(**kwargs)
        # 将指定用户组内的成员列表传给模板
        gid = self.request.GET.get("gid", "")
        try:
            group_obj = Group.objects.get(id=gid)
            context['obj_list'] = group_obj.user_set.all()
        except Group.DoesNotExist:
            raise Http404("group does not exist")
        context['gid'] = gid
        return context
