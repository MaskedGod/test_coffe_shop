from django.shortcuts import render, redirect
from .forms import OrderForm, OrderItemFormSet


def index_view(request):
    return render(request, "orders/index.html")


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
