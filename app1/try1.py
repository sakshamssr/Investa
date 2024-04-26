import requests
from mdate import getdate
query="ADANIENT.NS"

url="https://query2.finance.yahoo.com/v8/finance/chart/"+query+"?period1=1713943800&period2=1714116600&interval=1m&includePrePost=true&events=div%7Csplit%7Cearn&&lang=en-US&region=US"
print(url)
headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
response = requests.get(url,headers=headers)
data = response.json()

print(data)

#print(data["chart"]["result"][0]["indicators"]["quote"][0]["close"])
#print(data["chart"]["result"][0]["timestamp"])

store={"date":[],"close":[]}

for i in range(0,len(data["chart"]["result"][0]["timestamp"])):
    store["date"].append(getdate(data["chart"]["result"][0]["timestamp"][i]))
    store["close"].append(data["chart"]["result"][0]["indicators"]["quote"][0]["close"][i])

print(store)
    
