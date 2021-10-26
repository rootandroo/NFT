from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from rarity import views


urlpatterns = [
    path('', views.assets, name='assets'),
    path('<project>/', views.assets, name='assets')
]

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'assets', views.AssetViewSet, basename='asset')
router.register(r'collections', views.CollectionViewSet, basename='collection')
urlpatterns += [
    path('api/', include(router.urls)),
]