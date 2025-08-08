# MediConnect
The medical consultation booking web application was designed to streamline the process of scheduling, managing, and confirming doctor’s appointments online. The primary goal was to enhance communication between patients and healthcare providers while offering a convenient, self-service solution for appointment management.
________________________________________
📘 MediConnect — Doctor Appointment Booking System
MediConnect is a web-based appointment booking platform where patients can schedule appointments with doctors, receive confirmations, and communicate via a built-in messaging system.
 
________________________________________
🚀 Features
•	Doctor & patient user roles
•	Appointment scheduling with payment confirmation
•	Role-based dashboard
•	Inbox with message notifications
•	Responsive Bootstrap UI
________________________________________
🧰 Requirements
Before you start, make sure you have the following installed:
•	Python 3.8+
•	pip (Python package manager)
•	Git (optional, for cloning the repo)
________________________________________
🧪 Installation
# 1. Clone the repository (or download it)
git clone https://github.com/GabbyDePsalmist/MediConnect

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  

# 3. Install required packages
pip install -r requirements.txt

# 4. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create a superuser
python manage.py createsuperuser

# 6. Load any static files
python manage.py collectstatic

# 7. Run the server
python manage.py runserver
________________________________________
📁 Directory Structure (Simplified)
mediconnect/
│
├── api/               # Core app: views, models, forms, etc.
├── templates/api/     # HTML templates
├── static/            # Static files (CSS, JS, images)
├── manage.py
├── requirements.txt
└── README.md
________________________________________
🔑 Admin Login
After running the server, access the admin panel:
•	URL: http://127.0.0.1:8000/admin/
•	Use the credentials from createsuperuser.
________________________________________
📦 Dependencies
If requirements.txt is missing, here's a basic one you can generate:
# Core Backend
Django==4.2.7
djangorestframework==3.14.0

# Database
sqlite3 # Built-in (explicitly listed for clarity)

To generate your own:
pip freeze > requirements.txt
________________________________________
💬 Default URLs
•	Homepage: http://127.0.0.1:8000/
•	Login: /login/
•	Register: /register/
•	Book Appointment: /book/
•	Appointments: /appointments/
•	Messages: /messages/
 
________________________________________
## Test Actions and Expected Results

### Admin Panel
- **Action**: Login as Admin in the Admin Panel  
  **Expected Result**: Session is created, redirected to Admin dashboard

### Appointment Booking
- **Action**: Book New Appointment  
  **Expected Result**: 
  - Appointment is stored in database
  - Patient fills doctor, time/date, and payment details
  - Confirmation message is sent after payment
  - Status shows as "Confirmed" in My Appointments

- **Action**: Patient books via Web UI  
  **Expected Result**: 
  - Appointment saved to database
  - User receives confirmation message

### Appointment Management
- **Action**: Click "Cancel" on appointment  
  **Expected Result**: 
  - Appointment is deleted from database
  - UI updates in real-time showing cancelled status

- **Action**: View Appointment Dashboard  
  **Expected Result**: 
  - Upcoming appointments are listed for both doctors and patients
  - Each appointment has "Cancel" option

### System Validation
- **Action**: Attempt double-booking  
  **Expected Result**: 
  - Only one booking succeeds
  - Subsequent attempt shows "Slot no longer available" message________________________________________
🖼 Static Assets
Place images like default_avatar.png inside:
static/
________________________________________
📌 Tips
•	For styling, Bootstrap 5 is used.
•	Use DEBUG = True for development in settings.py.
•	For production, remember to set up a proper web server and database.










