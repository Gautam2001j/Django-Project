from django.urls import path
from .views import home_page, sign_up_view, login_view, courses, instructors, student_info_form ,admin,admin_dashboard,logout_view,assign_branch,success_message

urlpatterns = [
    path('',home_page,name='home'),
    path('sign-up/', sign_up_view , name='signup'),
    path('sign-in/',login_view,name='signin'),
    path('courses/',courses,name='courses'),
    path('instructors/',instructors,name='instructors'),
    path('information-form/',student_info_form,name='studentinfo'),
    path('admin-sign-in/',admin,name='adminsignin'),
    path('admin-dashboard/',admin_dashboard,name='admindashboard'),
    path('logout/',logout_view,name="logout"),
    path('assign_branch/',assign_branch, name='assign_branch'),
    path('results/', success_message)
]


