from django.db import models


# Create your models here.

class Idc(models.Model):
    name = models.CharField("idc 字母简称", max_length=10, default="", unique=True)
    idc_name = models.CharField("idc 中文名称", max_length=100, default="")
    address = models.CharField("具体地址,云厂商可以不填", max_length=255, null=True)
    phone = models.CharField("机房联系电话", max_length=20, null=True)
    email = models.EmailField("机房联系邮件", max_length=32, null=True, default="")
    username = models.CharField("机房联系人", max_length=32, null=True)

    class Meta:
        db_table = 'resources_idc'


class Product(models.Model):
    service_name = models.CharField("业务线的名称", max_length=32)
    module_letter = models.CharField("业务线字母简称", max_length=10, db_index=True)
    op_inteface = models.CharField("运维对接人", max_length=150)
    dev_interface = models.CharField("业务对接人", max_length=150)
    pid = models.IntegerField("上线业务线id", db_index=True)

    def __str__(self):
        return self.mod_letter
