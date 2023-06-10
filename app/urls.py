from django.urls import path, include
from app import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
###################################====Candidate Side URL====############################
    path("", views.CandidateIndexPage, name="index"),
    path("home/", views.HomePage, name="home"),
    path("about/", views.AboutPage, name="about"),
    path("blog/", views.BlogPage, name="blog"),
    path("contact/", views.ContactPage, name="contact"),
    path("signup/", views.SignupPage, name="register"),
    path("login/", views.LoginPage, name="login"),
    path("logout/", views.LogoutPage, name="logout"),
    path("otp/", views.OtpPage, name="otpverify"),
    path("new-post/", views.NewPostPage, name="new-post"),
    path("job-post/", views.JobPostPage, name="job-post"),
    path('test-session/', views.test_session, name='test-session'),
     # path("profile/", views.ProfilePage, name="candidate"),
    path("profile/<int:pk>", views.ProfilePage, name="profile"),
    path("updateprofile/<int:pk>", views.UpdateProfilePage, name="updateprofile"),

############################====Company Side URL====##########################################
    path("company/", views.CompanyIndexPage, name="company"),
    path("company-profile/", views.CompanyProfilePage, name="company-profile"),
    path("jobpost/<int:pk>", views.CompanyJobPostPage, name="jobpost"),
    path("joblist/", views.CompanyJobListPage, name="joblist"),
    path("jobupdate/<int:pk>", views.CompanyJobDetailSubmitPage, name="jobupdate"),

#################################### ADMIN SIDE ###########################################    
    # path("admin-login/", views.AdminLoginPage, name="admin-login"),
    path("admin-login/", views.AdminIndexPage, name="admin-login"),
    path("admin/", views.AdminPage, name="admin"),
    path("adminpage/", views.AdminLoginPage, name="adminpage"),
    path("admin-user-list/", views.AdminUserList, name="userlist"),
    path("admin-company-list/", views.AdminCompanyList, name="companylist"),
    path("user-delete/<int:pk>", views.UserDelete, name="userdelete"),
    path("verify-company/<int:pk>", views.VerifyCompanyPage, name="verifycompany"),
    path("verify/<int:pk>", views.VerifyCompany, name="verify"),
    path("company-delete/<int:pk>", views.CompanyDelete, name="companydelete"),   
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)