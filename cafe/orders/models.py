from uuid import uuid4
from django.db import models
from typing import LiteralString


class Product(models.Model):
    """Модель продукта, который может быть добавлен в заказ."""

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self) -> str:
        """Возвращает строковое представление продукта (его название)."""
        return self.name


class Order(models.Model):
    """Модель заказа, которая связывает столик и заказанные продукты с их статусом и общей стоимостью."""

    class StatusChoices(models.TextChoices):
        В_Ожидании = "в ожидании"
        Готово = "готово"
        Оплачено = "оплачено"

    id = models.UUIDField(primary_key=True, default=uuid4)
    table_number = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.В_Ожидании
    )

    def __str__(self) -> str:
        """Возвращает строковое представление заказа, используя первые 6 символов UUID и номер столика."""
        return f"Заказ №{str(self.id)[:6]} для Столика №{self.table_number}"

    def calculate_total(self) -> None:
        """Вычисляет полную стоимость заказа на основе связанных элементов заказа."""
        total: float = sum(item.item_total_price for item in self.order_items.all())
        if total:
            self.total_price = total

    def save(self, *args, **kwargs) -> None:
        """
        Переопределяет метод сохранения для автоматического пересчета
        общей стоимости перед сохранением заказа.
        """
        self.calculate_total()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Модель элемента заказа, связывающего продукт с заказом и количеством."""

    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def item_total_price(self) -> float:
        """Возвращает общую стоимость элемента заказа (цена продукта * количество)."""
        return self.product.price * self.quantity

    def __str__(self) -> LiteralString:
        """Возвращает строковое представление элемента заказа (название продукта и его количество)."""
        return f"{self.product.name} x {self.quantity} для Столика №{self.order.table_number}"

    def save(self, *args, **kwargs) -> None:
        """
        Переопределяет метод сохранения для обновления заказа
        при добавлении или изменении элемента заказа.
        """
        super().save(*args, **kwargs)
        self.order.save()

    def delete(self, *args, **kwargs) -> None:
        """
        Переопределяет метод удаления для обновления заказа
        при удалении элемента заказа.
        """
        super().delete(*args, **kwargs)
        self.order.save()
