from typing import LiteralString
from uuid import uuid4
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "в ожидании"
        READY = "готово"
        PAID = "оплачено"

    id = models.UUIDField(primary_key=True, default=uuid4)
    table_number = models.IntegerField()
    items = models.ManyToManyField(Product, through="OrderItem", related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )

    def __str__(self) -> str:
        return f"Заказ №{self.id} для Столика №{self.table_number}"

    def calculate_total(self) -> None:
        total: float = sum(item.item_total_price() for item in self.items.all())
        self.total_price: float = total
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def item_total_price(self) -> float:
        return self.product.price * self.quantity

    def __str__(self) -> LiteralString:
        return f"{self.product.name} x {self.quantity}"
