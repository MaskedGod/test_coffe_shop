import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafe.settings")
django.setup()

from orders.models import Product


def create_products():
    # Список продуктов для добавления
    products = [
        {"name": "Кофе", "price": 5.00, "description": "Ароматный кофе"},
        {"name": "Чай", "price": 3.00, "description": "Свежезаваренный чай"},
        {"name": "Пицца", "price": 10.00, "description": "Итальянская пицца"},
        {"name": "Бургер", "price": 7.00, "description": "Сочный бургер"},
        {"name": "Салат", "price": 6.00, "description": "Свежий салат"},
    ]

    for product_data in products:
        product, created = Product.objects.get_or_create(**product_data)
        if created:
            print(f"Создан продукт: {product.name}")
        else:
            print(f"Продукт уже существует: {product.name}")


if __name__ == "__main__":
    create_products()
