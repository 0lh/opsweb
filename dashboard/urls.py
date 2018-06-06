from django.conf.urls import url, include
from . import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.IndexView.as_view(), name='index'),  # 第三个是视图函数的名称
    url(r'^user/(20)/$', views.user_detail),  #
]
