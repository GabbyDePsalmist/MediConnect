from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DoctorViewSet,
    PatientViewSet,
    AppointmentViewSet,
    MessageViewSet,
    register_view,
    login_view,
    logout_view,
    home_view,
    book_appointment,
    cancel_appointment,
    message_list_view,
    my_appointments_view
)

# DRF Router for API endpoints
router = DefaultRouter()
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'messages', MessageViewSet)

# URL patterns
urlpatterns = [
    path('', home_view, name='home'),
    path('api/', include(router.urls)),              # REST API endpoints
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('book/', book_appointment, name='book_appointment'),
    path('appointments/', my_appointments_view, name='my_appointments'),
    path('appointment/cancel/<int:appointment_id>/', cancel_appointment, name='cancel_appointment'),
    # path('appointment/cancel/', cancel_appointment, name='cancel_appointment'),
    path('messages/', message_list_view, name='messages'),
]
