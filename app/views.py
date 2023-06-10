from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from app.models import *
from random import randint

# Create your views here.
#####################################===Candidate Side Views===###################################################

def CandidateIndexPage(request):
    return render(request, "candidate/index.html")

# @login_required()
def HomePage(request):
    request.session.clear()
    return render(request, "candidate/index.html")

# @login_required()
def AboutPage(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, "candidate/about.html", )

# @login_required()
def BlogPage(request):
    return render(request, "candidate/blog.html")

# @login_required()
def ContactPage(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, "candidate/contact.html")        

# @login_required()
def SignupPage(request):
    if request.method == "POST":
        if request.POST['role']=="Candidate":
            role = request.POST['role']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            email = request.POST['email']
            password = request.POST['password1']
            cpassword = request.POST['password2']
            # print(role,firstname,lastname,email,password,cpassword)
            user = UserMaster.objects.filter(email=email)

            if user:
                message = "User already Exits"
                return render(request, "candidate/signup.html",{'msg':message})
            else:
                if password == cpassword:
                    otp = randint(100000, 999999)
                    newuser = UserMaster.objects.create(role=role,otp=otp,email=email,password=password)  
                    newcandi = Candidate.objects.create(user_id=newuser,firstname=firstname,lastname=lastname)
                    return render(request, "otpverify.html",{'email':email})
        else:
            if request.POST['role']=="Company":
                role = request.POST['role']
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                email = request.POST['email']   
                password = request.POST['password1']
                cpassword = request.POST['password2']
                # print(role,firstname,lastname,email,password,cpassword)
                user = UserMaster.objects.filter(email=email)

            if user:
                message = "User already Exits"
                return render(request, "candidate/signup.html", {'msg':message})
            else:
                if password == cpassword:
                    otp = randint(100000, 999999)
                    newuser = UserMaster.objects.create(role=role,otp=otp,email=email,password=password)  
                    newcandi = Company.objects.create(user_id=newuser,firstname=firstname,lastname=lastname)
                    return render(request, "candidate/otpverify.html", {'email':email})        
    return render(request, "candidate/signup.html")

# @login_required()
def LoginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = UserMaster.objects.get(email=email)
        except UserMaster.DoesNotExist:
            message = "Check Your Email and Password"
            return render(request, "candidate/login.html", {'msg': message})

        if user.password == password:
            if user.role == "Candidate":
                candidate = Candidate.objects.get(user_id=user)
                image_url = candidate.profile_pic.url
                # print(image_url)
                request.session['id'] = user.id
                request.session['role'] = user.role
                request.session['email'] = user.email
                request.session['firstname'] = candidate.firstname
                request.session['lastname'] = candidate.lastname
                # print(request.session['id'])
                request.session.save()
                request.session.set_expiry(300)
                return render(request, "candidate/index.html", {'firstname': candidate.firstname, 'lastname': candidate.lastname, 'role':user.role, 'profile_pic':image_url})
            elif user.role == "Company":
                company = Company.objects.get(user_id=user)
                image_url = company.hr_pic.url
                # print(image_url)
                request.session['id'] = user.id
                request.session['role'] = user.role
                request.session['email'] = user.email
                request.session['firstname'] = company.firstname
                request.session['lastname'] = company.lastname
                request.session.save()
                request.session.set_expiry(300)
                return render(request, "company/index.html", {'firstname': company.firstname, 'lastname': company.lastname, 'role':user.role, 'profile_pic':image_url})
        else:
            message = "Check Your Email and Password"
            return render(request, "login.html", {'msg': message})

    return render(request, "candidate/login.html")

# @login_required()
def OtpPage(request):
    if request.user.is_authenticated:
        logout(request)
    email = request.POST['email']
    opt = int(request.POST['otp'])
    user = UserMaster.objects.get(email=email)

    if user:
        if user.otp == opt:
            message = "OTP verify successfuly"
            return render(request, "candidate/login.html", {'msg':message})
        else:
            message = "OTP is incorrect"
            return render(request, "candidate/otpverify.html", {'msg':message})
    else:
        return render(request, "candidate/signup.html")

    return render(request, "candidate/otpverify.html")    

