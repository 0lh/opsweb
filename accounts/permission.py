from django.views.generic import ListView
from django.contrib.auth.models import Permission


class PermissionListView(ListView):
    model = Permission
    template_name = 'user/permission_list.html'
    paginate_by = 10

