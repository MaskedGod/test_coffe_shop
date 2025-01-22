from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Sum, Q
from django.contrib import messages
from .forms import OrderForm, OrderItemFormSet
from .models import Order


def index_view(request):
    search_query = request.GET.get("search", "")
    if search_query:
        orders = Order.objects.filter(
            Q(id__istartswith=search_query)
            | Q(table_number__icontains=search_query)
            | Q(status__icontains=search_query)
        )
        if not orders.exists():
            messages.info(request, "Заказы по вашему запросу не найдены.")
    else:
        orders = Order.objects.all()
    return render(request, "orders/index.html", {"orders": orders})


def create_order_view(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)

        if order_form.is_valid() and formset.is_valid():

            order = order_form.save()
            formset.instance = order
            formset.save()

            return redirect("index")
    else:
        order_form = OrderForm()
        formset = OrderItemFormSet()

    return render(
        request,
        "orders/order_form.html",
        {"order_form": order_form, "formset": formset},
    )


def edit_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order_form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if order_form.is_valid() and formset.is_valid():
            order_form.save()
            formset.save()
            return redirect("index")
    else:
        order_form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)
    return render(
        request,
        "orders/order_form.html",
        {"order_form": order_form, "formset": formset},
    )


def delete_order_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.delete()
        messages.success(request, "Заказ успешно удален.")
    except Order.DoesNotExist:

        messages.error(request, "Заказ не найден.")
    return redirect("index")


def revenue_view(request):
    total_revenue = (
        Order.objects.filter(status="оплачено").aggregate(Sum("total_price"))[
            "total_price__sum"
        ]
        or 0
    )
    return render(request, "orders/revenue.html", {"total_revenue": total_revenue})