def JobPostPage(request):
    all_job = JobDetails.objects.all()
    return render(request, "candidate/job-post.html",{'all_job':all_job})

def NewPostPage(request):
    # if  role == "Candidate":
    #     user = UserMaster.objects.all()
    #     candidate = Candidate.objects.get(user_id=user)
    #     image_url = candidate.profile_pic.url
    #     request.session['firstname'] = candidate.firstname
    #     request.session['ladtname'] = candidate.lastname
    #     print(role)
    #     request.session.save()
    #     return render(request, "candidate/new-post.html", {'firstname': company.firstname, 'lastname': company.lastname, 'role':user.role, 'profile_pic':image_url})    
    return render(request, "candidate/new-post.html")

# @login_required(login_url='home')
def LogoutPage(request):
    request.session.clear()
    return redirect('home')

def test_session(request):
    if request.user.is_authenticated:
        firstname = 'John'  # Replace with the actual value
        lastname = 'Doe'  # Replace with the actual value
        print(firstname)
        print(lastname)

        request.session['app:firstname'] = firstname
        request.session['app:lastname'] = lastname
        request.session.save()
    
    return render(request, 'candidate/test_session.html')

def ProfilePage(request,pk):
    user = UserMaster.objects.get(pk=pk)
    role = user.role
    if role == "Candidate":
        candidate = Candidate.objects.get(user_id=pk)
        request.session['id'] = user.id
        return render(request, "candidate/profile.html", {'user':user , 'candidate':candidate})

    else:
        if role == "Company":
            company = Company.objects.get(user_id=pk)
            request.session['id'] = user.id
            return render(request, "candidate/profile.html", {'user':user , 'company':company})

def UpdateProfilePage(request, pk):
    user = UserMaster.objects.get(pk=pk)
    if user.role == "Candidate":
        can = Candidate.objects.get(user_id=user)

        if request.method == 'POST':
            can.firstname = request.POST['firstname']
            can.lastname = request.POST['lastname']
            can.contact = request.POST['phone']
            can.state = request.POST['state']
            can.city = request.POST['city']
            can.address = request.POST['address']
            can.dob = request.POST['dob']
            
            if 'image' in request.FILES:
                can.profile_pic = request.FILES['image']
            
            can.save()
            
            url = f'/updateprofile/{pk}'
            return redirect(url)

    else:
        if user.role == "Company":
            comp = Company.objects.get(user_id=user)

        if request.method == 'POST':
            comp.firstname = request.POST['firstname']
            comp.lastname = request.POST['lastname']
            comp.contact = request.POST['phone']
            comp.state = request.POST['state']
            comp.city = request.POST['city']
            comp.address = request.POST['address']
            comp.dob = request.POST['dob']
            
            if 'image' in request.FILES:
                comp.hr_pic = request.FILES['image']
            
            comp.save()
            
            url = f'/updateprofile/{pk}'
            return redirect(url)

    return render(request, "candidate/profile.html", {'user': user, 'company': comp})

# End Candidate

#####################################===Company Side Views====######################################

# Start Company

def CompanyIndexPage(request):
    return render(request, "company/index.html")    

def CompanyProfilePage(request):
    return render(request, "company/profile.html")    

def CompanyLogoutPage(request):
    pass

def CompanySignupPage(request):
    pass

def CompanyJobPostPage(request,pk):
    user = UserMaster.objects.get(pk=pk)
    role = user.role
    if role == "Company":
        company = Company.objects.get(user_id=pk)
        image_url = company.hr_pic.url
        # print(image_url)
        request.session['id'] = user.id
        request.session['role'] = user.role
        return render(request, "company/jobpost.html", {'user':user , 'role':'user.role', 'company':company, 'profile_pic':image_url})

