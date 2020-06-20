from django.shortcuts import render
from .models import Product, OrderLog
from django.http import HttpResponse, JsonResponse
from django.db.models import F, Sum, Count, Case, When

def index(request):
    product = Product.objects.all()
    return render(request, 'index.html', {'product':product})


# annotate는 필드를 하나 생성하고, 내용을 채울 수 있음!
def annotate(request):
    order_qs = OrderLog.objects.values(
        'created', 'product__name', 'product__price'
    )

    order_qs_annotate = OrderLog.objects.annotate(

        name=F('product__name'), 
        price=F('product__price')
        # F를 사용해서 key네임을 지정해주자
        ).values(
            'created', 'name', 'price'
        )

    return HttpResponse(order_qs_annotate)