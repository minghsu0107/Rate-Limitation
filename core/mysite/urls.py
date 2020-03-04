from django.urls import path
from app.views import DemoLimitRateView

urlpatterns = [
    path('', DemoLimitRateView, name="demo-limited"),
]
