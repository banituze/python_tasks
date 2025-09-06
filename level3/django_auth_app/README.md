# Django Web Application with Authentication

This is a complete Django web application that demonstrates user authentication features including registration, login, logout, password reset, and role-based permissions.

## Features

- User registration with email verification
- User login/logout functionality  
- Password reset via email
- Role-based permissions (Admin, Regular User)
- Profile management
- Secure password handling
- Session management
- CSRF protection

## Prerequisites

- Python 3.8+
- Django 4.2+
- Email service (for password reset functionality)

## Installation

1. **Install Dependencies**
   ```bash
   pip install django
   pip install django-crispy-forms
   pip install crispy-bootstrap5
   ```

2. **Setup the Project**
   ```bash
   # Create Django project
   django-admin startproject auth_project .
   
   # Create the main app
   cd auth_project
   python manage.py startapp accounts
   ```

3. **Configure Settings**
   - Update `settings.py` with the provided configuration
   - Configure email settings for password reset functionality

4. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
django_auth_app/
 manage.py
 auth_project/
    __init__.py
    settings.py
    urls.py
    wsgi.py
 accounts/
    __init__.py
    admin.py
    apps.py
    forms.py
    models.py
    urls.py
    views.py
 templates/
    base.html
    home.html
    accounts/
        login.html
        register.html
        profile.html
        password_reset.html
 static/
     css/
         style.css
```

## Usage

1. **Registration**: New users can register with email and password
2. **Login**: Existing users can log in with their credentials
3. **Password Reset**: Users can reset their password via email
4. **Profile Management**: Users can update their profile information
5. **Admin Panel**: Admins can manage users and permissions

## Security Features

- Password hashing using Django's built-in system
- CSRF protection on all forms
- Session management
- Permission-based access control
- Email verification for registration
- Secure password reset tokens

## Customization

The application can be extended with:
- Additional user fields
- Social authentication
- Two-factor authentication
- Custom user roles
- API endpoints
- Advanced profile features

## Testing

Run the test suite with:
```bash
python manage.py test
```

## Deployment Considerations

For production deployment:
1. Set DEBUG = False
2. Configure proper email backend
3. Set up static file serving
4. Use environment variables for sensitive settings
5. Configure HTTPS
6. Set up proper database (PostgreSQL/MySQL)


