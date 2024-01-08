from django.shortcuts import render,HttpResponse,redirect
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from .filters import UserFilter
from . managers import CustomUserManager

from .forms import UploadedFileForm
from .models import UploadedFile, CustomUser

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import UploadedFile
from .serializers import UploadedFileSerializer

from django.core.mail import send_mail



User = get_user_model()
# Create your views here.
# def HomePage(request):
#     return render (request,'home.html')



# def SignupPage(request):
#     if request.method=='POST':
#         uname=request.POST.get('username')
#         email=request.POST.get('email')
#         pass1=request.POST.get('password1')
#         pass2=request.POST.get('password2')

#         if pass1!=pass2:
#             return HttpResponse("Your password and confrom password are not Same!!")
#         else:

#             my_user=User.objects.create_user(uname,email,pass1)
#             my_user.save()
#             return redirect('login')
        



    #return render (request,'signup.html')

# def LoginPage(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         pass1=request.POST.get('pass')
#         user=authenticate(request,username=username,password=pass1)
#         if user is not None:
#             login(request,user)
#             return redirect('home')
#         else:
#             return HttpResponse ("Username or Password is incorrect!!!")

#     return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    # print("abc")
    # messages.success(request, "Logged Out")
    return redirect('signin')


def RegisterPage(request):
    if request.method=='POST':
        public_visibility = False
        email=request.POST.get('email')
        username=request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        public_visibility = request.POST.get('checkbox1')
        # print(public_visibility)

        #print(email)
        form_data = {
                'email': email,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                # 'public_visibility': public_visibility 
            }
        if pass1!=pass2:
            
            messages.error(request, "Your password and confirm password do not match!")
            return render(request, 'register.html', {'form_data': form_data})
        else:
            if public_visibility == 'on':  # Checkbox sent value when checked
                public_visibility = True
            else:
                public_visibility = False  # Checkbox not checked

            # CustomUser = get_user_model()
            # print(public_visibility)
            my_user=CustomUser.objects.create_user(email=email,username=username,first_name=first_name,last_name=last_name,public_visibility=public_visibility,password= pass1)
            # my_user.set_password
            #my_user.public_visibility = public_visibility
            #my_user.save()

            subject = 'Welcome to our platform!'
            message = 'Thank you for registering on our platform. We hope you enjoy your experience!'
            sender_email = '1032200814@mitwpu.edu.in' 
            recipient_email = my_user.email

            send_mail(subject, message, sender_email, [recipient_email])
            return redirect('signin')
    return render (request,'register.html')


def SigninPage(request):
    if(request.user.is_authenticated):
        logout(request)
    if request.method=='POST':
        email=request.POST.get('email')
        pass1=request.POST.get('pass')
        user=authenticate(request,email=email,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect!!")
            # return HttpResponse ("Username or Password is incorrect!!!")
    return render (request,'signin.html')

# def authors_and_sellers(request):
#     CustomUser = get_user_model()
#     user_filter = UserFilter(request.GET, queryset=CustomUser.objects.filter(public_visibility=True))
#     return render(request, 'authors_and_sellers.html', {'filter': user_filter})

def authors_and_sellers(request):
    CustomUser = get_user_model()
    user_filter = CustomUser.objects.filter(public_visibility=True)
    return render(request, 'authors_and_sellers.html', {"users" : user_filter})
    # CustomUser = get_user_model()
    # user_filter = None
    # filter_applied = False
    
    # if request.method == 'GET' and 'filter_users' in request.GET:
    #     user_filter = UserFilter(request.GET, queryset=CustomUser.objects.filter(public_visibility=True))
    #     filter_applied = True
    
    # return render(request, 'authors_and_sellers.html', {'filter': user_filter, 'filter_applied': filter_applied})

def upload_book(request):
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            return redirect('uploaded_files')
    else:
        form = UploadedFileForm()
    return render(request, 'upload_book.html', {'form': form})

def custom_uploaded_files_wrapper(request):
    user_has_files = UploadedFile.objects.filter(user=request.user).exists()

    if user_has_files:
        return uploaded_files(request)
    else:
        return redirect('upload_book')

def uploaded_files(request):
    user_files = UploadedFile.objects.filter(user=request.user)
    # test = UploadedFile.objects.all().order_by('user_id')
    # print(test)
    return render(request, 'uploaded_files.html', {'user_files': user_files})

@login_required(login_url = 'signin')
def IndexPage(request):
    # users = User.objects.all()
    return render (request,'index.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_uploaded_files(request):
    user_files = UploadedFile.objects.filter(user=request.user)
    serializer = UploadedFileSerializer(user_files, many=True)
    return Response(serializer.data)

def send_email_view(request):
    subject = 'Subject of the email'
    message = 'Message content of the email.'
    from_email = 'jawediqbal00248@gmail.com'  
    recipient_list = ['jawediqbal00248@gmail.com']  

    send_mail(subject, message, from_email, recipient_list)

    return HttpResponse('Email sent successfully!')


