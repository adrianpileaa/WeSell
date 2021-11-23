from django.urls import path
from . import views
app_name = 'products'
urlpatterns = [
	path('', views.home, name = 'home'),
	path('product/<pr_id>/', views.product_view, name='product'),
	path('product/<pr_id>/delete/', views.delete_product_view, name='product-delete'),
	path('product-sell/', views.sell_product_view, name = 'product-sell'),
	path('categoty-search/<category_name>/', views.category_search_view,name='category-search'),
	path('main-search/', views.main_search_view, name = 'main-search'),
	path('all-search/<localization>/<word>/',views.all_search_view, name = 'all-search'),
	path('all-searching/<localization>/',views.all_search2_view, name = 'all-searching'),
	path('add_favourite/', views.add_favourite_list),
	path('favourites/', views.favourites_view, name = 'favourites'),
	path('chat/<user_id>/<room_name>/', views.room_view, name = 'room'),
	path('messages/', views.messages_view, name = 'messages')
]