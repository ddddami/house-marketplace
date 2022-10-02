from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('houses', views.HouseViewSet, basename='house')
router.register('customers', views.CustomerViewSet)
router.register('carts', views.CartViewSet)
houses_router = routers.NestedDefaultRouter(
    router, 'houses', lookup='house')
houses_router.register('images', views.HouseImageViewSet,
                       basename='house-images')
houses_router.register('reviews', views.ReviewViewSet,
                       basename='house-reviews')
urlpatterns = router.urls + houses_router.urls
