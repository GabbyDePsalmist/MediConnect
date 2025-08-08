from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, time, timedelta
from django.contrib import messages as django_messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import make_aware, now as tz_now

from .models import Doctor, Patient, Appointment, Message
from .serializers import DoctorSerializer, PatientSerializer, AppointmentSerializer, MessageSerializer
from .forms import AppointmentForm, PaymentForm, CustomUserCreationForm


# ─── REST API ViewSets ────────────────────────────────────────────────────────

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    @action(detail=False, methods=['get'])
    def available_slots(self, request):
        doctor_id = request.GET.get('doctor_id')
        date_str = request.GET.get('date')

        if not doctor_id or not date_str:
            return Response({"error": "doctor_id and date are required"}, status=400)

        booked_slots = Appointment.objects.filter(
            doctor_id=doctor_id,
            date=date_str
        ).values_list('time_slot', flat=True)

        all_slots = [time(h, 0) for h in range(8, 18, 2)]  # 2-hour blocks
        available = [slot.strftime('%H:%M') for slot in all_slots if slot not in booked_slots]

        return Response({"available_slots": available})


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


# ─── Authentication Views ─────────────────────────────────────────────────────

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            role = form.cleaned_data['role']
            user.save()

            if role == 'doctor':
                Doctor.objects.create(user=user)
            elif role == 'patient':
                Patient.objects.create(user=user)
            elif role == 'admin':
                user.is_staff = True
                user.save()

            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'api/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'api/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── Home View ────────────────────────────────────────────────────────────────

@login_required
def home_view(request):
    user = request.user
    is_doctor = hasattr(user, 'doctor')
    is_patient = hasattr(user, 'patient')

    appointments = None
    if is_doctor:
        appointments = Appointment.objects.filter(doctor__user=user).order_by('date', 'time_slot')
    elif is_patient:
        appointments = Appointment.objects.filter(patient__user=user).order_by('date', 'time_slot')
    
    unread_count = Message.objects.filter(receiver=request.user, is_read=False).count()

    return render(request, 'api/home.html', {
        'appointments': appointments,
        'is_doctor': is_doctor,
        'is_patient': is_patient,
        'unread_count': unread_count
    })


# ─── Unified Appointments View ────────────────────────────────────────────────

@login_required
def my_appointments_view(request):
    user = request.user
    now = tz_now()

    if hasattr(user, 'doctor'):
        appointments = Appointment.objects.filter(doctor__user=user).order_by('date', 'time_slot')
    elif hasattr(user, 'patient'):
        appointments = Appointment.objects.filter(patient__user=user).order_by('date', 'time_slot')
    else:
        return redirect('home')

    for appt in appointments:
        appt_datetime = make_aware(datetime.combine(appt.date, appt.time_slot))
        appt.can_cancel = (appt_datetime - now) > timedelta(hours=24)

    return render(request, 'api/my_appointments.html', {
        'appointments': appointments,
        'now': now,
    })


# ─── Book Appointment ─────────────────────────────────────────────────────────

@login_required
def book_appointment(request):
    show_payment = False
    appointment_form = AppointmentForm()
    payment_form = PaymentForm()

    if request.method == 'POST':
        if 'select_slot' in request.POST:
            appointment_form = AppointmentForm(request.POST)
            if appointment_form.is_valid():
                request.session['appointment_data'] = {
                    'doctor_id': appointment_form.cleaned_data['doctor'].id,
                    'date': str(appointment_form.cleaned_data['date']),
                    'time_slot': appointment_form.cleaned_data['time_slot'],
                }
                show_payment = True
            else:
                django_messages.error(request, "Please complete the appointment form correctly.")

        elif 'process_payment' in request.POST:
            payment_form = PaymentForm(request.POST)
            appointment_data = request.session.get('appointment_data')

            if appointment_data and payment_form.is_valid():
                try:
                    doctor = Doctor.objects.get(id=appointment_data['doctor_id'])
                    date = appointment_data['date']
                    time_slot = appointment_data['time_slot']
                    patient = Patient.objects.get(user=request.user)

                    if Appointment.objects.filter(doctor=doctor, date=date, time_slot=time_slot).exists():
                        django_messages.error(request, "This time slot is already booked.")
                        return redirect('book_appointment')

                    appointment = Appointment.objects.create(
                        doctor=doctor,
                        patient=patient,
                        date=date,
                        time_slot=datetime.strptime(time_slot, '%H:%M').time(),
                        is_paid=True,
                        status='Confirmed'
                    )

                    request.session.pop('appointment_data', None)

                    Message.objects.create(
                        sender=request.user,
                        receiver=doctor.user,
                        appointment=appointment,
                        content=f"New appointment booked with you on {date} at {time_slot}."
                    )
                    Message.objects.create(
                        sender=doctor.user,
                        receiver=request.user,
                        appointment=appointment,
                        content=f"Your appointment with Dr. {doctor.user.last_name} is confirmed for {date} at {time_slot}."
                    )

                    return render(request, 'api/booking_success.html', {'appointment': appointment})
                except Exception as e:
                    django_messages.error(request, f"Error: {e}")
            else:
                show_payment = True
                if not appointment_data:
                    django_messages.error(request, "Session expired. Please start again.")

    return render(request, 'api/book_appointment.html', {
        'appointment_form': appointment_form,
        'payment_form': payment_form,
        'show_payment': show_payment
    })


# ─── Cancel Appointment ───────────────────────────────────────────────────────

@login_required
def cancel_appointment(request, appointment_id=None):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')

    if not appointment_id:
        django_messages.error(request, "No appointment selected to cancel.")
        return redirect('my_appointments')

    appointment = get_object_or_404(Appointment, id=appointment_id)

    user = request.user
    if user != appointment.patient.user and user != appointment.doctor.user:
        django_messages.error(request, "You are not authorized to cancel this appointment.")
        return redirect('my_appointments')

    appointment_dt = make_aware(datetime.combine(appointment.date, appointment.time_slot))
    current_time = tz_now()

    if appointment_dt <= current_time + timedelta(hours=24):
        django_messages.error(request, "You can't cancel appointments less than 24 hours in advance.")
        return redirect('my_appointments')

    appointment.status = 'Cancelled'
    appointment.save()

    receiver = appointment.doctor.user if user == appointment.patient.user else appointment.patient.user
    role = "patient" if user == appointment.patient.user else "doctor"

    Message.objects.create(
        sender=user,
        receiver=receiver,
        appointment=appointment,
        content=f"Appointment on {appointment.date} at {appointment.time_slot.strftime('%I:%M %p')} was cancelled by the {role}."
    )

    django_messages.success(request, "Appointment cancelled successfully.")
    return redirect('my_appointments')


# ─── Messages Inbox ───────────────────────────────────────────────────────────

@login_required
def message_list_view(request):
    inbox = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    inbox.filter(is_read=False).update(is_read=True)
    return render(request, 'api/messages.html', {'messages': inbox})
