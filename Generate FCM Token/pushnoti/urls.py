from django.contrib import admin
from django.urls import path
from home.views import index, send, showFirebaseJS

urlpatterns = [
    path('', index, name='index'),
    path('send/', send, name='send'),
    path('firebase-messaging-sw.js', showFirebaseJS, name='show_firebase_js'),
    path('admin/', admin.site.urls),
]

