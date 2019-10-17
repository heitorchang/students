from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def signup_view(request):
    if request.method == "POST":
        now = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
        username = request.POST['username']
        errors = []

        try:
            checkUser = User.objects.get(username=username)
            userExists = True
        except:
            userExists = False

        if userExists:
            errors.append("Username is already taken.")

        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            errors.append("Passwords do not match.")

        if len(password1) < 8 or len(password2) < 8:
            errors.append("Password must be at least 8 characters long.")

        if password1.isdigit() or password2.isdigit():
            errors.append("Password cannot be entirely numeric.")
            
        if errors:
            return render(request, "registration/signup_form.html",
                          {'existingUsername': request.POST['username'],
                           'errors': errors})
            
        fake_email = f"hello{now}@hellokey.com"

        User.objects.create_user(username=username,
                                 email=fake_email,
                                 password=password1)

        new_user = authenticate(username=username, password=password1)
        login(request, new_user)
        return redirect("index")

    else:
        return render(request, "registration/signup_form.html")
    
