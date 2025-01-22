from django import forms
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    """Форма для создания и редактирования заказов."""

    class Meta:
        model = Order
        fields = ["table_number", "status"]

    def clean_table_number(self):
        """Проверяет, что номер стола является положительным числом."""
        table_number = self.cleaned_data.get("table_number")
        if table_number < 1:
            raise forms.ValidationError("Номер стола должен быть положительным числом.")
        return table_number


class OrderItemForm(forms.ModelForm):
    """Форма для создания и редактирования элементов заказа."""

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]

    def clean_quantity(self):
        """Проверяет, что количество является положительным числом."""
        quantity = self.cleaned_data.get("quantity")
        if quantity < 1:
            raise forms.ValidationError("Количество должно быть положительным числом.")
        return quantity


OrderItemFormSet = forms.inlineformset_factory(
    Order,
    OrderItem,
    fields=["product", "quantity"],
    extra=5,
    can_delete=True,
)
