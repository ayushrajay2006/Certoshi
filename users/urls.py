from django.urls import path
from .views import home, signup_page, login_user, logout_user, menu_page, register_user, trusted_contacts_page, add_trusted_contact, delete_trusted_contact

urlpatterns = [
    path("", home, name="home"),  # Homepage (login)
    path("signup/", signup_page, name="signup"),  # Signup page
    path("login/", login_user, name="login"),  # Login API
    path("logout/", logout_user, name="logout"),  # Logout
    path("menu/", menu_page, name="menu"),  # Menu page
    path("register/", register_user, name="register"),  # Register API
    path("trusted_contacts/", trusted_contacts_page, name="contacts"),  # Trusted contacts page
    path("add_trusted_contact/", add_trusted_contact, name="add_trusted_contact"),  # Add trusted contact
    path("delete_trusted_contact/<int:id>/", delete_trusted_contact, name="delete_trusted_contact"),  # Delete trusted contact
]
