import requests

response_step1 = requests.get("https://fc.yahoo.com")
cookie = response_step1.headers.get('Set-Cookie')

url_step2 = "https://query2.finance.yahoo.com/v1/test/getcrumb"
headers_step2 = headers = {
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Cookie": cookie
    }  # Include obtained cookie in request headers

response_step2 = requests.get(url_step2, headers=headers_step2)
crumb = response_step2.text

url_step3 = f"https://query2.finance.yahoo.com/v7/finance/quote?symbols=TSLA&crumb={crumb}"
response_step3 = requests.get(url_step3, headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
                                                  'Cookie': cookie})

cache = {'cookie': cookie, 'crumb': crumb}
print(response_step3.json())