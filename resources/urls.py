from django.conf.urls import url, include
from . import views
from . import idc, product

urlpatterns = [
    url(r'^idc/', include([
        url(r'add/$', idc.CreateIdcView.as_view(), name="idc_add"),
        url(r'list/$', idc.IdcListView.as_view(), name="idc_list"),
    ])),

    url(r'product/', include([
        url(r'^add/$', product.ProductAddView.as_view(), name="add_product"),
    ])),

]
