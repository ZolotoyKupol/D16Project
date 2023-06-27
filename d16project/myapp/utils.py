from django.core.mail import send_mail
from django.conf import settings


def send_notification_email(to_email, ad_title, message):
    subject = 'Response Accepted'
    body = f'Your response on the ad "{ad_title}" has been accepted. {message}'
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, body, from_email, [to_email])
