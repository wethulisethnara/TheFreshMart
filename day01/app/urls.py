from django.urls import path # type: ignore
from . import views
from app.views import contact_view

urlpatterns = [
    path('category/', views.categoryview,name='category'),
    path('unit/', views.unitview, name='unit'),
    path('items/',views.itemsview, name='items'),
    path('item/<int:pk>/', views.itemview, name='item'),
    path('supplier/', views.supplierview, name='supplier'),
    path('order/', views.orderview, name='order'),
    path('shop/',views.shopview,name='shop'),
    path('login/', views.loginview, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('update/<int:item_id>/', views.update_item, name='update_item'),    
    path('delete-confirm/<int:item_id>/', views.delete_confirm, name='delete_confirm'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('update-category/<int:catergory_id>/', views.update_catergory, name='update_catergory'),
    path('delete-confirm-category/<int:category_id>/', views.delete_confirm_category, name='delete_confirm_category'),
    path('delete-category/<int:category_id>/', views.delete_catergory, name='delete_category'),
    path('update-unit/<int:unit_id>/', views.update_unit, name='update_unit'),
    path('delete-confirm-unit/<int:unit_id>/', views.delete_confirm_unit, name='delete_confirm_unit'),
    path('delete-unit/<int:unit_id>/', views.delete_unit, name='delete_unit'),
    path('update-order/<int:order_id>/', views.update_order, name='update_order'),
    path('delete-confirm-order/<int:order_id>/', views.delete_confirm_order, name='delete_confirm_order'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('contact/', views.contact_view, name='contact'),
    path('product_buy/<int:pk>/', views.product_buy, name='product_buy'),
    path('cart/', views.cart_detail, name='cart_detail'), 
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'), 
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'), 
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
  
]
