from django.urls import path, include
from django.http import HttpResponse
from livraria.views import home, logout_user, register_user, book_detail, book_delete, book_add, book_update, book_search, profile_user_view, profile_user_edit, tag_search, page_checkout, pix_payment, boleto_payment, card_payment, finish_purchase, accept_friend_request, reject_friend_request, login_user
# generate_barcode

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name="register" ),
    path('book/<int:id>/', book_detail, name="book"),
    path('delete_book/<int:id>/', book_delete, name="delete_book"),
    path('add_book/', book_add, name="add_book"),
    path('update_book/<int:id>/', book_update, name="update_book"),
    path('search/', book_search, name="book_search" ),
    path('tag_search/', tag_search, name="tag_search" ),
    # path('profile_view/', profile_user_view, name="profile_view" ),
    path('profile_view/<int:id>/', profile_user_view, name="profile_view" ),
    path('profile_edit/', profile_user_edit, name="profile_edit" ),
    path('checkout/', page_checkout, name="page_checkout" ),
    
    path("finish_purchase/", finish_purchase,name="finish_purchase"),
    path("pix_payment", pix_payment, name="pix_payment"),
    path("boleto_payment",boleto_payment, name="boleto_payment"),
    path("card_payment",card_payment, name="card_payment"),
    
    # path('send_friend_request/<int:id>/', send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:id>/', accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:id>/', reject_friend_request, name='reject_friend_request'),
    
    # path("barcode/<str:order_number>/", generate_barcode, name="generate_barcode"),
    
    # path('ratings/', include('star_ratings.urls', namespace='ratings')),
    # send_friend_request
    # path('sobre/', sobre)
]




