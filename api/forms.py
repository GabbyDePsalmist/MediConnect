from django import forms
from .models import Doctor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# ───── Appointment Booking Form ─────────────────────────
class AppointmentForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all())
    date = forms.DateField(widget=forms.SelectDateWidget)
    time_slot = forms.ChoiceField(choices=[
        ('08:00', '08:00 – 10:00'),
        ('10:00', '10:00 – 12:00'),
        ('12:00', '12:00 – 14:00'),
        ('14:00', '14:00 – 16:00'),
        ('16:00', '16:00 – 18:00'),
    ])

# ───── Payment Form ─────────────────────────────────────
class PaymentForm(forms.Form):
    card_number = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'})
    )
    expiry = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={'placeholder': 'MM/YY'})
    )
    cvv = forms.CharField(
        max_length=3,
        widget=forms.PasswordInput(attrs={'placeholder': 'CVV'})
    )

# ───── Role Choices ─────────────────────────────────────
ROLE_CHOICES = [
    ('doctor', 'Doctor'),
    ('patient', 'Patient'),
    ('admin', 'Admin'),
]

# ───── Custom Registration Form ─────────────────────────
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Register as')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role']
