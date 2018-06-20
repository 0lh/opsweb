from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .models import Product
from django.http import HttpResponse


class ProductAddView(TemplateView):
    template_name = "server/add_product.html"

    def get_context_data(self, **kwargs):
        context = super(ProductAddView, self).get_context_data(**kwargs)
        context["user_list"] = User.objects.filter(is_superuser=False)
        context["products"] = Product.objects.filter(pid__exact=0)
        return context

    def post(self, request):
        print(request.POST)
        return HttpResponse('...')
