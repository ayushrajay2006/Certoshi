from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django import forms
from .models import TrustedContact
from django.contrib.auth.decorators import login_required


# Menu Page (Redirects to menu if the user is authenticated)
@login_required
def menu_page(request):
    return render(request, 'menu.html')


# Trusted Contacts Page - Displays all the trusted contacts for the logged-in user
@login_required
def trusted_contacts_page(request):
    contacts = TrustedContact.objects.filter(user=request.user)
    return render(request, 'contact/contacts.html', {'contacts': contacts})


# Form for creating a new Trusted Contact
class TrustedContactForm(forms.ModelForm):
    class Meta:
        model = TrustedContact
        fields = ['name', 'phone', 'email', 'relationship', 'address']


# Home Page (Login Page)
def home(request):
    return render(request, "index.html")


# Signup Page
def signup_page(request):
    return render(request, "signup.html")


# Registration API-based view
@api_view(["POST"])
def register_user(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": f"Username '{username}' is already taken"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    return Response({"message": f"User '{username}' registered successfully"}, status=status.HTTP_201_CREATED)


# API-based User Login
@api_view(["POST"])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return JsonResponse({"error": "Username and password are required"}, status=400)

    # Authenticate the user
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({"redirect_url": "/menu/"}, status=200)
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=401)


# Logout User (Redirect to Home Page)
def logout_user(request):
    logout(request)
    return redirect("home")


# Add Trusted Contact (Form-based view to add a contact)
@login_required
def add_trusted_contact(request):
    if request.method == 'POST':
        form = TrustedContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user  # Associate contact with the logged-in user
            contact.save()
            return redirect('trusted_contacts_page')  # Redirect to the trusted contacts page after saving
    else:
        form = TrustedContactForm()

    return render(request, 'add_contact.html', {'form': form})


# View all Trusted Contacts for the logged-in user (List all contacts)
@login_required
def view_trusted_contacts(request):
    contacts = TrustedContact.objects.filter(user=request.user)
    return render(request, 'view_contacts.html', {'contacts': contacts})


# Additional Helper Functionality: Deleting a Trusted Contact
@login_required
def delete_trusted_contact(request, contact_id):
    try:
        contact = TrustedContact.objects.get(id=contact_id, user=request.user)
        contact.delete()
        return redirect('trusted_contacts_page')  # Redirect to the contacts page after deletion
    except TrustedContact.DoesNotExist:
        return JsonResponse({"error": "Contact not found"}, status=404)
