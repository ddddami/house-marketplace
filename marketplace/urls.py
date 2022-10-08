from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('houses', views.HouseViewSet, basename='house')
router.register('customers', views.CustomerViewSet)
router.register('carts', views.CartViewSet)
router.register('orders', views.OrderViewSet, basename='order')
houses_router = routers.NestedDefaultRouter(
    router, 'houses', lookup='house')
houses_router.register('images', views.HouseImageViewSet,
                       basename='house-images')
houses_router.register('reviews', views.ReviewViewSet,
                       basename='house-reviews')
carts_router = routers.NestedDefaultRouter(
    router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet,
                      basename='cart-items')
urlpatterns = router.urls + houses_router.urls + carts_router.urls
