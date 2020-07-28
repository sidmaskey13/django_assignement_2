from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.views import View
from django.views.generic import UpdateView
from .utils import token_generator
from django.contrib import messages
from .forms import LoginForm, SignUpForm, ProfilePicForm
from django.core.files.storage import FileSystemStorage
from .models import UserDetail
User = get_user_model()


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if not user.is_active:
                messages.success(request, 'Email not verified')

            if user:
                login(request, user)
                return redirect('blog:list')
        return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('/')


class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )
            user.is_active = False
            user.save()
            user.set_password(form.cleaned_data['password'])
            user.save()

            # send activation email
            current_site = get_current_site(request)
            email_body = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            }
            link = reverse('activate', kwargs={
                'uidb64': email_body['uid'], 'token': email_body['token']})
            email_subject = 'Activate your account'
            activate_url = 'http://' + current_site.domain + link
            email = EmailMessage(
                email_subject,
                'Hi ' + user.username + ', Please the link below to activate your account \n' + activate_url,
                settings.EMAIL_HOST_USER,
                [form.cleaned_data['email']],
            )
            email.send(fail_silently=False)

            # set profile pic
            if request.FILES['myfile']:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)

                profile = UserDetail()
                profile.user = user
                profile.profile_pic = uploaded_file_url
                profile.save()

            return redirect('login')
        else:
            form = SignUpForm()
        return render(request, 'signup.html', {'form': form})


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')




