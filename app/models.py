from django.db import models

# Create your models here.

class UserMaster(models.Model):
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    otp = models.IntegerField()
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_created = models.DateTimeField(auto_now_add=True)
    is_update = models.DateTimeField(auto_now_add=True)

class Candidate(models.Model):
    user_id = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    cit = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    dob = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to="img/condidate")

class Company(models.Model):
    user_id = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    company_name = models.CharField(max_length=150)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    hr_pic = models.ImageField(upload_to="img/company/hr", default="path/to/default/image.jpg")
    company_logo = models.ImageField(upload_to="img/company/logo")

class JobDetails(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, default=None)
    jobname = models.CharField(max_length=250)
    companyname = models.CharField(max_length=250)
    companyaddress = models.CharField(max_length=250)
    jobdescription = models.CharField(max_length=500)
    qualification = models.CharField(max_length=250)
    responsibilities = models.CharField(max_length=250)
    locations = models.CharField(max_length=250)
    companywebsite = models.CharField(max_length=250)
    companyemail = models.CharField(max_length=250)
    companycontact = models.CharField(max_length=50)
    salarypackage = models.CharField(max_length=250)
    jobtype = models.CharField(max_length=250, default=None)
    experience = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="img/jobpost", default=None)
