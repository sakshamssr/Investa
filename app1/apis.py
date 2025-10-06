#import matplotlib.pyplot as plt
#import numpy as np

import requests
from datetime import datetime
from django.http import JsonResponse,HttpResponse
from .models import users
from .mdate import getdate,today

from json import dumps

def search(request,query):
    query=query.replace(" ","%20")
    url="https://query2.finance.yahoo.com/v1/finance/search?q="+query
    headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}

    response = requests.get(url,headers=headers)
    data = response.json()

    #print(type(data))
    store={"stocks":[]}

    # print(data.keys())

    # print(data["quotes"])

    for i in data["quotes"]:
        store["stocks"].append(i)

    return JsonResponse(store)

# print(search("apple"))

def watchlist(request, query):

    response_step1 = requests.get("https://fc.yahoo.com")
    cookie = response_step1.headers.get('Set-Cookie')

    url_step2 = "https://query2.finance.yahoo.com/v1/test/getcrumb"
    headers_step2 = headers = {
            "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "Cookie": cookie
        }  # Include obtained cookie in request headers

    response_step2 = requests.get(url_step2, headers=headers_step2)
    crumb = response_step2.text

    # url = f"https://query2.finance.yahoo.com/v7/finance/quote?symbols=TSLA&crumb={crumb}"

    # Construct the URL with the crumb value
    url = "https://query1.finance.yahoo.com/v7/finance/quote?&symbols=" + query + "&fields=currency,fromCurrency,toCurrency,exchangeTimezoneName,exchangeTimezoneShortName,gmtOffSetMilliseconds,regularMarketChange,regularMarketChangePercent,regularMarketPrice,regularMarketTime,preMarketTime,postMarketTime,extendedMarketTime&crumb="+crumb+"&formatted=false&region=US&lang=en-US"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Cookie": cookie
    }

    response_step3 = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",'Cookie': cookie})

    cache = {'cookie': cookie, 'crumb': crumb}

    data=response_step3.json()
    store={"stocks":[]}
    
    for i in range(0,len(data["quoteResponse"]["result"])):
        symbol=data["quoteResponse"]["result"][i]["symbol"]
        link="/removewatchlist/"+symbol
        store["stocks"].append([symbol,round(data["quoteResponse"]["result"][i]["regularMarketPrice"],2),round(data["quoteResponse"]["result"][i]["regularMarketChangePercent"],5),link,data["quoteResponse"]["result"][i]["marketState"]])
        # print(store)
    
    # print(store)
    return JsonResponse(store)

    

# Example usage:
# watchlist("e", "aapl,goog,meta,msft,sony")

def fetchdetails(request, query):
    url="https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/"+query+"?merge=false&padTimeSeries=true&period1=1698240600&period2=1714055399&type=quarterlyMarketCap%2CtrailingMarketCap%2CquarterlyEnterpriseValue%2CtrailingEnterpriseValue%2CquarterlyPeRatio%2CtrailingPeRatio%2CquarterlyForwardPeRatio%2CtrailingForwardPeRatio%2CquarterlyPegRatio%2CtrailingPegRatio%2CquarterlyPsRatio%2CtrailingPsRatio%2CquarterlyPbRatio%2CtrailingPbRatio%2CquarterlyEnterprisesValueRevenueRatio%2CtrailingEnterprisesValueRevenueRatio%2CquarterlyEnterprisesValueEBITDARatio%2CtrailingEnterprisesValueEBITDARatio&lang=en-US&region=US"
    headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
    response = requests.get(url,headers=headers)
    data = response.json()

    #print(data["chart"]["result"][0]["meta"])

    store={}

    for i in (data["timeseries"]["result"]):
        typ=i["meta"]["type"][0]
        store[typ]=i[typ][0]["reportedValue"]["fmt"]
    
    return JsonResponse(store)

