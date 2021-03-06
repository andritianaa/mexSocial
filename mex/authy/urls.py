from django.urls import path
from authy.views import UserProfile, Signup, PasswordChange, PasswordChangeDone, EditProfile
from django.contrib.auth import views as authViews

from authy.views import EditPicture, EditName, EditLocation, EditUrl, EditProfile_info



urlpatterns = [
    
    path('profile/edit', EditProfile, name='edit-profile'),
    path('profile/editPicture', EditPicture, name='edit-picture'),
    path('profile/editName', EditName, name='edit-name'),
    path('profile/editLocation', EditLocation, name='edit-location'),
    path('profile/editUrl', EditUrl, name='edit-url'),
    path('profile/editProfile_info', EditProfile_info, name='edit-profile-info'),
   	path('signup/', Signup, name='signup'),
   	path('login/', authViews.LoginView.as_view(template_name='login.html'), name='login'),
   	path('logout/', authViews.LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),
   	path('changepassword/', PasswordChange, name='change_password'),
   	path('changepassword/done', PasswordChangeDone, name='change_password_done'),
   	path('passwordreset/', authViews.PasswordResetView.as_view(), name='password_reset'),
   	path('passwordreset/done', authViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
   	path('passwordreset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   	path('passwordreset/complete/', authViews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]