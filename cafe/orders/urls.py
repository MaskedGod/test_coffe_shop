from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("create-order/", views.create_order_view, name="create_order"),
]