def graphdata(request,query,start,end):
    # print("--------------------------------")
    # print(query,start,end)
    # print("--------------------------------")
    url="https://query2.finance.yahoo.com/v8/finance/chart/"+query+"?period1="+str(start)+"&period2="+str(end)+"&interval=5m&includePrePost=true&events=div%7Csplit%7Cearn&&lang=en-US&region=US"
    headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
    print(url)
    response = requests.get(url,headers=headers)
    data = response.json()

    store={"date":[],"close":[]}

    for i in range(0,len(data["chart"]["result"][0]["timestamp"])):
        store["date"].append(getdate(data["chart"]["result"][0]["timestamp"][i]))
        try:
            store["close"].append(round(data["chart"]["result"][0]["indicators"]["quote"][0]["close"][i],2))
        except:
            continue
    
    store["currency"]=data["chart"]["result"][0]["meta"]["currency"]
    return JsonResponse(store)

def portfolio(request):
    user=request.user
    stocks=user.stockbuy
    name=list(stocks.keys())
    print(name[0])
    print(name)
    stocksname=""
    for i in range(len(name)-1,-1,-1):
        print(i)
        stocksname=name[i]+","+stocksname
    print(stocksname)
    store=[]
    i=0
    url="http://127.0.0.1:8000/api/watchlist/"+stocksname
    headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
    response = requests.get(url,headers=headers)
    data = response.json()
    for i in range(0,len(name)):
        store.append({"symbol":[name[i]],"quantity":[stocks[name[i]]["quantity"]],"boughtat":[stocks[name[i]]["boughtat"]],"averageprice":[stocks[name[i]]["averageprice"]],"currentprice":data["stocks"][i][1],"percentchange":data["stocks"][i][2]})

    print(data["stocks"])
    print(store)
    
    return JsonResponse(store,safe=False)

def portfoliochart(request):
    user=request.user
    stocks=user.stockbuy
    price=[]
    name=list(stocks.keys())
    for i in name:
        price.append(user.stockbuy[i]["boughtat"]*user.stockbuy[i]["quantity"])

    store={"name":name,"price":price}
    return JsonResponse(store)

def income(request):
    user=request.user
    stocks=user.stockbuy
    price=[]
    name=list(stocks.keys())
    stocksname=""
    for i in range(len(name)-1,-1,-1):
        # print(i)
        stocksname=name[i]+","+stocksname
    print(stocksname)
    print(name)
    url="http://127.0.0.1:8000/api/watchlist/"+stocksname
    headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
    response = requests.get(url,headers=headers)
    data = response.json()
    storepl=0
    print(data["stocks"][0])
    for i in range(0,len(name)):
        investedamount=user.stockbuy[name[i]]["averageprice"]*user.stockbuy[name[i]]["quantity"]
        currentamount=data["stocks"][i][1]*user.stockbuy[name[i]]["quantity"]
        # print("investedamount",investedamount)
        # print("Current Amount",currentamount)
        pl=currentamount-investedamount
        storepl=storepl+round(pl,2)
    return HttpResponse(round(storepl,2))

def holdings(request,query):
    # print("---------------Holdings-----------------")
    # print(query)
    # print("---------------Holdings-----------------")
    logedInUser=request.user
    stocks=logedInUser.stockbuy.keys()
    print(logedInUser)
    print(stocks)
    if(query in list(stocks)):
        # url="http://127.0.0.1:8000/api/watchlist/"+query
        # headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
        # response = requests.get(url,headers=headers)
        # data = response.json()
        return HttpResponse(logedInUser.stockbuy[query]["quantity"])
    else:
        return HttpResponse(0)
    
def addtoWatchlist(request,query):
    logedInUser=request.user
    watchlist=logedInUser.watchlist
    print(watchlist)
    print(query)
    if(query in watchlist["symbol"]):
        print("Already Exists")
        return JsonResponse({"response":"Already Exists"})
    else:
        watchlist["symbol"].append(query)
        logedInUser.save()
        return JsonResponse({"response":"Added "+query})