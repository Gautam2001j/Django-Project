from django.shortcuts import render , redirect
from django.contrib.auth import login , logout ,authenticate
from.middlewares import guest
from .models import  StudentInfo , User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
import requests

# Create your views here.
import logging
logger = logging.getLogger(__name__)

def home_page(request):
    return render(request,'home.html')


def courses(request):
    return render(request,'courses.html')


def instructors(request):
    return render(request,'instructors.html')

@guest
def sign_up_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobilenumber = request.POST.get('mobilenumber')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if username and email and mobilenumber and password1 == password2:
            user = User.objects.create_user(username=username, email=email, mobilenumber=mobilenumber, password=password1)
            user.save()
            login(request,user)
            return redirect('signin')
        else:
            error_message = "All fields are required."
            return render(request, 'signup.html', {'error_message': error_message})
    else:
        return render(request, 'signup.html')

@guest
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            print("Authenticated user:", user) 
            if user is not None and user.is_active:
                login(request, user)
                logger.info(f"User {username} logged in successfully.")
                return redirect('studentinfo')
            else:
                logger.error("Authentication failed for user: %s", username)
                error_message = "Invalid username or password."
                return render(request, 'signin.html', {'error_message': error_message})
        else:
            error_message = "All fields are required."
            return render(request, 'signin.html', {'error_message': error_message})
    else:
        return render(request, 'signin.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def student_info_form(request):
    if request.user.is_authenticated:
        if StudentInfo.objects.filter(email=request.user.email).exists():
            student_data = StudentInfo.objects.get(email=request.user.email)
            preferences = {
                'preference_1': student_data.preference_1,
                'preference_2': student_data.preference_2,
                'preference_3': student_data.preference_3
            }
            return render(request, 'results.html', {'message': 'Your response is successfully recorded.'})
        else:
            if request.method == 'POST':
                full_name = request.POST.get('fullName')
                email = request.POST.get('email')
                phone_number = request.POST.get('phone')
                address = request.POST.get('address')
                math_marks_hs = int(request.POST.get('math'))
                science_marks_hs = int(request.POST.get('science'))
                english_marks_hs = int(request.POST.get('english'))
                hindi_marks_hs = int(request.POST.get('hindi'))
                physics_marks_10p2 = int(request.POST.get('physics'))
                chemistry_marks_10p2 = int(request.POST.get('chemistry'))
                mathematics_marks_10p2 = int(request.POST.get('maths'))
                preference_1 = request.POST.get('preference1')
                preference_2 = request.POST.get('preference2')
                preference_3 = request.POST.get('preference3')

                total_hs_marks = math_marks_hs + science_marks_hs + english_marks_hs + hindi_marks_hs
                hs_percentage = round(total_hs_marks / 4, 2) if total_hs_marks > 0 else None

                total_10p2_marks = physics_marks_10p2 + chemistry_marks_10p2 + mathematics_marks_10p2
                marks_10p2_percentage = round(total_10p2_marks / 3, 2) if total_10p2_marks > 0 else None

                if full_name and email and phone_number and address and math_marks_hs and science_marks_hs and english_marks_hs and hindi_marks_hs and physics_marks_10p2 and chemistry_marks_10p2 and mathematics_marks_10p2:
                    student = StudentInfo(
                        full_name=full_name,
                        email=email,
                        phone_number=phone_number,
                        address=address,
                        math_marks_hs=math_marks_hs,
                        science_marks_hs=science_marks_hs,
                        english_marks_hs=english_marks_hs,
                        hindi_marks_hs=hindi_marks_hs,
                        hs_percentage=hs_percentage,
                        physics_marks_10p2=physics_marks_10p2,
                        chemistry_marks_10p2=chemistry_marks_10p2,
                        mathematics_marks_10p2=mathematics_marks_10p2,
                        marks_10p2_percentage=marks_10p2_percentage,
                        preference_1=preference_1,
                        preference_2=preference_2,
                        preference_3=preference_3,
                    )
                    student.save()
                    return redirect('studentinfo')
                else:
                    error_message = "All fields are required."
                    return render(request, 'student_report.html', {'error_message': error_message})
            else:
                return render(request, 'student_report.html')
    else:
        return redirect('signin')
    

def admin(request):
    if request.method == 'POST':
        admin_username = request.POST.get('admin_username')
        admin_password = request.POST.get('admin_password')
        if admin_username and admin_password:
            user = authenticate(username=admin_username, password=admin_password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admindashboard')
            else:
                error_message = "Invalid admin username or password."
                return render(request, 'admin.html', {'error_message': error_message})
        else:
            error_message = "All fields are required."
            return render(request, 'admin.html', {'error_message': error_message})
    else:
        return render(request,'admin.html')
    
    
@login_required
def admin_dashboard(request):
    students = StudentInfo.objects.all()
    return render(request, 'admin_dashboard.html', {'students': students})

@login_required
def assign_branch(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        branch = request.POST.get('branch')
        student = StudentInfo.objects.get(pk=student_id)
        student.branch = branch
        student.save()
    return redirect('admindashboard')

@login_required
def success_message(request):
    if request.user.is_authenticated:
        student = StudentInfo.objects.filter(user=request.user).first()
        assigned_branch = student.branch if student else None
    else:
        assigned_branch = None

    return render(request, 'results.html', {'assigned_branch': assigned_branch})