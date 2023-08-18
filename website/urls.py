from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_user, name='login'), can uncomment to redirect to a separate login page
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('application/<int:pk>', views.customer_application, name='application'),
    path('delete_application/<int:pk>', views.delete_application, name='delete_application'),
    path('add_application/', views.add_application, name='add_application'),
    path('update_application/<int:pk>', views.update_application, name='update_application'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
