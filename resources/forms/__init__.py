from django import forms
from resources.models import Idc, Product
from django.contrib.auth.models import User


class ProductForm(forms.Form):
    service_name = forms.CharField(required=True)
    module_letter = forms.CharField(required=True)
    op_inteface = forms.MultipleChoiceField(
        choices=((u.email, u.username) for u in User.objects.filter(is_superuser=False)))
    dev_interface = forms.MultipleChoiceField(
        choices=((u.email, u.username) for u in User.objects.filter(is_superuser=False)))
    pid = forms.CharField(required=True)

    # 业务线只存在两级
    def clean_pid(self):
        pid = self.cleaned_data['pid']
        if pid.isdigit():
            if int(pid) != 0:
                try:
                    p_obj = Product.objects.get(pk=pid)
                    if p_obj != 0:
                        raise forms.ValidationError("请选择正确的一级业务线")
                except Product.DoesNotExist:
                    raise forms.ValidationError("请选择正确的一级业务线")
        else:
            raise forms.ValidationError("请选择正确的一级业务线")
        return pid

    def clean_dev_interface(self):
        dev_interface = self.cleaned_data['dev_interface']
