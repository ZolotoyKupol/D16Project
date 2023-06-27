import random
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistrationForm
from .forms import ConfirmationForm
from .forms import AdForm
from .forms import ResponseForm, NewsletterSubscriptionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Person, Ad, Response, Category


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Отправка письма с кодом подтверждения
            confirmation_code = generate_confirmation_code()
            send_confirmation_email(user.email, confirmation_code)

            # После успешной регистрации перенаправляем пользователя на страницу подтверждения
            return redirect('confirmation')
    else:
        form = RegistrationForm()
    return render(request, 'myapp/register.html', {'form': form})


def generate_confirmation_code():
    # Генерация случайного кода подтверждения
    code = ''
    for _ in range(settings.CONFIRMATION_CODE_LENGTH):
        code += str(random.randint(0, 9))
    return code


def send_confirmation_email(to_email, confirmation_code):
    subject = 'Подтверждение регистрации'
    message = f'Ваш код подтверждения: {confirmation_code}'
    from_email = 'noreply@example.com'
    send_mail(subject, message, from_email, [to_email])


@login_required
def confirmation(request):
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                user = Person.objects.get(email=request.user.email)  # Получаем пользователя по его email
                if code == user.confirmation_code:  # Проверяем код подтверждения
                    user.is_active = True  # Активируем аккаунт пользователя
                    user.save()
                    messages.success(request, 'Account activated successfully!')
                    return redirect('home')  # начальная страница
                else:
                    messages.error(request, 'Invalid confirmation code!')
            except Person.DoesNotExist:
                messages.error(request, 'User not found!')
    else:
        form = ConfirmationForm()
    return render(request, 'myapp/confirmation.html', {'form': form})


def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.owner = request.user
            ad.save()
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm()

    categories = Category.objects.all()
    return render(request, 'myapp/create_ad.html', {'form': form, 'categories': categories})


def edit_ad(request, pk):
    ad = Ad.objects.get(pk=pk)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            ad = form.save()
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)
    return render(request, 'myapp/edit_ad.html', {'form': form, 'ad': ad})


def send_response(request, ad_id):
    ad = Ad.objects.get(id=ad_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.ad = ad
            response.user = request.user
            response.save()

            # Отправка уведомления о новом отклике
            send_notification_email(ad.owner.email, ad.title, response.text)

            return redirect('myapp:ad_detail', ad_id=ad.id)
    else:
        form = ResponseForm()
    return render(request, 'myapp/send_response.html', {'form': form})


def send_notification_email(to_email, ad_title, response_text):
    subject = 'New Response on your Ad'
    message = f'Your ad "{ad_title}" has received a new response:\n\n{response_text}'
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [to_email])


@login_required
def private_page(request):
    user = request.user
    ads = Ad.objects.filter(owner=user)
    responses = Response.objects.filter(ad__owner=user)
    return render(request, 'myapp/private_page.html', {'ads': ads, 'responses': responses})


@login_required
def accept_response(request, response_id):
    response = Response.objects.get(id=response_id)
    if response.ad.owner == request.user:
        response.accepted = True
        response.save()
        send_notification_email(response.user.email, response.ad.title, 'Your response has been accepted.')
        messages.success(request, 'Response accepted successfully!')
    else:
        messages.error(request, 'You are not the owner of this ad.')
    return redirect('private_page')


@login_required
def delete_response(request, response_id):
    response = Response.objects.get(id=response_id)
    if response.ad.owner == request.user:
        response.delete()
        messages.success(request, 'Response deleted successfully!')
    else:
        messages.error(request, 'You are not the owner of this ad.')
    return redirect('private_page')


def create_categories():
    categories = ["Танки", "Хилы", "ДД", "Торговцы", "Гилдмастеры", "Квестгиверы", "Кузнецы", "Кожевники", "Зельевары", "Мастера заклинаний"]
    for category_name in categories:
        Category.objects.get_or_create(name=category_name)


def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have subscribed to the newsletter.')
            return redirect('home')  # любая желаемая страница
    else:
        form = NewsletterSubscriptionForm()
    return render(request, 'myapp/subscribe_newsletter.html', {'form': form})