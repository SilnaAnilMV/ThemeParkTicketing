from django.urls import path,include
from Ticketing import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index ,name='index'),
    path('create-bokking/', views.createBooking ,name='create-bokking'),
]    

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)