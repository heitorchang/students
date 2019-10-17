from datetime import datetime
from django.shortcuts import render

def signup_view(request):
    now = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
    fake_email = f"hello{now}@hellokey.com"
    return fake_email
    
