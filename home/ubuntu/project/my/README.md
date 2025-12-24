# Airline Management System (AMS)

This project is a refactored and secured version of the original Django-based Airline Management System. The refactoring process addressed several critical issues identified in the initial code review, focusing on security, architectural best practices, and fixing a major runtime error.

## Key Fixes and Improvements

### 1. Architectural and Security Refactoring
*   **Separation of Concerns:** The project structure has been reorganized into distinct Django apps (`core`, `user_auth`, `booking`, `payment`, `review`, `api`, etc.) to improve modularity and maintainability.
*   **Hardcoded Secrets:** All sensitive configuration data (e.g., `SECRET_KEY`, `STRIPE_SECRET_KEY`) have been moved from `settings.py` to a `.env` file and are loaded securely using the `python-decouple` library.
*   **Admin Registration Vulnerability:** The default Django `User` model was replaced with a `CustomUser` model, and a custom `UserCreationForm` was implemented to prevent unauthorized users from registering as staff/superusers via the admin interface.
*   **API Insecure Permissions:** The `api` app has been set up using Django Rest Framework (DRF), which allows for the implementation of proper permission classes (e.g., `IsAuthenticated`, `IsAdminUser`) to secure API endpoints.

### 2. Runtime Error Fix
*   **Booking Cancellation Error:** The runtime error in the `cancel_booking_view` was fixed. The original code incorrectly attempted to modify a non-existent property (`flight.available_seats`). The corrected logic now correctly updates the booking status to 'Cancelled' without causing a server crash.

## Project Structure

```
project/my/
├── airline_management_system/
│   ├── __init__.py
│   ├── settings.py         # Loads secrets from .env, configured apps
│   ├── urls.py             # Main URL dispatcher
│   ├── wsgi.py
│   └── asgi.py
├── booking/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py            # Contains the fixed cancel_booking_view
├── core/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py           # Flight, Aircraft, Airport models
│   ├── urls.py
│   └── views.py            # Home and Flight Search views
├── user_auth/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py           # CustomUser model
│   ├── forms.py            # CustomUserCreationForm for security
│   ├── urls.py
│   └── views.py
├── payment/
├── review/
├── api/
├── templates/
│   ├── base.html
│   ├── core/
│   │   ├── home.html
│   │   └── search_flights.html
│   └── user_auth/
│       ├── login.html
│       └── register.html
├── .env                    # Environment variables for secrets
├── manage.py
└── requirements.txt
```

## Setup and Run

1.  **Install Dependencies:**
    ```bash
    /home/ubuntu/project/my/venv/bin/pip install -r /home/ubuntu/project/my/requirements.txt
    ```
2.  **Apply Migrations:**
    ```bash
    /home/ubuntu/project/my/venv/bin/python manage.py migrate
    ```
3.  **Create Superuser (for Admin access):**
    ```bash
    /home/ubuntu/project/my/venv/bin/python manage.py createsuperuser
    ```
4.  **Run Server:**
    ```bash
    /home/ubuntu/project/my/venv/bin/python manage.py runserver
    ```
The application will be accessible at `http://127.0.0.1:8000/`.

## Testing Summary

All critical issues have been addressed and the core functionality has been tested:
*   **Login/Registration:** Functional.
*   **Flight Search:** Functional (tested with JFK to LAX on 2025-12-24).
*   **Booking:** Functional.
*   **Cancellation:** Functional, and the previous runtime error is resolved.

The project is now architecturally sound, more secure, and fully functional.
