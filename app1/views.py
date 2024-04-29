from django.shortcuts import render,HttpResponse,redirect
from .models import users
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import requests as req
from .mdate import today

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
        print(user)
        print(user.watchlist)
        watchlistsymbols=""
        for i in user.watchlist["symbol"]:
            watchlistsymbols=i+","+watchlistsymbols
        # print(watchlistsymbols)
        data={
            "username":user.username,
            "name":user.firstname,
            "email":user.email,
            "totalbalance":round(user.balance,2),
            "watchlist":watchlistsymbols,
        }
    return render(requests,"main/dashboard.html",data)

def stockdetails(requests,query):
    if requests.user.is_authenticated:
        todayepoch=int(today())
        url="https://query2.finance.yahoo.com/v8/finance/chart/"+query+"?period1="+str(todayepoch-457199)+"&period2="+str(todayepoch)+"&interval=5m&includePrePost=true&events=div%7Csplit%7Cearn&&lang=en-US&region=US"
        headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
        response = req.get(url,headers=headers)
        data = response.json()

        store={}
        data=data["chart"]["result"][0]["meta"]
        previousclose=data["previousClose"]

        for i in data.keys():
            if i == ("firstTradeDate") or i == ("regularMarketTime") or i == ("hasPrePostMarketData") or i == ("gmtoffset") or i == ("timezone") or i == ("instrumentType") or i == ("fullExchangeName") or i == ("regularMarketVolume") or i == ("previousClose") or i == ("regularMarketPrice"):
                continue
            if i == "scale":
                break
            store[i.capitalize()]=data[i]
            
        
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
            "totalbalance":round(user.balance,2),
            "watchlist":watchlistsymbols,
            "data":store,
            "query":query,
            "previousclose":previousclose,
        }
    return render(requests,"main/details.html",data)

def removewatchlist(requests,symbol):
    # print(symbol)
    wlist={"symbol":["sony","msft","meta","goog","aapl"]}
    wlist["symbol"].remove(symbol.lower())

    user = users.objects.first()
    user.watchlist=wlist

    # remove=users(watchlist=wlist)
    user.save()
    return redirect("dashboard")


def updatestocks(requests):
    if requests.method == "POST":
        quantity=int(requests.POST.get("quantity-input"))
        print(quantity)
        name=requests.POST.get("symbolname")
        print(name)
        currentprice=float(requests.POST.get("currentprice"))
        print(currentprice)
        if "buy" in requests.POST:
            user = users.objects.first()
            if (name in user.stockbuy.keys()):
                previousprice=user.stockbuy[name]["quantity"]*user.stockbuy[name]["boughtat"]
                currentshareprice=quantity*currentprice
                totalquantity=int(user.stockbuy[name]["quantity"])+int(quantity)
                averageprice=(previousprice+currentshareprice)/totalquantity
                user.stockbuy[name]={"quantity":totalquantity, "boughtat":currentprice, "averageprice":averageprice }
                user.balance=user.balance-float(quantity*currentprice)
            else:
            # user.stockbuy={}
                user.stockbuy[name]={"quantity": quantity ,"boughtat": currentprice, "averageprice": currentprice }
                user.balance=user.balance-float(quantity*currentprice)
            user.save()
            print("Buy")
        if "sell" in requests.POST:
            user=users.objects.first()
            if (name in user.stockbuy.keys()):
                if user.stockbuy[name]["quantity"] < quantity:
                    print("Not Enough Shares Holding")
                elif(  ):
                    pass
                else:
                    user.stockbuy[name].update({"quantity":user.stockbuy[name]["quantity"]-quantity})
                    user.balance=user.balance+(currentprice*quantity)
                    user.save()
                    print("Sell")
            else:
                print("Quantity is 0")
            print("Sell")
    
    return(redirect('/'))