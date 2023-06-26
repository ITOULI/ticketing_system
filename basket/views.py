from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from store.models import Ticket

from .basket import Basket


def basket_summary(request):
    basket = Basket(request)
    return render(request, 'basket/summary.html', {'basket': basket})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        ticket_id = int(request.POST.get('ticketid'))
        ticket_qty = int(request.POST.get('ticketqty'))
        ticket = get_object_or_404(Ticket, id=ticket_id)
        basket.add(ticket=ticket, qty=ticket_qty)

        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        ticket_id = int(request.POST.get('ticketid'))
        basket.delete(ticket=ticket_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        ticket_id = int(request.POST.get('ticketid'))
        ticket_qty = int(request.POST.get('ticketqty'))
        basket.update(ticket=ticket_id, qty=ticket_qty)

        basketqty = basket.__len__()
        basketsubtotal = basket.get_subtotal_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': basketsubtotal})
        return response


