from django.shortcuts import render
from .models import Product, OrderLog
from django.http import HttpResponse, JsonResponse
from django.db.models import F, Sum, Count, Case, When
import pprint

pp = pprint.PrettyPrinter(indent=4)
# 쿼리셋들 이쁘게 보려고!

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
    aggregation = order_qs_annotate.aggregate(
        total_price=Sum('price')
        )
    print(aggregation)
    return HttpResponse(aggregation.get('total_price')) 
    # enctype때문에 숫자가 안보여서 일단 딕셔너리 밸류로 가져와줌...

def daily_price(request):
    daily_list = OrderLog.objects.values(
        'created' # 묶어줄 기준을 정한다! (여기선 날짜별로)
        # 그런데 일까지만 잘라줘야함!!!! => datetime()을 이용해야할 것 같음
        #
        ).annotate(
            daily_total=Sum('product__price') # 날짜별로 가격들을 다 모아서 daily_total에 넣음!
        )

    # 그냥 터미널에서 이쁘게 보려고..
    pp_list = []
    for data in daily_list:
        pp_list.append(data)
    pp.pprint(pp_list)
    
    return HttpResponse(daily_list)








def index(request):
    product = Product.objects.all()
    return render(request, 'index.html', {'product':product})

