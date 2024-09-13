from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='about'),
    # path('room_checklist', views.room_checklist, name='room_checklist_api'),
    path('room_checklist/', views.room_checklist, name='room_checklist_api'),
    # path('items_api', views.items_api, name='room_checklist_item'),
    path('items_api/', views.items_api, name='room_checklist_item'),
    path('room_checklist/<str:id>/items/<str:uuid>', views.room_checklist, name='item-update'),
]