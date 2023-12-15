from django.urls import path
from . import views

urlpatterns = [
    path("", views.CartItemViews.as_view()),
    path("<int:id>", views.CartItemViews.as_view()),
]