def CompanyJobDetailSubmitPage(request,pk):
    user = UserMaster.objects.get(pk=pk)
    if user.role == "Company":
        comp = Company.objects.get(user_id=user)
        jobname = request.POST['jobname']
        companyname = request.POST['companyname']
        companyaddress = request.POST['companyaddress']
        jobdescription = request.POST['jobdescription']
        qualification = request.POST['qualification']
        responsibilities = request.POST['responsibilities']
        locations = request.POST['locations']
        companywebsite = request.POST['companywebsite']
        companyemail = request.POST['companyemail']
        companycontact = request.POST['companycontact']
        experience = request.POST['experience']
        salarypackage = request.POST['salarypackage']
        experience = request.POST['experience']
        # if 'logo' in request.FILES:
        logo = request.FILES['logo']
        jobtype = request.POST['jobtype']
        newjob = JobDetails.objects.create(company_id=comp, jobname=jobname, companyname=companyname, companyaddress=companyaddress, jobdescription=jobdescription, qualification=qualification, responsibilities=responsibilities, locations=locations, companywebsite=companywebsite, companyemail=companyemail, companycontact=companycontact, experience=experience, salarypackage=salarypackage, logo=logo, jobtype=jobtype)

        return render(request, "company/jobpost.html")                
    return render(request, "company/jobpost.html")                

def CompanyJobListPage(request):    
    all_job = JobDetails.objects.all()
    return render(request, "company/tables.html",{'all_job':all_job})

########################################  ADMIN SIDE ######################################

# def AdminLoginPage(request):
#     return render(request,"admin/login.html")

def AdminIndexPage(request):
    if 'username' in request.session and 'password' in request.session:
        return render(request,"admin/index.html")
        
    else:
        return redirect('admin')        

def AdminPage(request):
    return render(request,"admin/login.html")        

def AdminLoginPage(request):

    username = request.POST['username']
    password = request.POST['password']

    print(username, password)

    if username == "admin" and password == "admin":
        request.session['username'] = username
        request.session['password'] = password
        print(request.session['username'])
        return redirect('admin-login')

def AdminUserList(request):
    all_user = UserMaster.objects.filter(role="Candidate")
    print(all_user)
    return render(request, "admin/userlist.html", {'all_user':all_user})

def AdminCompanyList(request):
    all_user = UserMaster.objects.filter(role="Company")
    return render(request, "admin/companylist.html", {'all_user':all_user})

def UserDelete(request,pk):
    user = UserMaster.objects.get(pk=pk)
    user.delete()
    return redirect('userlist')

def VerifyCompanyPage(request,pk):
    company = UserMaster.objects.get(pk=pk)
    if company:
        return render(request, "admin/verify.html", {'company':company})

def VerifyCompany(request,pk):
    company = UserMaster.objects.get(pk=pk)
    if company:
        company.is_verified = request.POST['verify']
        company.save()
        return redirect('companylist')

def CompanyDelete(request,pk):
    user = UserMaster.objects.get(pk=pk)
    user.delete()
    return redirect('companylist')        

# def UpdateProfilePage(request, pk):
#     user = UserMaster.objects.get(pk=pk)
#     if user.role == "Candidate":
#         can = Candidate.objects.get(user_id=user)

#         if request.method == 'POST':
#             can.firstname = request.POST['firstname']
#             can.lastname = request.POST['lastname']
#             can.profile_pic = request.FILES['image']
#             can.contact = request.POST['phone']
#             can.state = request.POST['state']
#             can.city = request.POST['city']
#             can.address = request.POST['address']
#             can.dob = request.POST['dob']
#             can.save()
#             url = f'/updateprofile/{pk}'
#             return redirect(url)


# def UpdateProfilePage(request,pk):
#     user = UserMaster.objects.get(pk=pk)
#     if user.role == "Candidate":
#         can = Candidate.objects.get(user_id=user)
#         can['firstname'] = request.POST['firstname']
#         can['lastname'] = request.POST['lastname']
#         can['profile_pic'] = request.FILES['image']
#         can['contact'] = request.POST['phone']
#         can['state'] = request.POST['state']
#         can['city'] = request.POST['city']
#         can['address'] = request.POST['address']
#         can['dob'] = request.POST['dob']
#         can.save()
#         url = f'/company/{pk}'
#         return redirect(url)
    # else:
    #     Exception(NoReverseMatch)
    #     url = f'/company/{user_id}'
    #     return render(request, "profile.html")
    # return render(request, 'profile.html', {'candidate': can})
        

