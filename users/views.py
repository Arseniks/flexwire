from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView


# class ActivateUserView(View):
#     template_name = 'users/activate.html'
#
#     def get(self, request, name):
#         user = get_object_or_404(CustomUser, username=name)
#         if (
#             user.date_joined < timezone.now() - timedelta(hours=24)
#             and not user.is_active
#         ):
#             user.delete()
#             messages.error(request, 'Активация аккаунта недействительна')
#         elif user.is_active is False:
#             user.is_active = True
#             user.save()
#             messages.success(request, 'Аккаунт активирован!')
#         else:
#             messages.success(request, 'Аккаунт уже был активирован ранее')
#         return render(request, self.template_name)
#
#
# class RecoveryUserView(View):
#     template_name = 'users/recovery.html'
#
#     def get(self, request, name):
#         user = get_object_or_404(CustomUser, username=name)
#         if (
#             user.profile.freezing_account_date is not None
#             and user.profile.freezing_account_date
#             > timezone.now() + timedelta(days=7)
#             and not user.is_active
#         ):
#             user.delete()
#             messages.error(
#                 request, 'Пользователь удален системой безопасности'
#             )
#         elif user.is_active is False:
#             user.is_active = True
#             user.profile.login_failed_count = 0
#             user.profile.freezing_account_date = None
#             user.profile.save()
#             user.save()
#             messages.success(request, 'Аккаунт восстановлен!')
#         else:
#             messages.success(request, 'Аккаунт не требует восстановления')
#
#         return render(request, self.template_name)
#
#
# class Register(FormView):
#     template_name = 'users/signup.html'
#     form_class = CustomCreationForm
#     success_url = reverse_lazy('users:login')
#
#     def form_valid(self, form):
#         user = form.save(commit=False)
#
#         user.is_active = settings.DEFAULT_USER_ACTIVITY
#         user.save()
#
#         if not settings.DEFAULT_USER_ACTIVITY:
#             send_mail(
#                 'Письмо верификации аккаунта',
#                 'Ваша почта была зарегистрирована на сайте MeetingPoint!\n'
#                 'Для подтверждение регистрации перейдите по ссылке ниже:\n'
#                 'http://127.0.0.1:8000/auth/activate/'
#                 f'{form.cleaned_data["username"]}',
#                 settings.FEEDBACK_MAIL,
#                 [f'{form.cleaned_data["email"]}'],
#                 fail_silently=False,
#             )
#         return super().form_valid(form)
