from django.conf.urls import url, include
from . import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.IndexView.as_view(), name='index'),  # 第三个是视图函数的名称

    # 匹配大小写字符串，放在kwargs中
    url(r'^success/(?P<next>[\s\S]*)/$', views.SuccessView.as_view(), name='success'),

    url(r'^error/(?P<next>[\s\S]*)/(?P<msg>[\s\S\\u4e00-\\u9fa5]*)/$', views.ErrorView.as_view(), name="error"),
]

# errmsg
