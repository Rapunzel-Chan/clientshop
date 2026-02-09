from django.urls import path
from .views import AddProductToOrderView

urlpatterns = [
    path("add-product/", AddProductToOrderView.as_view()),
]
