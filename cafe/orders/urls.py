from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("create-order/", views.create_order_view, name="create_order"),
    path("edit-order/<uuid:order_id>/", views.edit_order_view, name="edit_order"),
    path("delete-order/<uuid:order_id>/", views.delete_order_view, name="delete_order"),
    path("revenue/", views.revenue_view, name="revenue"),
]
