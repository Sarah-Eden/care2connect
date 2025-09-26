"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from c2c.views import CreateUserView, UserViewSet, CaseViewSet, ChildViewSet, FosterFamilyViewSet, FosterPlacementViewSet, HealthServiceViewSet, ReminderLogViewSet, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'cases', CaseViewSet, basename='case')
router.register(r'children', ChildViewSet, basename='child')
router.register(r'foster-families', FosterFamilyViewSet, basename='fosterfamily')
router.register(r'foster-placements', FosterPlacementViewSet, basename='fosterplacement')
router.register(r'health-services', HealthServiceViewSet, basename='healthservice')
router.register(r'reminders', ReminderLogViewSet, basename='reminderlog')
				
urlpatterns = [
    path('admin/', admin.site.urls),
	path('api/register/', CreateUserView.as_view(), name='register'),
	path('api/', include(router.urls)),
	path('api/token/', CustomTokenObtainPairView.as_view(), name='get_token'),
	path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh'),
	path('api-auth/', include('rest_framework.urls')),
]
