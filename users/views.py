from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import View

from users.forms import UserAccountForm
from users.models import CustomUser


class Profile(DetailView):
    template_name = 'users/profile.html'
    model = CustomUser
    context_object_name = 'profile'


class Account(View):
    template_name = 'users/account.html'

    def get(self, request):
        user = request.user
        form = UserAccountForm(instance=user)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user

        form = UserAccountForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect('users:profile')

        # context = {'form': (form, profile_form)}
        # return render(request, self.template_name, context)
