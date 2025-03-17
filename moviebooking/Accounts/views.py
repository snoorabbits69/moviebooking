from django.contrib.auth import login
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm

class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("movie_list")

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # Pass the request data explicitly to the form
        if form.is_valid():
            user = form.save(commit=False)  
            user.set_password(form.cleaned_data['password1'])  # Set the password securely
            user.save()  # Save the user to the database
            print("User created:", user)

            login(request, user)  # Log the user in

            return HttpResponseRedirect(self.success_url)
        else:
            print(form.errors)  # Print form errors for debugging
            return self.form_invalid(form)
