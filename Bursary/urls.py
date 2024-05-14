from django.urls import path
from . import views
from . import views as bursary_views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('', views.index, name='index'), 
     path('requirements/', views.requirements, name='requirements'),
     path('contact/', views.contact, name='contact'),

     path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
     path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
     path('register/', views.register, name='register'),

     path('filling_details/', views.applicant_filling_details, name='filling_details'),
     path('update_details/', views.applicant_updateDetails, name='update_details'),
     path('bursary_application/<int:bursary_id>/', views.bursary_application, name='bursary_application'),

     path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
     path('applicant_dashboard/', views.applicant_dashboard, name='applicant_dashboard'),

     path('profile/', views.profile, name='profile'),
     path('profile/update/', views.profile_update, name='profile_update'),

     #path('bursaries/', views.bursaries, name='bursaries'),
     path('bursaries/<str:pk>/', views.BursaryDetailView, name='bursary_detail'),
     path('applicant/<str:pk_test>/', views.applicant, name="applicant"),
     path('applicant_list/', views.applicant_list, name='applicant_list'),
     path('institution_list/', views.institution_list, name='institution_list'),

     path('add_bursary/', views.add_bursary, name='add_bursary'),
     path('update_bursary/<int:bursary_id>/', views.update_bursary, name='update_bursary'),
     path('delete_bursary/<int:bursary_id>/', views.delete_bursary, name='delete_bursary'),

     path('generate_applicant_pdf/', views.generate_pdf, name='generate_pdf'),

     path('update_institutionContact/<int:institution_id>/', views.update_institutionContact, name='update_institutionContact'),
     path('institution_applicants/<int:institution_id>/', views.institution_applicants, name='institution_applicants'),
     
     #path('edit_bursary_application/<int:bursary_id>/', views.applicant_edit_bursary_application, name='applicant_edit_bursary_application'),
     #path('delete_bursary_application/<int:bursary_id>/', views.delete_bursary, name="applicant_delete_bursary_application"),

     path('reset_password/',
          auth_views.PasswordResetView.as_view(template_name="user/password_reset.html"),
          name="reset_password"),
     
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="user/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="user/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_done.html"),
         name="password_reset_complete"),


]
