from django.conf.urls import url, include
from . import views
from . import idc

urlpatterns = [
    url(r'^idc/', include([
        url(r'add/$', idc.CreateIdcView.as_view(), name="idc_add"),
        url(r'list/$', idc.IdcListView.as_view(), name="idc_list"),
    ])),

]
