from django import forms
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["table_number", "status"]


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


OrderItemFormSet = forms.inlineformset_factory(
    Order,
    OrderItem,
    fields=["product", "quantity"],
    extra=1,
    can_delete=True,
)
