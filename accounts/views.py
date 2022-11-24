from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, sex_chooses, VerifiedEmail, ResetPassword
from .forms import SignupForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
import requests
from store.views import get_client_ip
from accounts.SendEmail import send_email, send_email_reset_password
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import get_language

def SexValidation(sex):
    for sex_choose in sex_chooses:
        if sex_choose[0] == sex:
            return True
    return False

# Create your views here.
def Login(request):
    if not request.user.is_authenticated:
            
        username = ''
        password = ''
        if request.method == 'POST':
            #get requested fields
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            #get used language
            lang = request.POST.get('lang')

            recaptcha_post = {
                'secret':'6LcNyyojAAAAAOKRdqlfx_A9YxHL9JbEuKEsMFk_',
                'response': request.POST.get('g-recaptcha-response')
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=recaptcha_post).json()
            is_recaptcha_success = r.get('success')
            recaptcha_hostname = r.get('hostname')

            if is_recaptcha_success and recaptcha_hostname == get_client_ip(request):
                    

                
                # authenticate user
                user = authenticate(request, username=username, password=password)
                
                #authenticate user by email
                if not user:
                    get_username_by_email = User.objects.filter(email=username)
                    if get_username_by_email.exists():
                        username = get_username_by_email[0].username
                        user = authenticate(request, username=username, password=password)

                #login user
                if user is not None:

                    login(request, user)

                    return redirect('index')
                else:
                    #validation messages
                    if lang == 'ar':
                        messages.error(request, 'خطأ في اسم المستخدم او كلمة المرور')
                    else:
                        messages.error(request, 'Incorrect username or password')
            else:
                #validation messages
                if lang == 'ar':
                    messages.error(request, 'لا يمكننا تسجيلك يجب تأكيد انك لست روبوت')
                else:
                    messages.error(request, 'We cannot log you in. You must confirm that you are not a robot')
        return render(request, 'accounts/login.html', {'username':username, 'password':password})
    else:
        return redirect('index')


def Signup(request):
    if not request.user.is_authenticated:
            
        obj = {}
            
        form = SignupForm
        obj['form'] = form
        if request.method == 'POST':
            #get used language
            lang = request.POST.get('lang')
            accept = request.POST.get('accept')
            #get requested form
            form = form(request.POST)
            obj['form'] = form


            recaptcha_post = {
                'secret':'6LcNyyojAAAAAOKRdqlfx_A9YxHL9JbEuKEsMFk_',
                'response': request.POST.get('g-recaptcha-response')
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=recaptcha_post).json()
            is_recaptcha_success = r.get('success')
            recaptcha_hostname = r.get('hostname')

            if is_recaptcha_success and recaptcha_hostname == get_client_ip(request):


                
                # get all users
                users = User.objects.all()

                # get requested fields
                first_name = form.data.get('first_name')
                last_name = form.data.get('last_name')
                username = form.data.get('username')
                email = form.data.get('email')
                password = form.data.get('password')
                sex = form.data.get('sex')
                

                #validation
                validation_passed = True
                if lang == 'ar':
                    
                    if not password or len(password) < 6:
                        messages.error(request, 'يجب ان تتكون كلمة المرور على الاقل على 6 احرف او ارقام')
                        validation_passed = False
                    if users.filter(email=email).exists():
                        validation_passed = False
                        messages.error(request, 'هناك مستخدم موجود مسبقاً بهذا البريد الالكتروني')
                    if users.filter(username=username).exists():
                        validation_passed = False
                        messages.error(request, 'هناك مستخدم موجود مسبقاً بهذا الاسم')
                    if not first_name or not last_name:
                        validation_passed = False
                        messages.error(request, 'هناك خطأ في الاسم الاول او خطا في الاسم الثاني')
                    if not sex or not SexValidation(sex):
                        validation_passed = False
                        messages.error(request, 'الرجاء اختيار جنسك')

                    if not accept:
                        validation_passed = False
                        messages.error(request, 'يجب عليك الموافقة على  شروط الاستخدام وسياسة الخصوصية.')
                else:

                    if not password or len(password) < 6:
                        validation_passed = False
                        messages.error(request, 'The password must consist of at least 6 letters or numbers')
                    if users.filter(email=email).exists():
                        validation_passed = False
                        messages.error(request, 'A user already exists with this email')
                    if users.filter(username=username).exists():
                        validation_passed = False
                        messages.error(request, 'There is an existing user with that name')
                    if not first_name or not last_name:
                        validation_passed = False
                        messages.error(request, 'There is a mistake in the first name or a mistake in the second name')
                    if not sex or not SexValidation(sex):
                        validation_passed = False
                        messages.error(request, 'Please select your gender')
                    if not accept:
                        validation_passed = False
                        messages.error(request, 'You must agree to the Terms of Use and Privacy Policy.')

                # check validation
                if not validation_passed:
                    return render(request, 'accounts/signup.html', obj)

                #create user
                user = users.create(first_name=first_name, last_name=last_name, username=username, email=email)
                user.set_password(password)
                user.save()

                #create userprofile
                user_profile = UserProfile.objects.create(user=user, sex=sex)
                user_profile.save()
                domain = get_current_site(request).domain
                verified_email = VerifiedEmail.objects.create(user=user, email=user.email)
                verified_email.save()
                secret = verified_email.secret
                send_email(user.email, user.first_name + ' ' + user.last_name, 'email_validation', lang, domain, f'accounts/EmailValidation/{secret}')

                if lang == 'ar':
                    messages.error(request, 'تم انشاء حسابك بنجاح وتم ارسال رسالة التاكيد الحساب الى بريدك الالكتروني')
                else:
                    messages.error(request, 'Your account has been created successfully and an account confirmation message has been sent to your email')

                #redirect user to login page
                return redirect('login')
            else:
                #validation messages
                if lang == 'ar':
                    messages.error(request, 'لا يمكننا تسجيلك يجب تأكيد انك لست روبوت')
                else:
                    messages.error(request, 'We cannot log you in. You must confirm that you are not a robot')

        return render(request, 'accounts/signup.html', obj)
    else:
        return redirect('index')

