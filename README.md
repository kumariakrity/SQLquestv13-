# SQL Quest

**SQL Quest** is a mini-project developed as part of our college coursework. It’s a web-based platform designed to help users **practice, learn, and master SQL queries** through an interactive and user-friendly interface.

---

#### Tech Stack : Django, MySQL, TailwindCSS

---

## Key Features

- **SQL Topics Covered**: Practice essential SQL concepts like `JOIN`, `GROUP BY`, `HAVING`, and more.
- **User Authentication**: Login system to track individual progress.
- **Progress Tracking**: Real-time updates show how many questions you’ve completed, along with percentage tracking.
- **Auto-Save System**: Your query progress is saved automatically.
- **Help Box**: In-built SQL guide to assist users with syntax and concepts.
- **Hands-on Practice**: Answer SQL questions directly within the platform and get immediate feedback.

---

## Purpose

This platform is built to **help users improve their SQL skills** by solving curated problems and tracking their learning journey. SQL Quest offers a structured and practical approach to practice.

## Architecture

This section describes the overall setup, flow, and components of the SQL Quest system. The platform is built using Django for backend logic, MySQL for persistent data storage, and Tailwind CSS for responsive frontend design.

### Set-up (Django Environment)

Follow the steps below to create and set up a Django project without using a virtual environment:

1. Install Django (if not already installed)

```bash
pip install django
```
2. Create a new Django project
```bash
django-admin startproject sql_quest
cd sql_quest
```
3. Create a new Django app
```bash
python manage.py startapp core
```
4. Create urls.py in your app directory
Inside the app_name folder, create a file named urls.py and add the following:
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # example route
]
```
5. Add your app to INSTALLED_APPS in settings.py
Open project_name/settings.py and add your app name to the INSTALLED_APPS list:
```bash
INSTALLED_APPS = [
    ...
    'core',
]
```
6.  Include your app's URLs in the main urls.py
Edit project_name/urls.py:
```bash
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # include your app's URL config
]
```
7. Create a view in your app
In app_name/views.py, add a simple view:
```bash
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, this is your Django app!")
```
8. Start the server
```bash
python manage.py runserver
```

### Running the Application

To start the Django server and run the application:

1. Open the command prompt or terminal.

2. Navigate to your project directory:

```bash
cd sql_quest
```
3. Start the Django development server:

```bash
python manage.py runserver
```
4. After running the above command, you will see an output like this in the terminal:
```bash
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
June 24, 2025 - 12:00:00
Django version 4.x.x, using settings 'sql_quest.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
5. Open your browser and visit the following URL.
#### This will load the AI_Zen Query application in your browse

### Framework & Toolkit Choices

| Technology     | Purpose                                                        |
|----------------|----------------------------------------------------------------|
| Django         | Backend web framework for handling logic, routes, and views   |
| MySQL          | Relational database for storing users, questions, and progress|
| Tailwind CSS   | Utility-first CSS framework for responsive and modern UI      |
| HTML Templates | Used with Django to render frontend pages dynamically         |