# def LoginPage(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         try:
#             user = UserMaster.objects.get(email=email)
#         except UserMaster.DoesNotExist:
#             message = "Check Your Email and Password"
#             return render(request, "login.html", {'msg': message})
        
#         if user.password == password:
#             if user.role == "Candidate":
#                 candidate = Candidate.objects.get(user_id=user)
#                 request.session['id'] = user.id
#                 request.session['role'] = user.role
#                 request.session['firstname'] = candidate.firstname
#                 request.session['lastname'] = candidate.lastname
#                 request.session['email'] = user.email
#                 return render(request, "index.html", {'firstname': candidate.firstname, 'lastname': candidate.lastname})
#             elif user.role == "Company":
#                 company = Company.objects.get(user_id=user)
#                 request.session['id'] = user.id
#                 request.session['role'] = user.role
#                 request.session['firstname'] = company.firstname
#                 request.session['lastname'] = company.lastname
#                 request.session['email'] = user.email
#                 return render(request, "index.html", {'firstname': company.firstname, 'lastname': company.lastname})
#         else:
#             message = "Check Your Email and Password"
#             return render(request, "login.html", {'msg': message})
#     else:
#         if request.user.is_authenticated:
#             user = UserMaster.objects.get(id=request.session['id'])
#             if user.role == "Candidate":
#                 return render(request, "index.html", {'firstname': request.session['firstname'], 'lastname': request.session['lastname']})
#             elif user.role == "Company":
#                 return render(request, "index.html", {'firstname': request.session['firstname'], 'lastname': request.session['lastname']})

#     return render(request, "login.html")


# @login_required()
# def LoginPage(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         user = UserMaster.objects.get(email=email)

#         if user:
#             if user.password == password and user.role == "Candidate":
#                 can = Candidate.objects.get(user_id = user)
#                 request.session['id'] = user.id
#                 request.session['role'] = user.role
#                 request.session['firstname'] = can.firstname
#                 request.session['lastname'] = can.lastname
#                 request.session['email'] = user.email
#                 return render(request, "index.html", {'firstname': can.firstname, 'lastname': can.lastname})
#             else:
#                 message = "Check Your Email and Password"
#                 render(request, "login.html", {'msg':message})
#         else:
#             if user.password == password and user.role == "Company":
#                 can = Candidate.objects.get(user_id=user)
#                 request.session['id'] = user.id
#                 request.session['role'] = user.role
#                 request.session['firstname'] = user.firstname
#                 request.session['lastname'] = user.lastname
#                 request.session['email'] = user.email
#                 return render(request, "index.html", {'firstname': can.firstname, 'lastname': can.lastname})
#             else:
#                 message = "Check Your Email and Password"
#                 render(request, "login.html", {'msg':message})
#     return render(request, "login.html")

# used
# def LoginPage(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         try:
#             user = UserMaster.objects.get(email=email)
#         except UserMaster.DoesNotExist:
#             message = "Check Your Email and Password"
#             return render(request, "login.html", {'msg':message})
        
#         if user.password == password:
#             if user.role == "Candidate":
#                 candidate = Candidate.objects.get(user_id=user)
#                 request.session['id'] = user.id
#                 request.session['role'] = user.role
#                 request.session['firstname'] = candidate.firstname
#                 request.session['lastname'] = candidate.lastname
#                 request.session['email'] = user.email
#                 request.session.save()
#                 return render(request, "index.html", {'firstname': candidate.firstname, 'lastname': candidate.lastname})
#             elif user.role == "Company":
#                 company = Company.objects.get(user_id=user)
#                 request.session['id'] = user.id
#                 request.session['role'] = user.role
#                 request.session['firstname'] = company.firstname
#                 request.session['lastname'] = company.lastname
#                 request.session['email'] = user.email
#                 request.session.save()
#                 return render(request, "index.html", {'firstname': company.firstname, 'lastname': company.lastname})
#         else:
#             message = "Check Your Email and Password"
#             return render(request, "login.html", {'msg':message})

#     return render(request, "login.html")

