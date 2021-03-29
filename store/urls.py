from django.urls import path
from . import views

# app_name = 'app_store'

urlpatterns = [
    path('',views.store,name='store'),
    path('opto/',views.opto,name='opto'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('insert_cart/',views.insert_into_cart,name='insert_cart'),
    path('cart/update_item/',views.update_item_quantity,name='update_item'),
    path('order_details/',views.order_details,name='order_details'),
    path('item_detail/<int:id>',views.item_detail,name='item_detail'),
    path('make_payment/<int:id>',views.make_payment,name='make_payment'),
    path('delete_address/<int:id>', views.delete_address, name='delete_address'),
    path('show_items/<int:id>/',views.show_items,name='show_items'),
    #path('show_items/(<id>)/(<shape>)/',views.show_items,name='show_items'),
    path('show_items_frames/<int:id>/<str:shape>/', views.show_items_frames, name='show_items_frames'),
    path('search/',views.search,name='search'),
    path('update_address/<int:id>',views.update_address,name='update_address'),
    path('face_upload/', views.face_image, name = 'face_upload'),
    path('show_face/', views.display_face, name = 'show_face')
    #path('success', success, name = 'success'),
    #if (settings.DEBUG):
     #   urlpatterns += static(settings.MEDIA_URL,
      #                        document_root=settings.MEDIA_ROOT)
]