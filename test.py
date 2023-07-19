import requests
from bs4 import BeautifulSoup

headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13"}
url = "https://www.rakuten.com.tw/search/" + "PS5"
r = requests.get(url, headers = headers, verify=False)
print(r)
if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'html.parser')

lis = soup.find(class_="product-grid")
print(lis)


