from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SketchImageViewSet, sketch_converter

router = DefaultRouter()
router.register(r'sketch', SketchImageViewSet, basename='sketch')

urlpatterns = [
    path('', sketch_converter, name="home"),
    path('api/', include(router.urls)),
]
