from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from .forms import ImageUploadForm, InfoForm, NewUserForm
from django.contrib.auth import authenticate, login, logout
from .forms import NewUserForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import Doctor, Info

 
# Create your views here.
def homepage(request):
    return render(request, 'home.html')

# def appointment(request):
#     if request.method == 'POST':
#         print('yes')
#         date = request.POST['date']
#         patient_name = request.POST['patient_name']
#         doctor = request.POST['doctor']
#         time = request.POST['time']
#         user = request.user
#         appointments=Info(user=user,date=date,patient_name=patient_name,doctor=doctor,time=time)
#         appointments.save()
#         print(user)
#         return redirect('homepage')
#     doctor=Doctor.objects.all()
#     return render(request, 'appointment.html',{'doctor':doctor})

def appointment(request):
    if request.method == 'POST':
        form = InfoForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            return redirect('appointment')
    else:
        form =  InfoForm()
    return render(request, 'appointment.html', {'form':form})

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend'
)
            return redirect('homepage')
        messages.error(request, 'Invalid data')
    form = NewUserForm()
    return render(request, 'register.html', {'form':form})


# def login_request(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password")
#             user = authenticate(username = username, password= password)
#             if user is not None:
#                 login(request, user)
#                 return redirect("appointment")
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})

# def login_request(request):
# 	if request.method == "POST":
# 		form = AuthenticationForm(request.POST)
# 		if form.is_valid():
# 			username = form.cleaned_data.get('username')
# 			print(form)
# 			password = form.cleaned_data.get('password')
# 			print(form.cleaned_data)
# 			user = authenticate(username=username, password=password)
# 		    if user is not None:
# 				login(request, user)
# 				return redirect("appointment")
#             else:
#                 messages.error(request, "Invalid Username or Password")
#         else:
#             messages.error(request, "Invalid Username or password")
# 	form = AuthenticationForm()
# 	return render(request=request, template_name="login.html", context={'form':form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('appointment')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    
    form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})


def logout_request(request):
    logout(request)

    return redirect('login')

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import mail_managers, send_mail
from django.contrib.auth.models import User
def password_request(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            user = User.objects.get(email=data)
            if user:
                
                subject = " Password Reset Requested"
                email_template_name = 'password_reset_email.txt'
                c = {
                    'email': user.email,
                    'domain': '127.0.0.1:8000',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'site': 'Demo Website',
                    'user': user,
                    'token':  default_token_generator.make_token(user),
                    'protocol' : 'http',
                }
                email = render_to_string(email_template_name, c)
                send_mail(subject, email, 'abc@gmail.com', [user.email], fail_silently=False)
                return redirect('/password_reset/done/')
    password_reset_form = PasswordResetForm()
    return render(request = request, template_name='password_reset.html', context={'password_reset_form': password_reset_form} )


def user_details(request):
    if request.user.is_authenticated:
        user = request.user    
        appoint = Info.objects.filter(user = user)        
        # print(appoint)
        appointments = []
        for a in appoint:
            # print(a.date)
            appointments.append(a)
    
            
        
    return render(request, 'dashboard.html' , {'appointments': appointments})

def report(request):
    if request.method == 'POST':
        
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect ('dashboard')
    else:
        form = ImageUploadForm()
    return render(request, 'report.html', {'report_form':form})


def delete_appointment(request, id = id):
    obj=Info.objects.get(pk=id)
    obj.delete()
    return redirect(user_details)


def update_appointment(request, id = id):
    ect = Info.objects.POST(pk=id)



        