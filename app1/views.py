from django.shortcuts import render,HttpResponse,redirect
from .models import users
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.
def home(requests):
    return HttpResponse("Hello World!!")

def signup(requests):
    data={"isusername":"hidden","isemail":"hidden"}
    return render(requests,"login/signup.html",data)

def user_login(requests):
    def checkusername(text):
        try:
            uname=users.objects.get(username=text)
            checkpword=uname.password
            return checkpword
        except:
            return 0
        
    if requests.method == "POST":
        uname=requests.POST.get("username")
        pword=requests.POST.get("password")

        iscorrectpword=checkusername(uname)
    
        if(iscorrectpword==0):
            data={"isusername":"visible","ispasswordcorrect":"hidden"}
            return render(requests,"login/login.html",data)
        else:
            if(iscorrectpword==pword):
                # existing_user = users.objects.get(username=uname)
                # existing_user.make_password(pword)
                # user=authenticate(requests,username=uname,password=pword)
                # print(user)
                auth_login(requests,users.objects.get(username=uname))
                return redirect("logout")
            else:
                data={"isusername":"hidden","ispasswordcorrect":"visible"}
                return render(requests,"login/login.html",data)
    
    data={"isusername":"hidden","ispasswordcorrect":"hidden"}
    return render(requests,"login/login.html",data)

def createuser(requests):
    if requests.method=="POST":
        uname=requests.POST.get("username")
        fname=requests.POST.get("first_name")
        lname=requests.POST.get("last_name")
        mail=requests.POST.get("email")
        pword=requests.POST.get("password")

        # print(uname,fname,lname,mail,pword)

        def checkusername(text):
            user_count=users.objects.filter(username=text).count()
            return user_count
        
        def checkemail(text):
            email_count=users.objects.filter(email=text).count()
            return email_count
        
        ucount=checkusername(uname)
        ecount=checkemail(mail)
        
        if(ucount==1 and ecount==1):
            data={"isusername":"visible","isemail":"visible"}
            return render(requests,"login/signup.html",data)

        if(ucount==1):
            data={"isusername":"visible","isemail":"hidden"}
            return render(requests,"login/signup.html",data)
        elif(ecount==1):
            data={"isusername":"hidden","isemail":"visible"}
            return render(requests,"login/signup.html",data)
        
        if(ucount==0 and ecount==0):
            adduser=users(username=uname,firstname=fname,lastname=lname,email=mail,password=pword,watchlist={"symbol":["sony","msft","meta","goog","aapl"]})
            adduser.save()
            return redirect("login")
    
    data={"isusername":"hidden","isemail":"hidden"}
    return render(requests,"login/signup.html",data)

# def logout(requests):
#     auth_logout(requests)
#     return HttpResponse("Logout!!")

def logout(requests):
    if requests.user.is_authenticated:
        # User is logged in
        user = requests.user
        # Your view logic here
        return HttpResponse(user.email)
    else:
        # User is not logged in
        user = None
        # Handle the case when user is not logged in
        return HttpResponse("No!!")
    return render(requests, 'template.html', {'user': user})


def dashboard(requests):
    if requests.user.is_authenticated:
        print("Yes")
        user=requests.user
        # print(user.watchlist["symbol"])
        watchlistsymbols=""
        for i in user.watchlist["symbol"]:
            watchlistsymbols=i+","+watchlistsymbols
        print(watchlistsymbols)
        data={
            "username":user.username,
            "name":user.firstname,
            "email":user.email,
            "totalbalance":user.balance,
            "watchlist":watchlistsymbols,
        }
    return render(requests,"main/dashboard.html",data)

def stockdetails(requests):
    return render(requests,"main/stocks.html")

def removewatchlist(requests,symbol):
    # print(symbol)
    wlist={"symbol":["sony","msft","meta","goog","aapl"]}
    wlist["symbol"].remove(symbol.lower())

    user = users.objects.first()
    user.watchlist=wlist

    # remove=users(watchlist=wlist)
    user.save()
    return redirect("dashboard")