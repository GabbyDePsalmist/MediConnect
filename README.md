# MediConnect
Doctor Appointment Booking System
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
git clone https://github.com/yourusername/mediconnect.git
cd mediconnect

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

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
Django>=4.0
pytz
sqlparse
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
🖼 Static Assets
Place images like default_avatar.png inside:
static/images/
________________________________________
📌 Tips
•	For styling, Bootstrap 5 is used (via CDN or included in your static files).
•	Use DEBUG = True for development in settings.py.
•	For production, remember to set up a proper web server and database.


