from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect



def index(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'index.html', c)


#@csrf_protect
def createuser(request):
    if 'username' and 'userpass' in request.POST:
        if request.POST['username'] and request.POST['userpass']:
            username = request.POST['username']
            userpass = request.POST['userpass']
            user = User.objects.create_user(username=username)
            #user.set_password(userpass)
            user.save()
            return render(request, 'result.html', {username: username})



# login in a user
def login_user(request):
    username = request.POST['username']
    userpass = request.POST['userpass']
    user.authenticate(username=username, password=userpass)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page
        else:
            # Return  to a disabled account error message
            pass



# authenticating a user for sessions
def authenticate_user(request):
    if request.user.is_authenticated():
        # redirect to homepage
        pass
    else:
        # redirect to indexpage
        pass


def logout_user(request):
    logout(request)