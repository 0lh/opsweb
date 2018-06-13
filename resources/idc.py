from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect, reverse
from django.http import HttpResponse
import json
from resources.models import Idc
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

class CreateIdcView(TemplateView):
    template_name = "idc/add_idc.html"

    def post(self, request):
        print(request.POST)
        print(reverse("success", kwargs={'next': 'user_list'}))
        # return redirect('success', next='user_list')
        errmsg = '人为的失败，请重新处理'
        # return redirect("error", next='idc_add', msg=errmsg)
        # 先取到前端发送的post数据
        name = request.POST.get('name', "")
        idc_name = request.POST.get('idc_name', "")
        address = request.POST.get('address', "")
        username = request.POST.get('username', "")
        phone = request.POST.get('user_phone', "")
        email = request.POST.get('email', "")

        # 2、对数据进行验证
        errmsg = []
        if not name:
            errmsg.append("idc简称不能为空")
        if not idc_name:
            errmsg.append("idc_name简称不能为空")
        if errmsg:
            return redirect('error', next='idc_add', msg=json.dumps(errmsg))

        # 3、将数据插入到数据库，创建模型对象
        idc = Idc()
        idc.name = name
        idc.idc_name = idc_name
        idc.address = address
        idc.username = username
        idc.user_phone = phone
        idc.email = email
        try:
            idc.save()
        except Exception as e:
            return redirect('error', next='idc_add', msg=e.args)

        return redirect('success', next='idc_list')


class IdcListView(ListView):
    model = Idc
    template_name = 'idc/idc_list.html'

    @method_decorator(permission_required("resources.add_idc", login_url='/'))
    def get(self, request, *args, **kwargs):
        return super(IdcListView, self).get(request, *args, **kwargs)
