from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def home(request):
    # Add your skills here
    skills = [
        {"name": "Python / Django", "percent": 90},
        {"name": "React / JavaScript", "percent": 85},
        {"name": "HTML / CSS / Tailwind", "percent": 95},
        {"name": "REST APIs", "percent": 88},
        {"name": "PostgreSQL / SQLite", "percent": 80},
        {"name": "Git / GitHub", "percent": 85},
        {"name": "Three.js / GSAP", "percent": 75},
        {"name": "Docker", "percent": 70},
    ]

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        message = request.POST.get("message", "").strip()

        # Basic validation
        if not all([first_name, last_name, email, message]):
            messages.error(request, "Please fill out all required fields.")
            return render(request, "home.html", {"skills": skills})  # pass skills back on error

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return render(request, "home.html", {"skills": skills})

        # Simple honeypot spam check
        if request.POST.get("website"):
            return redirect("home")

        subject = f"Portfolio Contact from {first_name} {last_name}"
        body = f"""
Name: {first_name} {last_name}
Email: {email}
Phone: {phone or 'Not provided'}

Message:
{message}
        """

        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, "Message sent successfully! I'll get back to you soon.")
        except Exception as e:
            messages.error(request, "Something went wrong. Please try again later.")
            # print(e)  # for debugging

        return redirect("home")

    # GET request
    return render(request, "home.html", {"skills": skills})