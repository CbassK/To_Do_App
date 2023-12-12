from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from task.views import RegisterView, UserLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('task.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
