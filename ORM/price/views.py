from django.shortcuts import render
from .models import Product, OrderLog
from django.http import HttpResponse, JsonResponse
from django.db.models import F, Sum, Count, Case, When


order_qs = OrderLog.objects.values(
        'created', 'product__name', 'product__price'
                    # ForeignKey역참조
    )

# annotate는 필드를 하나 생성하고, 내용을 채울 수 있음!
order_qs_annotate = OrderLog.objects.annotate(
    name=F('product__name'), 
    price=F('product__price')
    # F를 사용해서 key네임을 지정해주자
    ).values(
        'created', 'name', 'price'
    )

def annotate(request):
    return HttpResponse(order_qs_annotate)

# aggregate는 하나의 각 컬럼들을 조회해서 하나의 결과값을 반환 가능
def aggregate(request):
    # annotate로 만든 price컬럼을 Sum을 통해 합쳐분다.
    aggregation = order_qs_annotate.aggregate(total_price=Sum('price'))
    print(aggregation)
    return HttpResponse(aggregation.get('total_price')) 
    # enctype때문에 숫자가 안보여서 일단 딕셔너리 밸류로 가져와줌...








def index(request):
    product = Product.objects.all()
    return render(request, 'index.html', {'product':product})