def Logout(request):
    if request.user.is_authenticated: 
        logout(request)
        return redirect('login')
    else:
        return redirect('index')


def EmailValidation(request, secret):
    obj = VerifiedEmail.objects.filter(secret=secret, is_finshed=False)
    lang = get_language()
    if obj.exists():
        obj=obj[0]
        user = User.objects.get(id=obj.user.id)
        userprofile = user.userprofile
        userprofile.verified_email = True
        userprofile.save()
        obj.is_finshed = True
        obj.save()
        if lang=='ar':
            messages.success(request, 'تم تأكيد حسابك بنجاح')
        else:
            messages.success(request, 'Your account has been confirmed successfully')
    else:
        if lang=='ar':
            messages.success(request, 'خطاء في تأكيد الحساب')
        else:
            messages.success(request, 'Account verification error')
    return render(request, 'accounts/EmailVaildations.html')

def SendSecretToValitedEmail(request, lang):
    user = request.user
    domain = get_current_site(request).domain
    verified_email = VerifiedEmail.objects.create(user=user, email=user.email)
    verified_email.save()
    secret = verified_email.secret
    send_email(user.email, user.first_name + ' ' + user.last_name, 'email_validation', lang, domain, f'accounts/EmailValidation/{secret}')
    if lang == 'ar':
        messages.success(request, 'تم ارسال رسالة التأكيد على بريدك الالكتروني')
    else:
        messages.success(request, 'A confirmation message has been sent to your email ')
    return redirect('dashboardMain')


def ForgetPassword(request):
    if request.method == 'POST':
            #get used language
            lang = get_language()
            #get requested form
            recaptcha_post = {
                'secret':'6LcNyyojAAAAAOKRdqlfx_A9YxHL9JbEuKEsMFk_',
                'response': request.POST.get('g-recaptcha-response')
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=recaptcha_post).json()
            is_recaptcha_success = r.get('success')
            recaptcha_hostname = r.get('hostname')

            if is_recaptcha_success and recaptcha_hostname == get_client_ip(request):
                username = request.POST.get('username')
                user = User.objects.filter(username=username)
                if not user.exists():
                    user = User.objects.filter(email=username)
                if user.exists():
                    user = user[0]
                    domain = get_current_site(request).domain
                    verified_email = ResetPassword.objects.create(user=user)
                    verified_email.save()
                    secret = verified_email.secret
                    send_email_reset_password(user.email, user.first_name + ' ' + user.last_name, 'email_validation', lang, domain, f'accounts/PasswordReset/{secret}')

                if lang == 'ar':
                    messages.success(request, 'سيتم إرسال رابط إعادة تعيين كلمة المرور إلى بريدك الإلكتروني إذا كان البريد الإلكتروني الذي أدخلته صحيحًا')
                else:
                    messages.success(request, 'A password reset link will be sent to your email if the email you entered is correct')
                



            else:
                #validation messages
                if lang == 'ar':
                    messages.error(request, 'لا يمكننا تسجيلك يجب تأكيد انك لست روبوت')
                else:
                    messages.error(request, 'We cannot log you in. You must confirm that you are not a robot')
    return render(request, 'accounts/ForgetPassword.html')


def PasswordReset(request, secret):
    lang = get_language()
    obj = ResetPassword.objects.filter(secret=secret, is_finshed=False)
    if obj.exists():
        obj = obj[0]
        if request.method == 'POST':
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if password == password2:
                user = obj.user
                user.set_password(password)
                user.save()
                obj.is_finshed = True
                obj.save()
                messages.success(request, 'تم تغير كلمة مرور حسابك بنجاح')
                return redirect('login')
            else:
                if lang == 'ar':
                    messages.success(request, 'كلمة المرور غير متشابهان اعد كتابة كلمة المرور')
                else:
                    messages.success(request, 'The password is not the same. Retype the password')
                
        return render(request, 'accounts/PasswordReset.html')
    

    if lang == 'ar':
        messages.success(request, 'خطاء في اعادة تعيين كلمة مرور الحساب')
    else:
        messages.success(request, 'Error resetting the account password')
    
    return render(request, 'accounts/EmailVaildations.html')