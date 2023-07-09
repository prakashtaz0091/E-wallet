from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class UserRegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('account:login')


class UserLoginView(LoginView):
    template_name = 'account/login.html'

    def get_success_url(self):
        return reverse_lazy('wallet:home')


class UserLogoutView(LogoutView):
    template_name = 'account/logout.html'


