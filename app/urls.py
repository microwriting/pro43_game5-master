from django.urls import path
from . import views
from .views import ChartData

app_name = 'app'

urlpatterns = [
    path('', views.slotmachine, name='slotmachine'),
    # path('', views.SlotMachine.as_view(), name='slotmachine'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('yamadaslot/', views.Aboutview.as_view(), name='yamadaslot'),
    path("api/chart/data/", ChartData.as_view(), name="chartdata"),
]