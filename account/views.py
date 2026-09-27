from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from .forms import UserEditForm
from account import forms


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('home')
    else:
        form = forms.LoginForm()

    return render(request, 'account/login.html', {'form': form})

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # ولیدیشن ساده
        if not username or not password or not email:
            messages.error(request, 'لطفاً همه فیلدهای ضروری را پر کنید.')
            return render(request, 'account/Register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'این نام کاربری قبلاً ثبت شده است.')
            return render(request, 'account/Register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        messages.success(request, 'ثبت‌نام با موفقیت انجام شد.')
        return redirect('login')

    else:
        return render(request, 'account/Register.html')


@require_POST
def user_logout(request):
    logout(request)
    messages.success(request,'با موفقیت خارج شدید.')
    return redirect('home')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import UserEditForm
from .models import Profile


@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = UserEditForm(request.POST, request.FILES, instance=profile)
        password_form = PasswordChangeForm(request.user, request.POST)

        # پسورد رو فقط وقتی اعتبارسنجی کن که کاربر واقعاً پر کرده باشه
        password_filled = request.POST.get('old_password') or request.POST.get('new_password1')

        profile_valid = profile_form.is_valid()
        password_valid = password_form.is_valid() if password_filled else True

        if profile_valid and password_valid:
            profile_form.save()

            if password_filled:
                user = password_form.save()
                update_session_auth_hash(request, user)  # جلوگیری از logout بعد تغییر پسورد

            messages.success(request, 'اطلاعات با موفقیت ذخیره شد.')
            return redirect('home')
    else:
        profile_form = UserEditForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'account/edit.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })

from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from datetime import datetime, time
from django.utils import timezone

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/profile.html'
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.object

        context['posts_count'] = profile_user.articles.count()
        context['comments_count'] = profile_user.comments.count()

        user_posts = list(profile_user.articles.all())
        for p in user_posts:
            p.activity_type = 'post'
        user_comments = list(profile_user.comments.all())
        for c in user_comments:
            c.activity_type = 'comment'

        def get_sort_key(instance):
            value = instance.created
            if isinstance(value, datetime):
                return value
            naive_dt = datetime.combine(value, time.min)
            return timezone.make_aware(naive_dt)

        recent_activities = sorted(
            chain(user_posts, user_comments),
            key=get_sort_key,
            reverse=True,
        )[:5]

        context['recent_activities'] = recent_activities
        return context