from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name='index'),
    path('view_products/',views.view_products, name='view_products'),
    path('contact/',views.contact, name='contact'),
    path('about_us/',views.about_us, name='about_us'),
    path('view_blog/',views.view_blog, name='view_blog'),
    path('view_product_details/<int:product_id>/',views.view_product_details, name='view_product_details'),
    path('register',views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart, name='add_to_cart'),
    path('view_shopping_cart/',views.view_shopping_cart, name='view_shopping_cart'),
    path('remove_cart_item/<int:item_id>/',views.remove_cart_item, name='remove_cart_item'),
    path('add_review/<int:product_id>/',views.add_review, name='add_review'),
    path('search/',views.search_products, name='search_products'),
    path('buynow/<int:item_id>/',views.buynow, name='buynow'),
    path('handle_payment/', views.handle_payment, name='handle_payment'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)