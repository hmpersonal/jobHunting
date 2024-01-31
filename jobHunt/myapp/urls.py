from django.urls import path
from .views import index
from .views import send_receive_request  # この行でビューをインポート

urlpatterns = [
    path('', index, name='index'),
    path('send_receive_request/', send_receive_request, name='send_receive_request'),
]