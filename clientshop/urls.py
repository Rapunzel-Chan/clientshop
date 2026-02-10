from django.urls import path

from .apps import ClientshopConfig
from .views import AddProductToOrderView

app_name = ClientshopConfig.name

urlpatterns = [
    path("add-product/", AddProductToOrderView.as_view(), name="add_product"),
]
