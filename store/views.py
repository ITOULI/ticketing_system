from django.shortcuts import get_object_or_404, render

from .models import Category, Ticket


def ticket_all(request):
    tickets = Ticket.objects.prefetch_related("ticket_image").filter(is_active=True)
    return render(request, "store/index.html", {"tickets": tickets})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    tickets = Ticket.objects.filter(
        category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True)
    )
    return render(request, "store/category.html", {"category": category, "tickets": tickets})


def ticket_detail(request, slug):
    ticket = get_object_or_404(Ticket, slug=slug, is_active=True)
    return render(request, "store/single.html", {"ticket": ticket})
