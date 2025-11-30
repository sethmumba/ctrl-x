from django.test import TestCase

# Create your tests here.
from django.core.mail import send_mail
from django.http import HttpResponse

def test_email(request):
    send_mail(
        'Test SendGrid Email',
        'This is a test email from Django + SendGrid',
        'support@empxautomations.site',  # must be verified
        ['hinzanoseth@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse("Email sent!")
