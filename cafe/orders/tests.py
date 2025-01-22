from django.test import TestCase, Client
from django.urls import reverse
from .models import Product, Order, OrderItem
from .forms import OrderForm, OrderItemForm


class ProductModelTest(TestCase):
    def test_create_product(self):
        """Тест создания продукта."""
        product = Product.objects.create(
            name="Кофе", price=5.00, description="Ароматный кофе"
        )
        self.assertEqual(product.name, "Кофе")
        self.assertEqual(product.price, 5.00)


class OrderModelTest(TestCase):
    def test_create_order(self):
        """Тест создания заказа."""
        order = Order.objects.create(table_number=1, status="в ожидании")
        self.assertEqual(order.table_number, 1)
        self.assertEqual(order.status, "в ожидании")

    def test_calculate_total(self):
        """Тест расчета общей стоимости заказа."""
        order = Order.objects.create(table_number=1)
        product = Product.objects.create(name="Кофе", price=5.00)
        OrderItem.objects.create(order=order, product=product, quantity=2)

        order.calculate_total()
        self.assertEqual(order.total_price, 10.00)


class OrderItemModelTest(TestCase):
    def test_create_order_item(self):
        """Тест создания элемента заказа."""
        order = Order.objects.create(table_number=1)
        product = Product.objects.create(name="Кофе", price=5.00)
        order_item = OrderItem.objects.create(order=order, product=product, quantity=2)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.item_total_price, 10.00)


class ViewTests(TestCase):
    def setUp(self):
        """Настройка данных для тестов."""
        self.client = Client()
        self.product = Product.objects.create(name="Кофе", price=5.00)
        self.order = Order.objects.create(table_number=1)

    def test_index_view(self):
        """Тест отображения главной страницы."""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_create_order_view(self):
        """Тест создания заказа."""
        response = self.client.post(
            reverse("create_order"),
            {
                "table_number": 2,
                "status": "в ожидании",
                "form-TOTAL_FORMS": 1,
                "form-INITIAL_FORMS": 0,
                "form-0-product": self.product.id,
                "form-0-quantity": 3,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)

    def test_delete_order_view(self):
        """Тест удаления заказа."""
        response = self.client.post(reverse("delete_order", args=[self.order.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)


class OrderFormTest(TestCase):
    def test_valid_form(self):
        """Тест валидной формы заказа."""
        form_data = {"table_number": 1, "status": "в ожидании"}
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Тест невалидной формы заказа (отрицательный номер стола)."""
        form_data = {"table_number": -1, "status": "в ожидании"}
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("table_number", form.errors)


class OrderItemFormTest(TestCase):
    def setUp(self):
        """Создаем продукт для тестов."""
        self.product = Product.objects.create(name="Кофе", price=5.00)

    def test_valid_form(self):
        """Тест валидной формы элемента заказа."""
        form_data = {"product": 1, "quantity": 2}
        form = OrderItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Тест невалидной формы элемента заказа (нулевое количество)."""
        form_data = {"product": 1, "quantity": 0}
        form = OrderItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)
