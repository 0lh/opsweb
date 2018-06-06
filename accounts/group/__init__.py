# 用户组列表
from django.views.generic import ListView, View
from django.contrib.auth.models import Group
from django.http import JsonResponse
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
