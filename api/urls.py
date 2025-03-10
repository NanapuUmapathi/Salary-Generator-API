from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet, generate_salary


router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    
    path('', include(router.urls)),

    
    path('salary/<uuid:user_id>/<str:date>/', generate_salary, name="generate_salary"),

    
    path('api/', include(router.urls)),  
    path('api/salary/<uuid:user_id>/<str:date>/', generate_salary, name="api_generate_salary"),
]
