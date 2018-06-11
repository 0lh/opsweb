from django.conf.urls import url, include

from accounts import group
from . import views, user

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # 类视图需要as_view()方法
    url(r'^login/$', views.UserLoginView.as_view(), name='user_login'),  # 第三个是视图函数的名称
    url(r'^logout/$', views.UserLogoutView.as_view(), name="user_logout"),
    # url(r'^user/list/$', views.UserListView.as_view(), name="user_list"),
    url(r'^user/list/$', user.UserListView.as_view(), name="user_list"),
    # url(r'^user/list/$', user.ModifyUserStatusView.as_view(), name="user_status_modify"),

    url(r'^user/', include([
        url(r'^modify/', include([
            url(r'status/$', user.ModifyUserStatusView.as_view(), name="user_modify_status"),
            url(r'group/$', user.ModifyUserGroupView.as_view(), name="user_modify_group"),
        ]))
    ])),

    url(r'^group/', include([
        url(r'^$', group.GroupListView.as_view(), name="group_list"),
        url(r'^create/$', group.GroupCreateView.as_view(), name="group_create"),
        url(r'^member_list/$', group.GroupUserList.as_view(), name="group_member_list"),
    ])),
]
