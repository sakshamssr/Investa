#import matplotlib.pyplot as plt
#import numpy as np

import requests
from datetime import datetime
from django.http import JsonResponse
from .models import users
from .mdate import getdate

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

    user = users.objects.first()
    print(user.cache)

    if(len(user.cache)==0):
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

        user.cache=store
        user.save()
        return JsonResponse(store)
    else:
        store=user.cache
        user.cache=[]
        user.save()
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

def graphdata(request,query):
    url="https://query2.finance.yahoo.com/v8/finance/chart/"+query+"?period1=1713943800&period2=1714116600&interval=5m&includePrePost=true&events=div%7Csplit%7Cearn&&lang=en-US&region=US"
    headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
    response = requests.get(url,headers=headers)
    data = response.json()

    store={"date":[],"close":[]}

    for i in range(0,len(data["chart"]["result"][0]["timestamp"])):
        store["date"].append(getdate(data["chart"]["result"][0]["timestamp"][i]))
        store["close"].append(data["chart"]["result"][0]["indicators"]["quote"][0]["close"][i])
    
    return JsonResponse(store)


