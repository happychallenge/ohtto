from django.contrib import auth
from django.contrib.auth import login, update_session_auth_hash, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.core.checks import messages
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

# Create your views here.
from .models import Relation
from .forms import SignUpForm, ProfileForm, ChangePasswordForm
from .tokens import account_activation_token
from blog.models import Theme

def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, first_name=first_name, 
                            password=password, email=email)

            user = authenticate(
                    username=form.cleaned_data.get('email'),
                    password=form.cleaned_data.get('password')
                )

            if user is not None and user.is_active:
                auth.login(request, user)
            
                Relation.objects.create(from_user=user.profile, to_user=user.profile, status='F')
                Theme.objects.create(name='General Life', author=user, public=True)
            
            # current_site = get_current_site(request)
            # message = render_to_string('account/active_email.html', {
            #         'user': user, 'domain': current_site.domain,
            #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #         'token': account_activation_token.make_token(user),
            #     })

            # mail_subject = 'Activate your account of "IRememberYourPast.com".'
            # email = EmailMessage(mail_subject, message, to=[to_email])
            # email.send()
            
            return render(request, 'account/send_email_for_confirm.html', {'email': email})
        else:
            return render(request, 'account/signup.html', {'form':form})
    else:
        form = SignUpForm()
        return render(request, 'account/signup.html', {'form':form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_encode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        return redirect('user_profile')
    else:
        return render(request, 'account/auth_fail.html')


@login_required
def user_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
                        
            return redirect('user_profile')
    else:
        form = ProfileForm(instance=profile)
        context = {'form':form}
    return render(request, 'account/user_profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect('login')


############################
# Email Check
############################
def checkemail(request):
    data = {}
    email = request.GET.get('email')
    if email:
        email = User.objects.filter(email = email).exists()
        if email:
            data["exists"] = True
        
    return JsonResponse(data, safe=False)


############################
# Change Password
############################
@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 'Your password was successfully changed.')
            return redirect('user_profile')

    else:
        form = ChangePasswordForm(instance=user)

    return render(request, 'account/password.html', {'form': form})


