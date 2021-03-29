import zope.interface
from .models import Product, ProductCategories
from .forms import PrescriptionAddForm
import json
from django.http import JsonResponse

class productSimpleFactory(zope.interface.Interface):

    product_category = zope.interface.Attribute("foo")
    products = zope.interface.Attribute("foo")

    def get_product_context(self, id):
        pass


class sunglassesDisp:

    def get_product_context(self, id):
        product_category = ProductCategories.objects.get(id=id)
        print(product_category)
        products = Product.objects.filter(category=product_category)
        print(products)
        context = {'product_category': product_category,
                   'products': products}
        return context


class lensDisp:

    def get_product_context(self, id):
        product_category = ProductCategories.objects.get(id=id)
        products = Product.objects.filter(category=product_category)
        context = {'product_category': product_category,
                   'products': products}
        return context


class framesDisp:

    def get_product_context(self, id):
        product_category = ProductCategories.objects.get(id=id)
        products = Product.objects.filter(category=product_category)
        context = {'product_category': product_category,
                   'products': products}
        return context

    def post_prescription_details(self, request):
        form = PrescriptionAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        dic = {
        'data' : 'hello',
        'total_item_cart' : 8,
        }
        return JsonResponse(dic, safe=False)

    def get_product_context_shape(self,id,shape):
        product_category = ProductCategories.objects.get(id=id)
        products = Product.objects.filter(category=product_category,shape=shape)
        context = {'product_category': product_category,
                   'products': products}
        return context