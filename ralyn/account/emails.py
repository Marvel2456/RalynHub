from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
from .utils import token_generator

def activate_email(request, user, to_email):
    mail_subject = "Activate your account"
    message = render_to_string("account/activate_account.html", {
        'user': user.email,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please visit your email {to_email} inbox and click on \
            recieved activation link to confirm and complete the registration. Note: if email is not in your \
                inbox, check your spam folder as well.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check that the email is correct.')