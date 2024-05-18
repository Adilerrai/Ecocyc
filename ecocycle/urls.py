from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib import admin

from api.views import TrashTypeViewSet, TrashViewSet, RamassageViewSet,  BalanceViewSet

router = DefaultRouter()
router.register(r'trashtypes', TrashTypeViewSet)
router.register(r'trashes', TrashViewSet)
router.register(r'ramassages', RamassageViewSet)
router.register(r'balances', BalanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),

]