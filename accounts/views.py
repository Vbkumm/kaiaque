from django.views.generic import UpdateView, ListView, DetailView
from .forms import SignUpForm, UserUpdateForm
from .forms import Profile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, f"Bem vindo a Kaiaque Itajuru {user}")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form = UserUpdateForm
    fields = ('avatar', 'profile_cover', 'first_name', 'last_name', 'email', 'bio', 'location', 'url', 'facebook',
              'instagram', 'you_tube',)
    template_name = 'accounts/my_account.html'
    success_message = f"Perfil salvo com sucesso!"

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'username': self.object.user})


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'accounts/profile.html'

    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username'])


class TermsView(TemplateView):
    template_name = "accounts/terms.html"


class CookiesView(TemplateView):
    template_name = "accounts/cookies.html"
